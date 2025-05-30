#!/usr/bin/env python3
"""
ClaudeStack Launcher - Auto-launch all agents in separate terminals

This script detects the OS and launches each agent in its own terminal window/tab.
Supports macOS and Linux (GNOME).
"""

import os
import sys
import time
import platform
import subprocess
import argparse
from pathlib import Path

class ClaudeStackLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.agents_dir = self.base_dir / "agents"
        self.system = platform.system().lower()
        
        # Default agents to launch
        self.default_agents = [
            "chat",
            "planner", 
            "tasker",
            "coder",
            "reviewer",
            "tester",
            "designer",
            "frontend",
            "helper"
        ]
    
    def check_requirements(self):
        """Check if system requirements are met"""
        # Check if agent_runner.py exists
        agent_runner = self.agents_dir / "agent_runner.py"
        if not agent_runner.exists():
            print("❌ Error: agents/agent_runner.py not found")
            print("   Please run the setup first to create the agent runner.")
            return False
        
        # Check if Anthropic API key is set
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
            print("   Please set your API key: export ANTHROPIC_API_KEY='your-key-here'")
            return False
        
        return True
    
    def launch_macos_terminal(self, agent_name):
        """Launch agent in macOS Terminal"""
        script = f"""
        tell application "Terminal"
            do script "cd '{self.base_dir}' && python3 agents/agent_runner.py --agent {agent_name}"
        end tell
        """
        
        try:
            subprocess.run(["osascript", "-e", script], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to launch {agent_name} in Terminal: {e}")
            return False
    
    def launch_macos_iterm(self, agent_name):
        """Launch agent in macOS iTerm2"""
        script = f"""
        tell application "iTerm2"
            tell current window
                create tab with default profile
                tell current session
                    write text "cd '{self.base_dir}' && python3 agents/agent_runner.py --agent {agent_name}"
                end tell
            end tell
        end tell
        """
        
        try:
            subprocess.run(["osascript", "-e", script], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to launch {agent_name} in iTerm2: {e}")
            return False
    
    def launch_linux_gnome(self, agent_name):
        """Launch agent in GNOME Terminal"""
        cmd = [
            "gnome-terminal",
            "--tab",
            "--title", f"Claude-{agent_name.title()}",
            "--", "bash", "-c",
            f"cd '{self.base_dir}' && python3 agents/agent_runner.py --agent {agent_name}; exec bash"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to launch {agent_name} in GNOME Terminal: {e}")
            return False
        except FileNotFoundError:
            print("❌ GNOME Terminal not found. Please install it or use a different terminal.")
            return False
    
    def launch_agent(self, agent_name):
        """Launch a single agent based on the current OS"""
        print(f"🚀 Launching Claude-{agent_name.title()}...")
        
        if self.system == "darwin":  # macOS
            # Try iTerm2 first, fallback to Terminal
            if not self.launch_macos_iterm(agent_name):
                return self.launch_macos_terminal(agent_name)
            return True
        
        elif self.system == "linux":
            return self.launch_linux_gnome(agent_name)
        
        else:
            print(f"❌ Unsupported operating system: {self.system}")
            print("   ClaudeStack currently supports macOS and Linux only.")
            return False
    
    def launch_router(self):
        """Launch the router in a separate terminal"""
        print("🔀 Launching Router...")
        
        if self.system == "darwin":  # macOS
            script = f"""
            tell application "Terminal"
                do script "cd '{self.base_dir}' && python3 router.py"
            end tell
            """
            try:
                subprocess.run(["osascript", "-e", script], check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        
        elif self.system == "linux":
            cmd = [
                "gnome-terminal",
                "--tab",
                "--title", "ClaudeStack-Router",
                "--", "bash", "-c",
                f"cd '{self.base_dir}' && python3 router.py; exec bash"
            ]
            try:
                subprocess.run(cmd, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        
        return False
    
    def launch_all(self, agents_to_launch, exclude_agents=None):
        """Launch all specified agents"""
        if not self.check_requirements():
            return False
        
        exclude_agents = exclude_agents or []
        agents_to_launch = [agent for agent in agents_to_launch if agent not in exclude_agents]
        
        print(f"🎯 ClaudeStack Launcher - {self.system.title()}")
        print(f"📁 Base directory: {self.base_dir}")
        print(f"🤖 Launching {len(agents_to_launch)} agents...\n")
        
        # Launch router first
        if not self.launch_router():
            print("⚠️  Warning: Could not launch router automatically")
            print("   You can start it manually: python3 router.py")
        
        time.sleep(1)  # Give router time to start
        
        # Launch each agent
        successful_launches = 0
        for agent in agents_to_launch:
            if self.launch_agent(agent):
                successful_launches += 1
                time.sleep(0.5)  # Small delay between launches
            else:
                print(f"⚠️  Warning: Could not launch {agent} automatically")
                print(f"   You can start it manually: python3 agents/agent_runner.py --agent {agent}")
        
        print(f"\n✅ Successfully launched {successful_launches}/{len(agents_to_launch)} agents")
        
        if successful_launches > 0:
            print("\n🎉 ClaudeStack is ready!")
            print("📝 Start chatting by editing: inbox/chat.txt")
            print("📊 Monitor logs at: logs/messages.log")
            print("\n💡 Tip: Each agent runs in its own terminal window")
        
        return successful_launches > 0

def main():
    parser = argparse.ArgumentParser(description="Launch ClaudeStack agents")
    parser.add_argument(
        "--agents", 
        nargs="*", 
        help="Specific agents to launch (default: all)"
    )
    parser.add_argument(
        "--exclude", 
        nargs="*", 
        default=[],
        help="Agents to exclude from launch"
    )
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List available agents"
    )
    
    args = parser.parse_args()
    launcher = ClaudeStackLauncher()
    
    if args.list:
        print("Available agents:")
        for agent in launcher.default_agents:
            print(f"  - {agent}")
        return
    
    agents_to_launch = args.agents if args.agents else launcher.default_agents
    
    try:
        launcher.launch_all(agents_to_launch, args.exclude)
    except KeyboardInterrupt:
        print("\n👋 Launch cancelled")
        sys.exit(1)

if __name__ == "__main__":
    main()