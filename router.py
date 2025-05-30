#!/usr/bin/env python3
"""
ClaudeStack Router - Intelligent message routing between agents

This module handles:
- Reading from inbox/chat.txt
- Using Claude to classify user intent
- Routing messages to appropriate agent inboxes
- Logging all routing decisions
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic

class ClaudeStackRouter:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.inbox_dir = self.base_dir / "inbox"
        self.outbox_dir = self.base_dir / "outbox"
        self.logs_dir = self.base_dir / "logs"
        self.config_dir = self.base_dir / "config"
        
        # Ensure directories exist
        for dir_path in [self.inbox_dir, self.outbox_dir, self.logs_dir, self.config_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize Anthropic client
        self.client = Anthropic()
        
        # Load routing rules
        self.routing_rules = self.load_routing_rules()
        
        # Track last processed message
        self.last_chat_hash = None
        
    def load_routing_rules(self):
        """Load routing rules from config/routing_rules.json"""
        rules_file = self.config_dir / "routing_rules.json"
        if rules_file.exists():
            with open(rules_file, 'r') as f:
                return json.load(f)
        else:
            # Default routing rules
            default_rules = {
                "feature_request": "planner",
                "code_question": "helper",
                "ui_request": "designer",
                "bug_fix": "coder",
                "code_review": "reviewer",
                "testing": "tester",
                "general": "helper"
            }
            # Save default rules
            with open(rules_file, 'w') as f:
                json.dump(default_rules, f, indent=2)
            return default_rules
    
    def get_file_hash(self, file_path):
        """Get MD5 hash of file content"""
        if not file_path.exists():
            return None
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def classify_intent(self, message):
        """Use Claude to classify user intent"""
        classification_prompt = f"""
You are a message classifier for ClaudeStack, a multi-agent AI development framework.

Analyze the following user message and classify it into ONE of these categories:
- feature_request: User wants to build/add a new feature
- code_question: User has questions about existing code or general programming
- ui_request: User wants UI/UX design or frontend work
- bug_fix: User reports a bug or wants something fixed
- code_review: User wants code reviewed
- testing: User wants tests written or testing help
- general: Anything else

User message: "{message}"

Respond with ONLY the category name (e.g., "feature_request").
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=50,
                messages=[{"role": "user", "content": classification_prompt}]
            )
            intent = response.content[0].text.strip().lower()
            
            # Validate intent is in our routing rules
            if intent in self.routing_rules:
                return intent
            else:
                return "general"  # Default fallback
                
        except Exception as e:
            self.log_message(f"Error classifying intent: {e}")
            return "general"  # Default fallback
    
    def route_message(self, message, intent):
        """Route message to appropriate agent inbox"""
        target_agent = self.routing_rules.get(intent, "helper")
        target_file = self.inbox_dir / f"{target_agent}.md"
        
        # Write message to target agent's inbox
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        routed_content = f"""# New Request - {timestamp}

**Intent:** {intent}
**Original Message:**

{message}

---
"""
        
        with open(target_file, 'w') as f:
            f.write(routed_content)
        
        # Log the routing decision
        log_entry = f"[{timestamp}] Routed user query (intent: {intent}) to {target_agent}"
        self.log_message(log_entry)
        
        return target_agent
    
    def log_message(self, message):
        """Log message to logs/messages.log"""
        log_file = self.logs_dir / "messages.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def process_chat_input(self):
        """Check for new input in inbox/chat.txt and route it"""
        chat_file = self.inbox_dir / "chat.txt"
        
        if not chat_file.exists():
            return False
        
        # Check if file has changed
        current_hash = self.get_file_hash(chat_file)
        if current_hash == self.last_chat_hash:
            return False
        
        # Read the message
        with open(chat_file, 'r') as f:
            message = f.read().strip()
        
        if not message:
            return False
        
        # Classify and route
        intent = self.classify_intent(message)
        target_agent = self.route_message(message, intent)
        
        # Update hash
        self.last_chat_hash = current_hash
        
        print(f"✅ Routed message to {target_agent} (intent: {intent})")
        return True
    
    def run(self, poll_interval=2):
        """Main router loop"""
        print("🚀 ClaudeStack Router started")
        print(f"📁 Watching: {self.inbox_dir / 'chat.txt'}")
        print(f"📝 Logging to: {self.logs_dir / 'messages.log'}")
        print("\n💬 Type your messages in inbox/chat.txt to get started!\n")
        
        try:
            while True:
                self.process_chat_input()
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\n👋 Router stopped")

if __name__ == "__main__":
    router = ClaudeStackRouter()
    router.run()