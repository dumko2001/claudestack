#!/usr/bin/env python3
"""
ClaudeStack Agent Runner - Universal agent execution script

This script can run any ClaudeStack agent by:
1. Loading the agent's specific prompt template
2. Watching the agent's inbox for new input
3. Processing input through Claude API
4. Writing output to the agent's outbox
5. Logging all interactions
"""

import os
import sys
import json
import time
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic

class ClaudeStackAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.base_dir = Path(__file__).parent.parent
        self.prompts_dir = self.base_dir / "prompts"
        self.inbox_dir = self.base_dir / "inbox"
        self.outbox_dir = self.base_dir / "outbox"
        self.logs_dir = self.base_dir / "logs"
        self.config_dir = self.base_dir / "config"
        
        # Ensure directories exist
        for dir_path in [self.inbox_dir, self.outbox_dir, self.logs_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=api_key)
        
        # Load agent configuration
        self.model = self.load_model_assignment()
        self.prompt_template = self.load_prompt_template()
        
        # Track last processed input
        self.last_input_hash = None
        
        print(f"🤖 Claude-{self.agent_name.title()} initialized")
        print(f"📋 Model: {self.model}")
        print(f"📁 Watching: {self.inbox_dir / f'{self.agent_name}.md'}")
        print(f"📤 Output: {self.outbox_dir / f'{self.agent_name}.md'}")
    
    def load_model_assignment(self):
        """Load model assignment from config"""
        config_file = self.config_dir / "model_assignments.json"
        
        # Default model assignments based on latest Claude Code capabilities
        default_assignments = {
            "chat": "claude-3-5-sonnet-20241022",
            "planner": "claude-3-opus-20240229",  # Complex planning needs Opus
            "tasker": "claude-3-5-sonnet-20241022",
            "coder": "claude-3-5-sonnet-20241022",  # Sonnet excels at coding
            "reviewer": "claude-3-opus-20240229",  # Code review needs deep analysis
            "tester": "claude-3-5-sonnet-20241022",
            "designer": "claude-3-opus-20240229",  # Creative design needs Opus
            "frontend": "claude-3-5-sonnet-20241022",
            "helper": "claude-3-5-sonnet-20241022"
        }
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                assignments = json.load(f)
        else:
            assignments = default_assignments
            # Save default assignments
            self.config_dir.mkdir(exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(assignments, f, indent=2)
        
        return assignments.get(self.agent_name, "claude-3-5-sonnet-20241022")
    
    def load_prompt_template(self):
        """Load agent-specific prompt template"""
        prompt_file = self.prompts_dir / f"{self.agent_name}.txt"
        
        if prompt_file.exists():
            with open(prompt_file, 'r') as f:
                return f.read().strip()
        else:
            # Create default prompt if it doesn't exist
            default_prompt = self.get_default_prompt()
            self.prompts_dir.mkdir(exist_ok=True)
            with open(prompt_file, 'w') as f:
                f.write(default_prompt)
            return default_prompt
    
    def get_default_prompt(self):
        """Get default prompt template for the agent"""
        prompts = {
            "chat": """
You are Claude-Chat, the main interface for ClaudeStack.

Your role:
- Receive user input and understand their intent
- Provide helpful responses when appropriate
- The router will handle directing complex requests to other agents

Be conversational, helpful, and professional. If a user asks something that would be better handled by a specialist agent, acknowledge their request and let them know it's being routed appropriately.
""",
            "planner": """
You are Claude-Planner, an expert in breaking down software feature requests into clear technical plans.

Input: A user request for a feature or system.
Output: A markdown plan with these sections:
- 📌 **Objective**: Clear statement of what needs to be built
- 🛠 **Implementation Plan**: Detailed bullet points covering:
  - Architecture decisions
  - Key components needed
  - Technology choices
  - Integration points
  - Potential challenges

Be precise, include system boundaries, and consider scalability and maintainability.
""",
            "tasker": """
You are Claude-Tasker. Your job is to convert planning docs into atomic developer tasks.

Input: Claude-Planner's implementation plan.
Output: Markdown task list, formatted as:
- [ ] Task Name - brief description (estimated time)

Rules:
- Each task should be completable in < 30 minutes ideally
- Tasks should be specific and actionable
- Include setup, implementation, and testing tasks
- Order tasks logically (dependencies first)
- Be clear about what "done" looks like for each task
""",
            "coder": """
You are Claude-Coder. You write clean, efficient, production-ready code based on task descriptions.

Input: One specific development task.
Output: Complete code implementation with:
- Well-commented, readable code
- Error handling where appropriate
- Following best practices for the language/framework
- Include any necessary imports/dependencies

Focus on code quality, security, and maintainability. If the task is unclear, ask for clarification.
""",
            "reviewer": """
You are Claude-Reviewer. You provide thorough, constructive code reviews.

Input: Code implementation from Claude-Coder.
Output: Detailed review covering:
- ✅ **Strengths**: What's done well
- ⚠️ **Issues**: Problems that need fixing (security, bugs, performance)
- 💡 **Suggestions**: Improvements for readability, maintainability
- 🎯 **Verdict**: APPROVED / NEEDS_CHANGES / MAJOR_REVISION

Be thorough but constructive. Focus on code quality, security, performance, and best practices.
""",
            "tester": """
You are Claude-Tester. You write comprehensive tests and identify potential issues.

Input: Code implementation or feature description.
Output: Test suite including:
- Unit tests for individual functions
- Integration tests for component interactions
- Edge case testing
- Error condition testing
- Performance considerations

Use appropriate testing frameworks and follow testing best practices. Include both positive and negative test cases.
""",
            "designer": """
You are Claude-Designer, a UI/UX architect focused on user experience.

Input: Feature requirements or user interface needs.
Output: Design specification including:
- 🎨 **User Experience Flow**: Step-by-step user journey
- 📱 **Interface Design**: Layout and component descriptions
- 🎯 **Key Interactions**: How users will interact with the feature
- 📋 **Component List**: Specific UI components needed
- 💡 **Design Principles**: Accessibility, usability considerations

Keep designs simple, user-friendly, and implementable. Focus on solving user problems effectively.
""",
            "frontend": """
You are Claude-Frontend. You implement UI components based on design specifications.

Input: UI component descriptions, wireframes, or design specs.
Output: Frontend code including:
- HTML structure
- CSS styling (responsive design)
- JavaScript functionality
- Framework-specific code (React, Vue, etc.) if specified

Create clean, accessible, and responsive interfaces. Follow modern web standards and best practices.
""",
            "helper": """
You are Claude-Helper, a general-purpose coding assistant.

Your role:
- Answer questions about code architecture and logic
- Explain complex programming concepts
- Provide guidance on tools and technologies
- Help debug issues
- Offer best practice recommendations

Be helpful, educational, and provide practical advice. Include examples when helpful.
"""
        }
        
        return prompts.get(self.agent_name, f"""
You are Claude-{self.agent_name.title()}, a specialized AI assistant.

Please provide helpful and accurate responses based on your role.
""")
    
    def get_file_hash(self, file_path):
        """Get MD5 hash of file content"""
        if not file_path.exists():
            return None
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def log_interaction(self, input_text, output_text, processing_time):
        """Log interaction to messages.log"""
        log_file = self.logs_dir / "messages.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
[{timestamp}] Claude-{self.agent_name.title()} processed request
Processing time: {processing_time:.2f}s
Model: {self.model}
Input length: {len(input_text)} chars
Output length: {len(output_text)} chars
---
"""
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
    
    def process_input(self, input_text):
        """Process input through Claude API"""
        start_time = time.time()
        
        # Combine prompt template with user input
        full_prompt = f"{self.prompt_template}\n\n---\n\nUser Input:\n{input_text}"
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            output_text = response.content[0].text
            processing_time = time.time() - start_time
            
            # Log the interaction
            self.log_interaction(input_text, output_text, processing_time)
            
            return output_text
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def check_for_input(self):
        """Check for new input in agent's inbox"""
        inbox_file = self.inbox_dir / f"{self.agent_name}.md"
        
        if not inbox_file.exists():
            return False
        
        # Check if file has changed
        current_hash = self.get_file_hash(inbox_file)
        if current_hash == self.last_input_hash or current_hash is None:
            return False
        
        # Read and process input
        with open(inbox_file, 'r') as f:
            input_text = f.read().strip()
        
        if not input_text:
            return False
        
        print(f"📨 New input received ({len(input_text)} chars)")
        print("🔄 Processing...")
        
        # Process through Claude
        output = self.process_input(input_text)
        
        # Write output
        outbox_file = self.outbox_dir / f"{self.agent_name}.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output_content = f"""# Claude-{self.agent_name.title()} Output - {timestamp}

{output}

---
*Generated by ClaudeStack Agent Runner*
"""
        
        with open(outbox_file, 'w') as f:
            f.write(output_content)
        
        # Update hash
        self.last_input_hash = current_hash
        
        print(f"✅ Output written to {outbox_file}")
        return True
    
    def run(self, poll_interval=2):
        """Main agent loop"""
        print(f"\n🚀 Claude-{self.agent_name.title()} is running")
        print("💬 Waiting for input...\n")
        
        try:
            while True:
                self.check_for_input()
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            print(f"\n👋 Claude-{self.agent_name.title()} stopped")

def main():
    parser = argparse.ArgumentParser(description="Run a ClaudeStack agent")
    parser.add_argument(
        "--agent", 
        required=True,
        help="Agent name to run (e.g., coder, planner, helper)"
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=2,
        help="Polling interval in seconds (default: 2)"
    )
    
    args = parser.parse_args()
    
    try:
        agent = ClaudeStackAgent(args.agent)
        agent.run(args.poll_interval)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()