# ClaudeStack - Terminal-First Multi-Agent AI Dev Framework

🚀 **A revolutionary open-source framework that orchestrates multiple specialized Claude AI agents through terminal-based communication.**

## 🧭 Overview

ClaudeStack enables developers to interact with multiple specialized Claude AI agents through a single interface. Each agent runs in its own terminal window and performs a distinct role in the software development lifecycle.

**No servers, no databases, no dashboards** — just smart agent routing, local file-based communication, and raw Claude power.

## 💡 Key Features

✅ **Single Chat Interface** – Talk to one Claude (Claude-Chat) and get routed intelligently  
✅ **Multi-Agent System** – Each Claude instance runs in a terminal and handles a single responsibility  
✅ **Zero Infrastructure** – No DB, no backend, no frontend required. All communication through shared folders  
✅ **Model-Specific Roles** – Different Claude models (Sonnet/Opus) assigned based on complexity  
✅ **Expandable Design** – Add/remove/replace agents easily  

## 🧩 Agent Architecture

| Agent Name | Model | Role Description |
|------------|-------|------------------|
| Claude-Chat | Sonnet-4 | Main user interface — interprets input and routes it |
| Claude-Planner | Opus-4 | Breaks down high-level feature requests into dev plans |
| Claude-Tasker | Sonnet-4 | Converts plans into atomic development tasks |
| Claude-Coder | Sonnet-4 | Implements code based on specific tasks |
| Claude-Reviewer | Opus-4 | Reviews written code and gives feedback |
| Claude-Tester | Sonnet-4 | Writes and runs tests, finds bugs, ensures stability |
| Claude-Designer | Opus-4 | Generates UX/UI design specs, wireframes |
| Claude-Frontend | Sonnet-4 | Implements frontend UI components |
| Claude-Helper | Sonnet-4 | General-purpose support: codebase explanation, Q&A |

## 🔁 Agent Flow

```
You → Claude-Chat → Claude-Planner → Claude-Tasker → Claude-Coder → Claude-Reviewer → Claude-Tester
                                        ↓
                                  Claude-Designer → Claude-Frontend
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API key
- Terminal access (macOS/Linux)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/claudestack.git
   cd claudestack
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Anthropic API key:**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

4. **Launch all agents:**
   ```bash
   python launcher.py
   ```

5. **Start chatting:**
   - Open `inbox/chat.txt` in your favorite editor
   - Type your request and save the file
   - Watch the magic happen across multiple terminal windows!

## 📁 Project Structure

```
claudestack/
├── agents/
│   └── agent_runner.py      # Shared runner for all agents
├── inbox/
│   ├── chat.txt             # Your input goes here
│   ├── planner.md           # Input to planner
│   ├── tasker.md            # Input to tasker
│   ├── coder.md             # Input to coder
│   └── ...                  # Other agent inputs
├── outbox/
│   └── ...                  # Agent outputs
├── logs/
│   └── messages.log         # Chronological logs
├── config/
│   ├── model_assignments.json
│   └── routing_rules.json
├── prompts/
│   └── ...                  # Agent prompt templates
├── router.py                # Core routing logic
├── launcher.py              # Auto-terminal launcher
└── README.md
```

## 🛠 Usage Examples

### Feature Request
```
# In inbox/chat.txt
"I need a user authentication system with JWT tokens and password reset functionality"

# ClaudeStack will:
# 1. Route to Claude-Planner for breakdown
# 2. Claude-Tasker creates atomic tasks
# 3. Claude-Coder implements each piece
# 4. Claude-Reviewer ensures quality
# 5. Claude-Tester adds comprehensive tests
```

### Code Question
```
# In inbox/chat.txt
"How does the authentication middleware work in this codebase?"

# Routes directly to Claude-Helper for explanation
```

### UI Request
```
# In inbox/chat.txt
"Design a modern dashboard for user analytics"

# Routes to Claude-Designer → Claude-Frontend
```

## 🔧 Configuration

### Model Assignments
Edit `config/model_assignments.json` to customize which Claude model each agent uses:

```json
{
  "chat": "claude-3-5-sonnet-20241022",
  "planner": "claude-3-opus-20240229",
  "coder": "claude-3-5-sonnet-20241022",
  "reviewer": "claude-3-opus-20240229"
}
```

### Routing Rules
Customize `config/routing_rules.json` to control how requests are routed:

```json
{
  "feature_request": "planner",
  "code_question": "helper",
  "ui_request": "designer",
  "bug_fix": "coder",
  "code_review": "reviewer"
}
```

## 🚀 Extending ClaudeStack

### Adding a New Agent

1. **Create prompt template:**
   ```bash
   # Create prompts/my_agent.txt
   echo "You are Claude-MyAgent..." > prompts/my_agent.txt
   ```

2. **Add to model assignments:**
   ```json
   {
     "my_agent": "claude-3-5-sonnet-20241022"
   }
   ```

3. **Update routing rules:**
   ```json
   {
     "my_task_type": "my_agent"
   }
   ```

4. **Launch the agent:**
   ```bash
   python agents/agent_runner.py --agent my_agent
   ```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Anthropic's Claude](https://www.anthropic.com/claude) AI models
- Inspired by the need for better AI-assisted development workflows
- Special thanks to the open-source community

---

**Ready to revolutionize your development workflow? Give ClaudeStack a try!** 🚀