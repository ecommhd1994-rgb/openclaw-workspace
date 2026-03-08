# OpenClaw Core — Multi-Agent System

**Optimized multi-agent system for efficient task routing, minimal token usage, and safe execution.**

## Architecture

```
User
 ↓
OpenClaw Controller (Planner)
 ↓
Router (Classifier)
 ↓
Specialized Agents
```

## Components

### 1. OpenClaw Controller

**Role:** Task orchestration and planning

**Responsibilities:**
- Understand user requests
- Break tasks into steps
- Delegate tasks to sub-agents
- Combine final outputs

**Rules:**
- Do NOT perform coding tasks directly
- Do NOT perform research directly
- Do NOT generate long outputs
- Do NOT access repository files

**Always delegate** specialized tasks to the appropriate sub-agent.

### 2. Router

**Role:** Ultra-fast task classification

**Routing Logic:**
- Source code, stack traces, filenames, debugging → **Forge**
- Factual info, technical explanations, docs lookup → **Researcher**
- Documentation, guides, README, formatted content → **Writer**

**Rules:**
- Produce minimal output (only agent name)
- No reasoning or explanation
- Fast classification

### 3. Forge (Coding Agent)

**Role:** Safe and efficient code assistance

**Capabilities:**
- Writing code
- Code reviews
- Debugging
- Code explanation
- Small repository edits

**Model:** `zai/glm-4.7` (reasoning only for debugging)

**Workspace:** `/openclaw/agents/forge/workspace/`

**Repository Safety:**
- Max 3 files per task
- Max 2000 lines per file
- No full repository scans
- Patch-style edits only

### 4. Researcher (Information Agent)

**Role:** Technical and informational research

**Capabilities:**
- Technical explanations
- API references
- Architecture comparisons
- Documentation summaries

**Model:** Fast default model

**Rules:**
- Concise summaries
- Structured outputs
- No repository access

### 5. Writer (Documentation Agent)

**Role:** Structured writing and documentation

**Capabilities:**
- Documentation
- README files
- Guides
- Structured explanations

**Model:** Default model

**Rules:**
- Concise writing
- Clear formatting
- No external research

## Token Safety Rules

All agents follow these limits:
- Avoid long reasoning chains
- Keep outputs concise
- Summarize if output exceeds token limits
- Never repeat large blocks of text unnecessarily

## Repository Protection

- No full repository scans
- No recursive directory analysis
- Limit context size
- Limit number of loaded files

## Usage

### Controller Workflow

1. Receive user request
2. Break down into steps
3. For each step, ask Router to classify
4. Delegate to appropriate specialized agent
5. Collect results
6. Combine into final response

### Example Request

**User:** "Debug the authentication bug and document the fix"

**Controller Process:**
1. Step 1: Understand the bug → Researcher
2. Step 2: Fix the code → Forge
3. Step 3: Write documentation → Writer
4. Combine results → Final response

## Workspaces

- **Forge:** `/openclaw/agents/forge/workspace/` (isolated coding workspace)
- **Researcher:** No workspace (no file access)
- **Writer:** No workspace (no file access)

## Installation

1. Clone or copy this skill directory to OpenClaw workspace skills
2. Enable the skill in OpenClaw settings
3. Controller will automatically route to specialized agents

## Memory Policy

Each agent stores memory only when:
- A reusable pattern is discovered
- A persistent decision is made
- User feedback indicates value

## Cost Optimization

- Routing is ultra-fast (minimal tokens)
- Specialized agents use minimal reasoning
- Context isolation prevents token bloat
- Patch-style edits reduce output size

## Final Objective

OpenClaw Core provides:
- Efficient task routing
- Minimal token usage
- Safe repository operations
- Scalable multi-agent collaboration
