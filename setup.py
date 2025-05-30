#!/usr/bin/env python3
"""
ClaudeStack Setup Script

This script helps users set up ClaudeStack quickly by:
1. Checking system requirements
2. Installing dependencies
3. Setting up configuration
4. Validating the installation
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class ClaudeStackSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.errors = []
        self.warnings = []
    
    def print_header(self):
        print("\n" + "="*60)
        print("🚀 ClaudeStack v1.0 Setup")
        print("="*60)
        print("Terminal-first, multi-agent AI development framework")
        print("="*60 + "\n")
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("📋 Checking Python version...")
        
        if sys.version_info < (3, 8):
            self.errors.append("Python 3.8+ is required. Current version: {}.{}.{}".format(
                sys.version_info.major, sys.version_info.minor, sys.version_info.micro
            ))
            return False
        
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
        return True
    
    def check_api_key(self):
        """Check if Anthropic API key is set"""
        print("\n🔑 Checking API key...")
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            self.warnings.append(
                "ANTHROPIC_API_KEY environment variable not set. "
                "You'll need to set this before running ClaudeStack."
            )
            print("⚠️  ANTHROPIC_API_KEY not found")
            print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
            return False
        
        # Basic validation (should start with 'sk-ant-')
        if not api_key.startswith('sk-ant-'):
            self.warnings.append("API key format looks incorrect. Should start with 'sk-ant-'")
            print("⚠️  API key format looks incorrect")
            return False
        
        print("✅ API key found and format looks correct")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\n📦 Installing dependencies...")
        
        requirements_file = self.base_dir / "requirements.txt"
        if not requirements_file.exists():
            self.errors.append("requirements.txt not found")
            return False
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install dependencies: {e}")
            return False
    
    def verify_directory_structure(self):
        """Verify all required directories exist"""
        print("\n📁 Verifying directory structure...")
        
        required_dirs = [
            "agents", "inbox", "outbox", "logs", "config", "prompts", "examples"
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
                dir_path.mkdir(exist_ok=True)
        
        if missing_dirs:
            print(f"📁 Created missing directories: {', '.join(missing_dirs)}")
        
        print("✅ Directory structure verified")
        return True
    
    def verify_core_files(self):
        """Verify core files exist"""
        print("\n📄 Verifying core files...")
        
        required_files = [
            "router.py",
            "launcher.py",
            "agents/agent_runner.py",
            "config/routing_rules.json",
            "config/model_assignments.json"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.errors.append(f"Missing core files: {', '.join(missing_files)}")
            return False
        
        print("✅ All core files present")
        return True
    
    def test_anthropic_connection(self):
        """Test connection to Anthropic API"""
        print("\n🔗 Testing Anthropic API connection...")
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  Skipping API test (no API key)")
            return False
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            
            # Simple test call
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            
            print("✅ API connection successful")
            return True
            
        except ImportError:
            self.warnings.append("anthropic package not installed")
            return False
        except Exception as e:
            self.warnings.append(f"API connection failed: {str(e)}")
            return False
    
    def create_sample_input(self):
        """Create a sample input file for testing"""
        print("\n📝 Creating sample input...")
        
        sample_content = """
# Welcome to ClaudeStack!

This is a sample input file. Try asking:

"Help me plan a simple Python web scraper that can extract article titles from a news website."

Or:

"Review this code for potential issues:
```python
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return database.execute(query)
```"

Delete this content and write your own request!
"""
        
        sample_file = self.base_dir / "inbox" / "chat.md"
        with open(sample_file, 'w') as f:
            f.write(sample_content)
        
        print(f"✅ Sample input created: {sample_file}")
    
    def print_summary(self):
        """Print setup summary"""
        print("\n" + "="*60)
        print("📊 Setup Summary")
        print("="*60)
        
        if not self.errors:
            print("🎉 Setup completed successfully!")
            print("\n🚀 Quick Start:")
            print("   1. Set your API key: export ANTHROPIC_API_KEY='your-key'")
            print("   2. Launch ClaudeStack: python launcher.py")
            print("   3. Edit inbox/chat.md with your request")
            print("   4. Check outbox/ for agent responses")
        else:
            print("❌ Setup completed with errors:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        print("\n📚 Documentation:")
        print("   • README.md - Project overview")
        print("   • examples/basic_usage.md - Usage examples")
        print("   • PRD.md - Product requirements")
        
        print("\n" + "="*60)
    
    def run(self):
        """Run the complete setup process"""
        self.print_header()
        
        # Run all setup steps
        steps = [
            self.check_python_version,
            self.verify_directory_structure,
            self.verify_core_files,
            self.check_api_key,
            self.install_dependencies,
            self.test_anthropic_connection,
            self.create_sample_input
        ]
        
        for step in steps:
            try:
                step()
            except Exception as e:
                self.errors.append(f"Setup step failed: {str(e)}")
        
        self.print_summary()
        
        # Return success status
        return len(self.errors) == 0

def main():
    setup = ClaudeStackSetup()
    success = setup.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()