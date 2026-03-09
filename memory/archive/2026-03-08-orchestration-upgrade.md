# Session: 2026-03-08 11:43:30 UTC

- **Session Key**: agent:main:main
- **Session ID**: 475b4a98-afcc-4466-9730-727af5daf39c
- **Source**: webchat

## Conversation Summary

user: A new session was started via /new or /reset. Execute your Session Startup sequence now - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
Current time: Sunday, March 8th, 2026 — 11:36 AM (UTC) / 2026-03-08 11:36 UTC
assistant: Hey Mohamad! Fresh session, ready to go. Using MiniMax-M2.5 this time. What do you need?

Model: minimax/MiniMax-M2.5 | Tokens: 82 → 47 | Cost: $0.001
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-03-08 11:37 UTC] Implement the final stable OpenClaw orchestration architecture using the pattern:

Router → Planner → Workers → Validator → Memory

This prompt upgrades the orchestration logic only.
Do NOT modify any system configuration files such as:

~/.openclaw/openclaw.json

The system must remain idle until a real user request is received.
No automatic tests, benchmarks, or background tasks may run.

---

SYSTEM ROLES

The orchestration system contains five roles:

Router
Planner
Workers
Validator
Memory Worker

The main agent performs Router and Planner responsibilities.

---

ROUTER

The Router receives the user request first.

Responsibilities:

• analyze request complexity
• determine whether workers are needed
• route the task appropriately

Routing rules:

If the request is simple (short explanation, basic answer):

→ respond directly without spawning workers.

If the request is complex:

→ forward the task to the Planner.

Simple requests must never trigger worker spawning.

---

PLANNER

The Planner prepares tasks for workers.

Responsibilities:

1. analyze the routed request
2. classify task type
3. generate a concise task brief
4. spawn appropriate workers

Task brief rules:

Maximum length: 120 words.

The brief must include:

• task objective
• minimal relevant context
• expected output format

The Planner must never forward the full conversation history.

Workers must receive ONLY the planner task brief.

---

WORKER TYPES

Workers must run as temporary sub-agents created using:

sessions_spawn

Worker roles:

Forge Worker
Used for coding, debugging, and development tasks.

Research Worker
Used for explanations, analysis, and technical research.

Writer Worker
Used for documentation and structured writing.

Spawn rules:

CODING → spawn Forge Worker
RESEARCH → spawn Research Worker
WRITING → spawn Writer Worker

If multiple capabilities are required, workers may run in parallel.

Maximum parallel workers: 3.

---

WORKER LIMITS

Workers must follow strict limits:

Maximum worker output: 400 words.

Workers must:

• avoid recursive directory scanning
• avoid reading entire repositories
• avoid repeating the planner brief
• avoid long reasoning chains unless required for debugging

Workers must terminate immediately after completing their task.

---

VALIDATOR

After workers complete their tasks, spawn a Validator.

Validator responsibilities:

• review worker outputs
• detect inconsistencies or errors
• merge relevant results
• produce the final response

Validator receives only:

• planner task brief
• worker outputs

Maximum validator output: 200 words.

Maximum validation cycles: 1.

---

MEMORY WORKER

After the final response is generated, spawn a Memory Worker.

Responsibilities:

• store useful results
• store reusable solutions
• store important insights

Memory entries must be concise summaries.

Memory Worker must store entries in:

~/.openclaw/workspace/memory/

Memory entry size limit: 100 words.

Memory must never store full conversations.

---

SESSION GUARD

The orchestration system must enforce strict safety limits:

Maximum parallel workers: 3
Maximum sub-agent depth: 2
Maximum validation cycles: 1
Maximum orchestration loops: 1

If any limit is reached:

Stop spawning agents and return the best available result.

---

TOKEN OPTIMIZATION RULES

To minimize token usage:

• workers receive only the planner brief
• conversation history is never forwarded
• validator receives only worker outputs
• workers terminate immediately after finishing tasks
• repeated orchestration loops are forbidden

---

EXECUTION FLOW

User Request
↓
Router analyzes request complexity
↓
If simple → respond directly
↓
If complex → Planner creates task brief
↓
Planner spawns workers
↓
Workers execute tasks and terminate
↓
Validator merges outputs
↓
Memory Worker stores useful insights
↓
Final response returned to user

---

ACTIVATION

The orchestration system activates only when a real user request requires task execution.

The system must remain idle otherwise.
assistant: Got it. This orchestration pattern is now active for complex tasks:

- **Router** (me) → assess complexity → simple = direct response, complex → Planner
- **Planner** → spawn Forge/Research/Writer workers (max 3 parallel)
- **Validator** → merge outputs (1 cycle max)
- **Memory Worker** → store insights (100 words max)

System stays idle until a real request comes in. What's up?

Model: minimax/MiniMax-M2.5 | Tokens: 120 → 89 | Cost: $0.001
assistant: agents:
-----
(none)
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-03-08 11:40 UTC] how to use my agents?
assistant: Quick guide:

**Spawn agents** using `sessions_spawn` with `runtime: "acp"` (for Codex/Claude Code) or `runtime: "subagent"` (for configured sub-agents).

**Common patterns:**
- `runtime: "acp", agentId: "codex"` — coding tasks
- `runtime: "acp", agentId: "claude-code"` — development
- `runtime: "subagent", agentId: <id>` — custom sub-agents

**Key flags:**
- `mode: "run"` — one-shot task
- `mode: "session"` — persistent thread
- `thread: true` — Discord/chat thread
- `pty: true` — terminal access (required for interactive CLIs)

Want me to spawn one for a specific task?

Model: minimax/MiniMax-M2.5 | Tokens: 132 → 98 | Cost: $0.001
