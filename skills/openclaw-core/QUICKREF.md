# OpenClaw Core Quick Reference

## Routing Cheat Sheet

| Request Type | Agent | Examples |
|--------------|-------|----------|
| Code/Debug | Forge | "Fix this bug", "Write a function", "Debug error" |
| Research/Info | Researcher | "How does X work?", "Compare A vs B", "Explain Y" |
| Documentation | Writer | "Write README", "Create guide", "Document API" |

## Controller Pattern

```markdown
1. Understand task
2. Break into steps
3. For each step:
   - Ask Router: "Route to: [task description]"
   - Delegate to <agent>
4. Combine results
```

## Token Limits

| Agent | Max Tokens | Reasoning |
|-------|-----------|-----------|
| Forge | 2000 | Debugging only |
| Researcher | 1500 | Minimal |
| Writer | 2000 | Minimal |
| Router | 50 | None |

## Forge Safety

- Max 3 files per task
- Max 2000 lines per file
- Patch-style edits only
- No full repo scans

## Commands

```
/openclaw-core route <task>  # Manual routing test
/new                          # Reset session
```

## Workspaces

- Forge: `/openclaw/agents/forge/workspace/`
- Researcher: None (no file access)
- Writer: None (no file access)

## Memory Policy

Store ONLY when:
- Reusable pattern discovered
- Persistent decision made
- User feedback indicates value

---

**Fast. Safe. Efficient.**
