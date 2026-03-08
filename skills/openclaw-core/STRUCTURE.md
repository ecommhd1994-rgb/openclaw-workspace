# OpenClaw Core System Structure

```
openclaw-core/
├── SKILL.md              # Main Controller behavior
├── README.md             # System overview
├── INTEGRATION.md        # Setup and configuration guide
├── QUICKREF.md           # Quick reference card
├── STRUCTURE.md          # This file
├── router/
│   └── SKILL.md         # Router agent behavior
├── forge/
│   └── SKILL.md         # Forge (coding) agent behavior
├── researcher/
│   └── SKILL.md         # Researcher agent behavior
└── writer/
    └── SKILL.md         # Writer agent behavior
```

## Workspaces

```
/openclaw/agents/forge/workspace/
└── (isolated coding workspace)
```

## Agent Responsibilities

### Controller (Main Agent)
- Planning and orchestration
- Delegation to sub-agents
- Result combination

### Router
- Task classification
- Ultra-fast routing
- No execution

### Forge
- Coding and debugging
- Repository operations
- Patch-style edits

### Researcher
- Information lookup
- Technical explanations
- Concise summaries

### Writer
- Documentation
- Guides
- Structured content

## Data Flow

```
User Request
    ↓
Controller (understand, plan)
    ↓
Router (classify)
    ↓
Specialized Agent (execute)
    ↓
Controller (combine)
    ↓
Final Response
```

## Token Budget

Per session:

| Agent | Input | Output | Reasoning |
|-------|-------|--------|-----------|
| Controller | Variable | Minimal | Planning |
| Router | < 100 | < 50 | None |
| Forge | Task-specific | ≤ 2000 | Debug only |
| Researcher | Task-specific | ≤ 1500 | Minimal |
| Writer | Task-specific | ≤ 2000 | Minimal |

## Memory Storage

Each agent stores memory when:
- Reusable patterns discovered
- Persistent decisions made
- User feedback received

## Config Files

Main config: `~/.openclaw/openclaw.json`

```json5
{
  skills: {
    entries: {
      "openclaw-core": {
        enabled: true,
        path: "~/.openclaw/workspace/skills/openclaw-core",
      },
    },
  },
  agents: {
    defaults: {
      forgeWorkspace: "/openclaw/agents/forge/workspace",
    },
  },
}
```

## Environment

- Linux server (no GPU)
- Default model: `glm-4.7-flash`
- Coding model: `zai/glm-4.7`
- Cache retention: 24h

## Status

- ✅ Skills created
- ✅ Workspaces prepared
- ✅ Documentation complete
- ⏳ Integration pending (user action needed)
- ⏳ Testing pending (after integration)

---

**System ready for deployment.**
