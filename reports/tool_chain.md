# OpenClaw Architecture — 3 Key Points

**Source:** `/root/.openclaw/workspace/docs/architecture.md`  
**Extracted:** 2026-03-19 20:56 UTC

---

## Key Point 1 — Memory Hierarchy (5-Tier System)

OpenClaw uses a 5-tier memory hierarchy with clear promotion rules:
1. **Working** — `memory/YYYY-MM-DD.md` — raw session notes
2. **Project** — `projects/*.md` — architecture & design docs
3. **Infrastructure** — `infrastructure/*.md` — server config, ports, runbooks
4. **Incidents** — `incidents/debugging.md` — solved bugs and fixes
5. **Core** — `MEMORY.md` — permanent truths and preferences

Promotion follows: memory/ → projects/ / infrastructure/ / incidents/ → MEMORY.md

---

## Key Point 2 — Loop Protection (3-Strike Block)

When the same task fails 3 times consecutively:
1. Stop retrying
2. Mark as **BLOCKED**
3. Write to `incidents/debugging.md`
4. Ask for human guidance

This prevents infinite retry loops and ensures failures are documented.

---

## Key Point 3 — MEMORY.md Isolation Rule

`MEMORY.md` is designated **MAIN SESSION ONLY** — it must not be loaded in shared or subagent contexts. This prevents:
- Cross-session memory contamination
- Subagent prompt pollution from long-term memory
- Premature context saturation from persistent data

Only the main orchestrator agent reads and writes permanent truths to MEMORY.md.

---

*Tool chain: exec (find) → read (doc) → extract (3 points) → write (file) — all successful, no retries*
