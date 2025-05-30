# ClaudeStack Basic Usage Examples

This guide shows you how to use ClaudeStack for common development tasks.

## Prerequisites

1. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Example 1: Building a Simple Web App

### Step 1: Start ClaudeStack
```bash
python launcher.py
```

### Step 2: Request a Plan
Create a file `inbox/chat.md` with:
```markdown
I want to build a simple todo app with Python Flask. It should have:
- Add new todos
- Mark todos as complete
- Delete todos
- Simple web interface
```

### Step 3: Follow the Agent Flow
ClaudeStack will automatically:
1. **Claude-Chat** receives your request
2. **Router** directs it to **Claude-Planner**
3. **Claude-Planner** creates an implementation plan
4. **Claude-Tasker** breaks it into specific tasks
5. **Claude-Coder** implements each component
6. **Claude-Reviewer** reviews the code

## Example 2: Code Review Request

Create `inbox/chat.md` with:
```markdown
Please review this Python function for security issues:

```python
def process_user_input(user_data):
    query = f"SELECT * FROM users WHERE name = '{user_data['name']}'"
    return execute_query(query)
```
```

The router will send this to **Claude-Reviewer** for analysis.

## Example 3: Getting Help

Create `inbox/chat.md` with:
```markdown
Can you explain the difference between async/await and threading in Python?
When should I use each approach?
```

This will be routed to **Claude-Helper** for explanation.

## Example 4: UI Design Request

Create `inbox/chat.md` with:
```markdown
Design a user-friendly interface for a expense tracking app. 
Users need to:
- Add expenses with categories
- View spending by month
- Set budget limits
- Get spending alerts
```

This will be routed to **Claude-Designer** for UI/UX planning.

## Monitoring Agent Activity

### Check Logs
```bash
tail -f logs/messages.log
```

### View Agent Outputs
```bash
# Check what the planner created
cat outbox/planner.md

# Check coder output
cat outbox/coder.md

# Check reviewer feedback
cat outbox/reviewer.md
```

## Running Individual Agents

You can also run agents individually:

```bash
# Run just the coder agent
python agents/agent_runner.py --agent coder

# Run with custom polling interval
python agents/agent_runner.py --agent helper --poll-interval 5
```

## Tips for Better Results

1. **Be Specific**: The more details you provide, the better the output
2. **Use Keywords**: Include relevant keywords to help routing
3. **Break Down Complex Requests**: Large projects work better when broken into phases
4. **Review Outputs**: Always check agent outputs in the `outbox/` directory
5. **Iterate**: Use agent feedback to refine your requests

## Common Workflows

### Full Stack Development
```
User Request → Planner → Tasker → Coder → Reviewer → Tester
```

### Code Review
```
Code Snippet → Reviewer → (Optional) Coder for fixes
```

### Learning & Help
```
Question → Helper
```

### UI Development
```
Feature Request → Designer → Frontend → Reviewer
```

## Troubleshooting

### Agent Not Responding
- Check that the agent is running
- Verify your API key is set
- Check `logs/messages.log` for errors

### Wrong Agent Routing
- Review your request keywords
- Check `config/routing_rules.json`
- Use more specific language

### Poor Output Quality
- Provide more context in your request
- Try a different agent (e.g., use Planner before Coder)
- Check if you're using the right agent for the task

For more examples and advanced usage, check the other files in this `examples/` directory.