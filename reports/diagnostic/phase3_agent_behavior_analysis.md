# PHASE 3 — AGENT BEHAVIOR ANALYSIS

**Generated:** 2026-03-19 19:12 UTC

---

## 1. AGENT: main (Jarvis)

### Profile
- **Model:** MiniMax-M2.7 (200k ctx, reasoning enabled)
- **Sandbox:** `non-main` → runs UNSANDBOXED on host
- **Workspace:** `/root/.openclaw/workspace`
- **Current session tokens:** 31,490 total (input 24,230, output 53 in last turn)

### Task Completion Reliability
| Task Type | Reliability | Notes |
|-----------|-------------|-------|
| Conversational | HIGH | Concise, personality-driven, good judgment |
| Delegation to researcher | MEDIUM | Requires clean handoff, file-based coordination |
| Tool execution (exec/read/write) | HIGH | Direct host access, fast |
| Cron/heartbeat management | HIGH | Well-structured AUTOMATION.md |
| Deep research | LOW | Delegates to researcher; main just summarizes |
| Code generation | MEDIUM | No coding model directly configured |

### Timeout Risks
- **Context compaction:** `memoryFlush.softThresholdTokens=32000` → compaction triggers at ~32k tokens; with 200k context, large session can accumulate before compaction fires
- **Bootstrap files:** `bootstrapMaxChars=6000` per file, `bootstrapTotalMaxChars=20000` → all workspace context files (AGENTS.md, SOUL.md, USER.md, etc.) injected every session start
- **No timeout override for main** — uses `agents.defaults.timeoutSeconds=300` (5 min)

### Token Usage Patterns
- Current session: 24,230 input / 53 output (last turn) → very lean output
- Uses thinking blocks (visible in transcript) — adds token overhead
- Bootstrap injects 5-6 files at session start (~20k chars total)
- QMD memory search: `maxInjectedChars=1200` per result, `maxResults=2` → up to 2400 chars from memory per search

### Tool Usage Efficiency
- **Preferred order:** `read → search → write` (per AGENTS.md policy)
- **Limits enforced:** max 3 searches/task, max 5 reads/task, no consecutive duplicate tool calls
- **Loop detection:** warning@6, critical@12, circuit breaker@20
- **Exec ask:** OFF — no approval needed for any command
- **Issue:** AGENTS.md has loop guard rules but no enforced technical control — relies on model compliance

### Prompt Quality Issues
1. **No explicit `no_think` or token budget instruction** in main SOUL.md — model uses thinking blocks when it wants
2. **Bootstrap is heavy** — 6 workspace files + memory files injected every session start; no skip logic for small tasks
3. **AGENTS.md loop guard** is advisory only — no technical enforcement
4. **SANDBOX.md referenced in boot sequence** — file doesn't exist (GAVE me a file-not-found warning in boot)

### Detected Issues
- **Over-reading at boot:** Boot sequence reads SOUL.md, USER.md, then attempts memory/YYYY-MM-DD.md (today) and memory/YYYY-MM-DD.md (yesterday) — both fail silently (ENOENT). This is by design but generates log errors.
- **Research delegation:** AGENTS.md says "delegate research" but doesn't define WHAT the researcher should be told; relies on ad-hoc prompting
- **No explicit output length control** — model can be verbose when not needed

---

## 2. AGENT: local-ops

### Profile
- **Model:** `ollama/qwen3.5:0.8b` (0.8B params, 33k ctx, **1024 max tokens**)
- **Sandbox:** `non-main` → unsandboxed
- **Workspace:** `/root/.openclaw/workspace`
- **State:** DISABLED (cron job `enabled: false`)

### Task Completion Reliability
| Task Type | Reliability | Notes |
|-----------|-------------|-------|
| Simple health check ("HEALTH_OK") | MEDIUM | Works but model is extremely limited |
| Lightweight cron tasks | LOW | 1024 token max means no complex operations |
| Memory updates | LOW | Can't handle multi-step workflows |

### Timeout Risks
- **CRITICAL:** 1024 max tokens is below the `agents.defaults.heartbeat.prompt` character count — prompts can be truncated mid-execution
- **Ollama CPU-bound:** ~10 tokens/s generation on CPU-only host
- **Last cron run:** 124,762ms (2 min) for a simple health check — too slow for a "quick" task

### Token Usage Patterns
- **CRITICAL ISSUE:** `maxTokens: 1024` on a 33k context model means the model literally CANNOT use its full context
- Multiple stale sessions from 6 days ago showing "unknown/33k (?%)" — session tracking may be broken for this agent
- `maxTokens` config doesn't match actual model capability (ollama says 4k max for qwen3.5)

### Tool Usage Efficiency
- Limited to extremely simple read/write operations
- Cannot handle conditional logic well
- No loop detection applied to local-ops sessions

