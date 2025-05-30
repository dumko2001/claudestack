
---

# ✅ ClaudeStack Final Build Roadmap (v1.0 Open Source)

### Total Stages: 8

Each stage has clear, atomic subtasks. Follow it top to bottom.

---

## **STAGE 1: Project Scaffolding**

### 🎯 Goal: Set up the repo, folders, and base infra

```
claudestack/
├── agents/
├── inbox/
├── outbox/
├── logs/
├── config/
├── router.py
├── launcher.py
├── README.md
```

### 🔧 Tasks:

* [ ] Create Git repo: `claudestack`
* [ ] Create folders: `agents/`, `inbox/`, `outbox/`, `logs/`, `config/`
* [ ] Create empty placeholders:

  * `router.py` (for routing logic)
  * `launcher.py` (for auto-terminal launch)
  * `README.md` (for final docs)

---

## **STAGE 2: Define Agent Prompt Templates**

### 🎯 Goal: Lock prompts for consistent, scoped agent behavior

### 🔧 Tasks:

* [ ] Create `prompts/` folder
* [ ] Write prompt templates for all agents:

  * [ ] Claude-Chat
  * [ ] Claude-Planner
  * [ ] Claude-Tasker
  * [ ] Claude-Coder
  * [ ] Claude-Reviewer
  * [ ] Claude-Tester
  * [ ] Claude-Designer
  * [ ] Claude-Frontend
  * [ ] Claude-Helper
* [ ] Save each as `prompts/{agent_name}.txt`

---

## **STAGE 3: Build Core Agent Runner**

### 🎯 Goal: Single Python script to run any agent with its prompt

### 🔧 Tasks:

* [ ] Create `agents/agent_runner.py`

* [ ] Implement:

  * [ ] `--agent` CLI arg (e.g. `--agent coder`)
  * [ ] Load corresponding `prompts/{agent}.txt`
  * [ ] Watch `inbox/{agent}.md` for new input
  * [ ] On new input:

    * Read prompt
    * Read user input
    * Call Claude via Anthropic API (pass in prompt + input)
    * Write output to `outbox/{agent}.md`
    * Log interaction to `logs/messages.log`

* [ ] Add polling delay (e.g. 2s) with `file_hash` change detection

* [ ] Add Claude model assignment via `config/model_assignments.json`

---

## **STAGE 4: Implement Claude-Chat + Router Logic**

### 🎯 Goal: Create a usable interface via `Claude-Chat`, auto-routing via `router.py`

### 🔧 Tasks:

* [ ] Claude-Chat:

  * Input: `inbox/chat.txt`
  * Output: write to `router.py` trigger or shared bus

* [ ] `router.py`:

  * [ ] Read latest message from `inbox/chat.txt`
  * [ ] Use Claude to classify intent
  * [ ] Based on intent, route message to correct inbox:

    * e.g., route to `inbox/planner.md`, `inbox/helper.md`, etc.
  * [ ] Log: `[timestamp] Routed user query to [agent]`

* [ ] Add routing schema in `config/routing_rules.json`:

  ```json
  {
    "feature_request": "planner",
    "code_question": "helper",
    "ui_request": "designer",
    ...
  }
  ```

---

## **STAGE 5: Implement Minimum Agent Flow (MVP)**

### 🎯 Goal: Chat → Planner → Tasker → Coder → Reviewer

### 🔧 Tasks:

* [ ] Implement input/output watcher for:

  * [ ] Claude-Planner
  * [ ] Claude-Tasker
  * [ ] Claude-Coder
  * [ ] Claude-Reviewer

* [ ] Automate flow:

  * Planner writes to outbox → Tasker picks it up
  * Tasker writes to outbox → Coder picks up one task
  * Coder writes to outbox → Reviewer reviews code
  * Reviewer feedback goes to `inbox/coder.md` again if needed

* [ ] Add basic file-level signaling to avoid race conditions:

  * Use `.lock` or `.done` markers if needed

---

## **STAGE 6: Add All Remaining Agents**

### 🎯 Goal: Integrate the rest of the team (Designer, Frontend, Tester, Helper)

### 🔧 Tasks:

* [ ] Claude-Designer:

  * Pulls from Planner or Tasker outputs
  * Outputs UX notes and wireframes

* [ ] Claude-Frontend:

  * Consumes Designer outputs
  * Writes HTML/CSS/JS to outbox

* [ ] Claude-Tester:

  * Consumes Coder output or Reviewer feedback
  * Writes tests and bug reports

* [ ] Claude-Helper:

  * Consumes any direct Q\&A or codebase questions

* [ ] Update `router.py` to include routing rules for these agents

* [ ] Update `logs/messages.log` to reflect these new paths

---

## **STAGE 7: Create Launcher Script (Auto-Terminal Launcher)**

### 🎯 Goal: Allow 1-click launch of all agents in separate terminals

### 🔧 Tasks:

* [ ] `launcher.py`:

  * Detect OS (macOS/Linux only for now)
  * Launch each `agent_runner.py --agent xxx` in a new terminal tab/window

    * For GNOME: `gnome-terminal -- bash -c 'python3 agent_runner.py --agent coder'`
    * For macOS: `osascript` or `iTerm` AppleScript

* [ ] Add optional agent flags:

  * `--exclude chat,tester` to skip launching specific agents

---

## **STAGE 8: Polish & Release**

### 🎯 Goal: Final docs, examples, and polish

### 🔧 Tasks:

* [ ] Add MIT License
* [ ] Write `README.md` with:

  * [ ] What it is
  * [ ] How to run
  * [ ] Agent overview diagram
  * [ ] How to extend
  * [ ] Example walkthrough
* [ ] Add `.gitignore` for `*.log`, `*.pyc`, `__pycache__/`, `inbox/`, `outbox/`
* [ ] Add `examples/` folder:

  * [ ] `examples/feature_request.md` – Chat input → full flow walkthrough
* [ ] Push to GitHub

---

## 🧠 Optional Stage 9 (Post-v1 Ideas — Do NOT Build Yet)

* [ ] Add CLI UI for `Claude-Chat` (rich console)
* [ ] Add YAML-based long memory/log linking
* [ ] Use SQLite for better indexing (if needed)
* [ ] Add "agent memory" folders per-agent

---

## 🏁 Final MVP Flow Example

```text
You → Claude-Chat → Claude-Planner → Claude-Tasker → Claude-Coder → Claude-Reviewer → Claude-Tester
                                        ↓
                                  Claude-Designer → Claude-Frontend
```

---

This task list is **complete, logically ordered, and optimized for dev handoff**. You’ll get a functional, extensible open-source system by the end of it — no major refactor needed.
