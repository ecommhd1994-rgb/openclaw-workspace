# AGENTS.md - Your Workspace

## Every Session

1. Read `SOUL.md` — identity
2. Read `USER.md` — who you're helping
3. Read `FOCUS.md` — session focus rules
4. Read `memory/YYYY-MM-DD.md` (today + yesterday) — recent context
5. **MAIN SESSION ONLY**: Also read `MEMORY.md`

## Memory Architecture

### Hierarchy
- **Working**: `memory/YYYY-MM-DD.md` — Raw session notes
- **Project**: `projects/*.md` — Architecture & design
- **Infrastructure**: `infrastructure/*.md` — Server config, ports, runbooks
- **Incidents**: `incidents/debugging.md` — Solved bugs, fixes
- **Core**: `MEMORY.md` — Permanent truths, preferences

### MEMORY.md Rules
- **MAIN SESSION ONLY** — Do not load in shared contexts (security)
- Read, edit, update freely in main sessions
- Write: significant events, decisions, opinions, lessons learned

### Write It Down
- "Remember this" → `memory/YYYY-MM-DD.md`
- Learned lesson → AGENTS.md, TOOLS.md, or skill SKILL.md
- Made a mistake → Document it

### Promotion Rule
`memory/` → `projects/` / `infrastructure/` / `incidents/` → `MEMORY.md`

### Loop Protection
If same task fails 3×:
1. Stop retrying
2. Mark as **BLOCKED**
3. Write to `incidents/debugging.md`
4. Ask for guidance

## Token Efficiency Rules

**Default: search memory before reading files.**

1. Never load files unless required for the task.
2. Always attempt `memory_search` before reading memory files.
3. Use `memory_get` only when a specific section is needed.
4. Avoid loading entire files when only small sections are needed.
5. Large files (>300 lines) must never be automatically loaded.
6. Prefer summaries over full documents.
7. If unsure whether a file is needed, ask before loading it.

**Example workflow:**
1. Understand the task
2. Use `memory_search`
3. Retrieve snippet with `memory_get`
4. Only read full files if absolutely necessary

## Safety
- No private data exfiltration
- Destructive commands? Ask first
- `trash` > `rm`
- When in doubt, ask

## Make It Yours
This is a starting point. Add conventions as you figure things out.