### Prompt Quality Issues
1. **Model too small for agentic tasks** — 0.8B model cannot reliably follow complex tool-use instructions
2. **Security audit flagged it:** "Small models require sandboxing" — but `sandbox=non-main` means it's unsandboxed
3. **No fallback model** — if Ollama is down, local-ops fails completely
4. **Heartbeat uses this model** when main agent's 60m heartbeat fires

### Detected Issues
- **Security + capability mismatch:** Small model with weak sandbox and no web tool access is acknowledged but not fixed
- **Cron job disabled but sessions exist** — 8 stale sessions from 6 days ago, all showing "unknown" token usage

---

## 3. AGENT: researcher

### Profile
- **Model:** MiniMax-M2.7 (200k ctx)
- **Sandbox:** `non-main` → sandboxed (subagent sessions)
- **Workspace:** `/root/.openclaw/workspace-researcher` (isolated from main)
- **Skills:** github, clawhub, session-logs

### Task Completion Reliability
| Task Type | Reliability | Notes |
|-----------|-------------|-------|
| Web research | N/A | `group:web` denied — no web access |
| File-based research | HIGH | Reads docs, sources, writes reports |
| Source gathering | MEDIUM | github skill exists but has security flaws |
| Report writing | HIGH | Clear output format in AGENTS.md |

### Timeout Risks
- **No specific timeout configured** — inherits `agents.defaults.timeoutSeconds=300`
- **Subagent runTimeout:** 600 seconds (10 min) — adequate for research tasks
- **Max concurrent subagents:** 3 — research tasks can run in parallel

### Token Usage Patterns
- Large context (200k) enables deep research
- Outputs to workspace files — no token limit concern for outputs
- AGENTS.md specifies: `reports/<topic>.md`, `sources/<topic>_sources.md`, `notes/<topic>_notes.md`

### Tool Usage Efficiency
- Skills: github (has env-harvesting vulnerability), clawhub, session-logs
- No web search — confined to local files and github API only
- Clear workflow: research → gather sources → write report → save files

### Prompt Quality Issues
1. **No web access** — research is limited to github and local files; cannot fetch external docs
2. **github skill security flaw** — env-harvesting pattern in `api.js:29` and `test.js:12`
3. **Researcher SOUL.md is generic** — not tailored to research task (similar to generic SOUL.md template)
4. **No explicit source validation** — AGENTS.md says "always cite sources" but doesn't specify quality criteria

### Detected Issues
- **Web tools disabled globally** — researcher cannot actually do comprehensive web research
- **github skill** with known security issues is the primary external data source
- **No model for local file summarization** — if MiniMax API fails, researcher has no fallback

---

## 4. CROSS-AGENT BEHAVIOR ISSUES

### Tool Loop Risk
- Loop detection: `historySize=20`, warning@6, critical@12, global@20
- AGENTS.md has manual loop guard rules but no technical enforcement — relies on model following instructions
- If model enters a read→search→read loop, only the global circuit breaker (20) will fire after significant token waste

### Delegation Breakdown
- main → researcher: file-based handoff (read reports from workspace-researcher)
- No status updates during researcher task — main must poll or wait
- If researcher crashes, main has no notification mechanism
- AGENTS.md says "wait for files" but no timeout or retry logic

### Prompt Injection Susceptibility
- main agent in Telegram open group: receives all messages
- No prompt injection detection — relies on model recognizing malicious instructions
- With unsandboxed main agent, successful injection = direct host access

### Context Management
- Compaction mode: "safeguard" with 20k token floor
- `memoryFlush` triggers at 32k tokens soft threshold
- No compaction for local-ops (its context is only 33k anyway)
- Bootstrap files injected every session regardless of task complexity

---

## 5. AGENT BEHAVIOR SUMMARY TABLE

| Aspect | main | local-ops | researcher |
|--------|------|-----------|------------|
| Model | MiniMax-M2.7 | qwen3.5:0.8b | MiniMax-M2.7 |
| Sandbox | **UNSANDBOXED** | **UNSANDBOXED** | sandboxed (subagent) |
| Reliability | HIGH | LOW | MEDIUM |
| Timeout risk | MEDIUM | CRITICAL | LOW |
| Token efficiency | GOOD | POOR | GOOD |
| Tool discipline | GOOD | POOR | MEDIUM |
| Biggest weakness | Prompt injection exposure | Model too small | No web access |

---

## PHASE 3 SUMMARY

- **main agent:** Reliable orchestrator but runs unsandboxed with exec/fs/process tools exposed — biggest attack surface; lightweight outputs, good delegation patterns
- **local-ops agent:** DISABLED but 8 stale sessions remain; qwen3.5:0.8b with 1024 max tokens is critically under-specced for agentic tool use; Ollama CPU bottleneck (~10 tkn/s)
- **researcher agent:** Good structure and isolation but cannot do real web research (web tools globally denied); github skill has known security flaw; no fallback if MiniMax fails
- **Systemic issues:** No technical loop enforcement, no approval for exec commands, prompt injection risk in open Telegram group with unsandboxed main agent
