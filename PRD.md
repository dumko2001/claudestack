🧠 ClaudeStack PRD – v1.0

🚀 Project Title:
ClaudeStack – A Terminal-First, Multi-Agent AI Dev Framework Using Claude

🧭 Overview

ClaudeStack is an open-source, terminal-native framework that lets developers interact with multiple specialized Claude AI agents through a single interface. Each agent runs in its own terminal window and performs a distinct role in the software development lifecycle.

No servers, no databases, no dashboards — just smart agent routing, local file-based communication, and raw Claude power.

💡 Key Features

✅ Single Chat Interface – Talk to one Claude (Claude-Chat) and get routed intelligently.
✅ Multi-Agent System – Each Claude instance runs in a terminal and handles a single responsibility.
✅ Zero Infra – No DB, no backend, no frontend required. All communication is done through shared inbox/ and outbox/ folders.
✅ Model-Specific Roles – Different Claude models (Sonnet/Opus) are assigned to agents based on complexity.
✅ Expandable Design – Add/remove/replace agents easily.
🧩 Agents (Full List)

Agent Name	Model	Role Description
Claude-Chat	Sonnet-4	Main user interface — interprets your input and routes it
Claude-Planner	Opus-4	Breaks down high-level feature requests into a dev plan
Claude-Tasker	Sonnet-4	Converts plans into atomic development tasks
Claude-Coder	Sonnet-4	Implements code based on specific tasks
Claude-Reviewer	Opus-4	Reviews written code and gives feedback
Claude-Tester	Sonnet-4	Writes and runs tests, finds bugs, ensures stability
Claude-Designer	Opus-4	Generates UX/UI design specs, user flows, wireframes (via markdown description)
Claude-Frontend	Sonnet-4	Implements frontend UI components as per Designer or Tasker output
Claude-Helper	Sonnet-4	General-purpose support: codebase explanation, tech Q&A, tool advice
🔁 Agent Interaction Graph

         ┌────────────┐
         │Claude-Chat│◄────────── You talk here
         └─────┬──────┘
               ▼
        ┌─────────────┐
        │Claude-Planner│
        └─────┬────────┘
              ▼
       ┌─────────────┐
       │Claude-Tasker│
       └────┬─┬──────┘
            ▼ ▼
  ┌────────────┐ ┌─────────────┐
  │Claude-Designer│ │Claude-Coder │
  └────┬────────┘ └────┬────────┘
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│Claude-Frontend│ │Claude-Reviewer│
└──────┬────────┘ └────┬──────────┘
       ▼               ▼
               ┌─────────────┐
               │Claude-Tester│
               └─────────────┘
Designer talks to Frontend
Coder and Frontend both feed into Reviewer
Reviewer and Coder/Frontend feedback loop until approved
Tester ensures production-readiness
🗂 Directory Layout (File Protocol)

claudestack/
├── router.py                # Core router script
├── agents/
│   └── agent_runner.py      # Shared runner for all agents
├── inbox/
│   └── chat.txt             # You type here
│   └── planner.md           # Input to planner
│   └── tasker.md            # Input to tasker
│   └── coder.md             # Input to coder
│   └── reviewer.md          # Input to reviewer
│   └── tester.md            # Input to tester
│   └── designer.md          # Input to designer
│   └── frontend.md          # Input to frontend
│   └── helper.md            # Input to helper
├── outbox/
│   └── ... same structure   # Output from each agent
├── logs/
│   └── messages.log         # Chronological logs
└── config/
    └── model_assignments.json
⚙️ Terminal Setup (Example)

Launch Agents in separate terminal tabs:

python agent_runner.py --agent chat
python agent_runner.py --agent planner
python agent_runner.py --agent tasker
python agent_runner.py --agent designer
python agent_runner.py --agent coder
python agent_runner.py --agent frontend
python agent_runner.py --agent reviewer
python agent_runner.py --agent tester
python agent_runner.py --agent helper
Each agent polls their inbox/{agent}.md and writes output to outbox/{agent}.md

📑 Template Prompt Files

Each agent has a pre-loaded prompt like below.

📜 Claude-Planner Prompt Template
You are Claude-Planner, an expert in breaking down software feature requests into clear technical plans.

Input: A user request.
Output: A markdown plan with 2 sections:
- 📌 Objective
- 🛠 Implementation Plan (bullet points)

Be precise, include system boundaries and tooling when necessary.
📜 Claude-Tasker Prompt Template
You are Claude-Tasker. Your job is to convert planning docs into atomic developer tasks.

Input: Claude-Planner's plan.
Output: Markdown task list, formatted as:
- [ ] Task Name - short desc

Each task must be < 30 mins ideally.
📜 Claude-Coder Prompt Template
You are Claude-Coder. You write clean, efficient code based on task descriptions.

Input: One specific task.
Output: Code only, well-commented.
📜 Claude-Designer Prompt Template
You are Claude-Designer, a UI/UX architect.

Input: Feature plan or spec.
Output:
- Wireframe in markdown (ASCII or explanation)
- UX Notes
- Component list for Frontend

Keep it simple and dev-friendly.
📜 Claude-Frontend Prompt Template
You are Claude-Frontend. You implement UI components as per the Designer or Tasker’s spec.

Input: UI component descriptions or wireframe
Output: React (or framework-free) HTML/CSS/JS code
🚨 Routing Logic (router.py)

Router reads from inbox/chat.txt and uses Claude-Chat to classify intent:

Intent Type	Routed To
Feature request	Planner → Tasker → Coder/Designer
UI/UX question	Designer or Helper
General code Q	Helper
Bug fix	Coder → Reviewer → Tester
Code review request	Reviewer
Test writing	Tester
Each routing step updates logs/messages.log.

🧰 Optional: Automate Terminal Launch

Use Python to open terminal windows (macOS/Linux):

import os
os.system("gnome-terminal -- bash -c 'python agent_runner.py --agent planner'")
# Repeat for other agents
(Windows requires a PowerShell script or subprocess.Popen with new consoles.)

🏁 Deliverables

 claudestack/ repo
 Fully working local system with at least 3 agents (MVP: chat → planner → coder)
 Templates for all agents
 Simple README
 MIT License
 Quickstart CLI script
🪓 Dev Handoff Summary

“Hey dev, build me this system: it runs multiple Claude agents in terminal windows. Each one watches its own input file, sends it to Claude with a pre-written prompt, and writes the result. The router decides which agent should act next based on user intent. No database, no web server, just raw file-based coordination. Start with Chat → Planner → Coder → Reviewer. I want the base working in 3 days.”
