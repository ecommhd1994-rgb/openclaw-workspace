# Workspace Architecture

## Memory Hierarchy

| Type | Location | Purpose |
|------|----------|---------|
| Working | memory/YYYY-MM-DD.md | Raw session notes |
| Project | projects/*.md | Architecture & design |
| Infrastructure | infrastructure/*.md | Server config, ports, runbooks |
| Incidents | incidents/debugging.md | Solved bugs, fixes |
| Core | MEMORY.md | Permanent truths, preferences |

## MEMORY.md Rules

- **MAIN SESSION ONLY** — Do not load in shared contexts
- Read, edit, update freely in main sessions
- Write: significant events, decisions, opinions, lessons learned

## Promotion Rule

memory/ → projects/ / infrastructure/ / incidents/ → MEMORY.md

## Loop Protection

If same task fails 3×:
1. Stop retrying
2. Mark as **BLOCKED**
3. Write to incidents/debugging.md
4. Ask for guidance

## Research Output Storage

```
reports/YYYY-MM-DD-topic-summary.md
```

Never store research reports in memory files.
