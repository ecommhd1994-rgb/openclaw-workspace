# PHASE 7 — CONFIGURATION AUDIT

**Generated:** 2026-03-19 19:25 UTC
**Auditor:** Jarvis (self-audit)
**Scope:** Prompts, agent definitions, model choices, security settings

---

## 1. PROMPT & DOCUMENT AUDIT

### 1.1 Bootstrap Budget vs. Actual Load

| File | Size (chars) |
|------|-------------|
| AGENTS.md | 4,294 |
| SOUL.md | 670 |
| MEMORY.md | 1,405 |
| IDENTITY.md | 136 |
| USER.md | 182 |
| **Core total** | **6,687** |

- `bootstrapMaxChars`: 6,000 per file
- `bootstrapTotalMaxChars`: 20,000 total
- `BOOTSTRAP.md`: missing (expected but absent — silently skipped)
- Memory files (today/yesterday): added on top

**Finding:** `AGENTS.md` alone (4,294 chars) exceeds `bootstrapMaxChars` (6,000) when considered as a single file entry. Total load of 6,687 chars already consumes 33% of the 20K budget before session history. The system likely truncates or handles this gracefully, but the margin is thin for complex sessions.

### 1.2 Prompt Quality Issues

**SOUL.md** — Good. Short, opinionated, clear boundaries. No issues.

**USER.md** — Good. Concise, action-oriented. Notes "Tracks token usage carefully" which implies cost sensitivity.

**AGENTS.md** — Has problems:
- Rule complexity: "Maximum searches per task: 3", "Maximum reads per task: 5" — these are arbitrary constraints that may cause the agent to stop prematurely or waste tokens debating whether it has exceeded limits.
- "Never call the same tool more than twice consecutively" — may prevent efficient tool chains (e.g., read→read→edit is common).
- Loop guard says "stop tool usage" — this is the wrong remediation for a stuck agent; it should escalate or signal, not silently halt.
- Redundant rules with actual system config (sandbox mode stated in AGENTS.md matches `agents.defaults.sandbox.mode`).

**IDENTITY.md** — Fine. Minimal.

### 1.3 Memory Flush Prompt

```
prompt: "Write a durable session note to memory/daily/YYYY-MM-DD.md. Capture only: decisions, architecture changes, debugging discoveries, open questions, and important constraints."
systemPrompt: "Be concise. Use bullet points. Do not copy the conversation."
```

**Issue:** The `systemPrompt` here is a generic instruction injected into the compaction agent's context. It may conflict with the agent's own SOUL.md persona. No explicit instruction to preserve Mohamad's name, timezone context, or current task state. The flush fires at `softThresholdTokens: 32000` but there's no hard guarantee the agent will actually produce useful output given the 1500 token cap on the daily model.

---

## 2. MODEL CONFIGURATION AUDIT

### 2.1 Cost Blind Spot — ZAI Models

```json
// All ZAI models have zero cost
"zai/glm-4.7":       { "cost": { "input": 0, "output": 0, ... } },
"zai/glm-4.7-flash": { "cost": { "input": 0, "output": 0, ... } },
"zai/glm-5":         { "cost": { "input": 0, "output": 0, ... } }
```

**Severity: HIGH**

USER.md says Mohamad "Tracks token usage carefully." With ZAI costs set to zero, the entire cost tracking system is blind to ZAI API spend. If ZAI is used as fallback or for subagents, spend is invisible. This directly conflicts with the user's stated priority.

### 2.2 Model Aliases — Redundancy & Inconsistency

```
agents.defaults.models:
  - "minimax/MiniMax-M2.5"    → alias: "Minimax"
  - "zai/glm-4.7"             → alias: "coding"
  - "zai/glm-4.7-flash"       → alias: "daily"
  - "ollama/qwen3.5:0.8b"    → alias: "local"
  - "minimax/MiniMax-M2.7"    → alias: "MiniMax-M2.7"  ← redundant, no different params
```

**Finding:** `MiniMax-M2.7` has an alias entry but no distinct params from the base definition. It's a no-op entry. The `coding` alias (glm-4.7) is defined but unused — no agent or task actually routes to it.

### 2.3 ZAI API Mismatch

- Provider `zai` uses `baseUrl: https://api.z.ai/api/coding/paas/v4`
- API type: `openai-completions`
- But GLM-4.7 / GLM-5 are chat models — they ship best with the messages/chat completions API
- The `coding` agent alias sets `maxTokens: 8000` but ZAI completions API may truncate or behave differently for chat-oriented models

**Unknown:** Whether ZAI actually works correctly with the completions API for GLM models. No failure has been reported, but this is an untested configuration.

### 2.4 Reasoning Parameter Inconsistency

| Model | `reasoning` in schema | Alias params |
|-------|----------------------|--------------|
| MiniMax-M2.5 | `true` | `{ cacheRetention: "24h" }` |
| MiniMax-M2.7 | `true` | `{ cacheRetention: "24h" }` |
| glm-4.7 | `true` | `{ reasoning: "on", maxTokens: 8000 }` |
| glm-4.7-flash | `true` | `{ reasoning: "low", maxTokens: 1500 }` |

**Finding:** ZAI models have `reasoning` explicitly set in alias params, but MiniMax models do not. If `reasoning` param is honored by the ZAI provider, this is fine. If it's ignored and only the schema-level `reasoning: true` is used, then the per-alias settings do nothing. **This is ambiguous — requires verification.**

### 2.5 Runtime vs. Default Model Divergence

- **Configured default:** `minimax/MiniMax-M2.7`
- **Current runtime:** `minimax/MiniMax-M2.5` (per session system prompt)
- **Fallback:** `zai/glm-4.7-flash`

No documentation explains why M2.5 is the active session model when M2.7 is the declared default. Possible causes: manual override, alias resolution, or a config inconsistency. **Not a problem if intentional, but undocumented.**

---

## 3. AGENT DEFINITION AUDIT

### 3.1 Main Agent (Jarvis)

```json
{
  "id": "main",
  "subagents": {
    "allowAgents": ["researcher"],
    "model": "minimax/MiniMax-M2.7"
  }
}
```

**Issue:** `allowAgents` restricts Jarvis to only spawn `researcher`. The AGENTS.md defines a "local-ops" agent, but the main agent cannot spawn it. This means the orchestrator cannot delegate system operations — a core stated responsibility in AGENTS.md ("System operations → local-ops agent"). Either:
1. `allowAgents` should include `local-ops`, or
2. The local-ops agent is intended for cron-triggered isolated sessions only (in which case the delegation rule in AGENTS.md is wrong).

### 3.2 Researcher Agent

```json
{
  "skills": ["github", "clawhub", "session-logs"]
}
```

**Unknown:** Whether these skills actually exist and are installed. The `clawhub` skill is confirmed at `/usr/lib/node_modules/openclaw/skills/clawhub/SKILL.md`. `session-logs` skill exists at `~/.openclaw/workspace/skills/session-logs/SKILL.md`. `github` skill location is **unknown** — not in the standard skills directory. If `github` skill is missing, the researcher agent may fail silently when trying to use it.

### 3.3 Local-Ops Agent

```json
{
  "id": "local-ops",
  "model": "ollama/qwen3.5:0.8b"
}
```

**Finding:** No `skills`, no `subagents`, no special tool grants. It's a bare agent entry. Since it can't be spawned by main (due to `allowAgents`), and no cron job references it explicitly, it appears **unused**. The heartbeat uses the local model directly without spawning an agent. This agent definition is dead code.

---

## 4. SECURITY SETTINGS AUDIT

### 4.1 Exec Tool Security

```json
"tools.exec": {
  "host": "gateway",
  "security": "full",
  "ask": "off"
}
```

- `security: "full"` — no allowlist restrictions on exec commands
- `ask: "off"` — no approval prompts for exec
- `host: "gateway"` — exec runs on the gateway host

**Assessment:** Appropriate for a non-shared VPS where the operator is the sole user. Would be dangerous on a shared system. Fine given current deployment model.

### 4.2 Gateway Bind

```json
"gateway": {
  "bind": "lan",
  "mode": "local"
}
```

- Binds to LAN interface, not public
- `controlUi.allowedOrigins`: only localhost
- `auth.mode`: token with rate limiting

**Assessment:** Good. Local-first with token auth. Rate limit (10 attempts per 60s, 5min lockout) is reasonable.

### 4.3 Node Device Permissions

```json
"nodes.denyCommands": [
  "camera.snap", "camera.clip", "screen.record",
  "calendar.add", "contacts.add", "reminders.add"
]
```

**Finding:** These commands are denied at the gateway level. However, `nodes` tool shows `camera_snap`, `camera_clip`, `screen_record` as available actions. The deny list may be applying to paired device nodes, not the local gateway node. **Consistency unclear** — the deny list and the available node actions don't obviously map to each other.

### 4.4 Tools Deny List

```json
"tools.deny": ["group:web", "browser"]
```

Web browsing tools are globally blocked. This is correct for a security-focused deployment. However, the `group:web` deny group may also block legitimate research tools if the researcher agent needs web access. Currently the researcher is used for docs/code investigation, not general web search, so this is not yet a problem.

---

## 5. SANDBOX CONFIGURATION AUDIT

### 5.1 Sandbox Mode

```json
"agents.defaults.sandbox": {
  "mode": "non-main",
  "workspaceAccess": "rw",
  "scope": "session"
}
```

- Main agent: no sandbox (outside sandbox)
- Subagents: sandboxed with read-write workspace access
- `scope: "session"` — sandbox limited to session lifetime

**Assessment:** Correct separation. Main agent runs on host, subagents isolated.

### 5.2 Workspace Path Inconsistency

```json
// Researcher workspace
"workspace": "/root/.openclaw/workspace-researcher"

// But AGENTS.md says:
// "Researcher workspace: ~/.openclaw/workspace-researcher"
// and "Workspace Separation Rule: Jarvis writes only inside main workspace"
```

The path uses an absolute path `/root/.openclaw/workspace-researcher` which is consistent. However, the `~` expansion in the `memory.qmd.paths` config items uses `~` which may not resolve consistently depending on where it's evaluated (node process vs shell).

**Minor issue:** The `memory.qmd.paths` entries use `~` while the agent workspaces use absolute paths. This inconsistency could cause memory search to miss files if `~` doesn't expand in the qmd context.

---

## 6. CHANNEL & SESSION CONFIGURATION

### 6.1 Telegram Configuration

```json
"channels.telegram": {
  "dmPolicy": "pairing",
  "groupPolicy": "open",
  "streaming": "off"
}
```

- `streaming: "off"` — responses delivered as single messages, not streamed
- `dmPolicy: "pairing"` — requires pairing for DMs
- `groupPolicy: "open"` — anyone in a group can interact

**Finding:** `groupPolicy: "open"` is a **risk**. Any Telegram user who adds the bot to a group can issue commands. Consider setting to `allowlist` or `admin` if group access is meant to be restricted. Current setting matches if Mohamad intentionally wants open group access.

### 6.2 Session Maintenance

```json
"session.maintenance": {
  "mode": "enforce",
  "pruneAfter": "30d",
  "maxEntries": 50,
  "rotateBytes": "10mb",
  "resetArchiveRetention": "14d"
}
```

**Assessment:** Aggressive but reasonable. 30-day retention, 50 entry cap, 10MB rotation. Good for a VPS with limited storage.

---

## 7. QMD MEMORY CONFIGURATION

```json
"memory.qmd": {
  "maxResults": 2,
  "maxSnippetChars": 300,
  "maxInjectedChars": 1200,
  "timeoutMs": 60000
}
```

**Finding:** These limits are very conservative.

- `maxResults: 2` — only 2 memory entries returned per search
- `maxSnippetChars: 300` — snippets are ~300 chars, barely enough for a sentence
- `maxInjectedChars: 1200` — with 2 results × 300 chars = 600 chars max from snippets, well under the 1200 cap
- `timeoutMs: 60000` — 60 second timeout is very high; indicates QMD can be slow

With a 200K token context window, injecting only 600 chars of memory context is minimal. The system will rely heavily on the bootstrap files and session history rather than semantic memory retrieval.

**Verdict:** QMD is configured for minimal memory injection. Fine if the agent is expected to work session-locally, but limits the benefit of the memory system.

---

## 8. COMPACTION CONFIGURATION

```json
"compaction": {
  "mode": "safeguard",
  "reserveTokensFloor": 20000,
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 32000
  }
}
```

- Compaction triggers at ~180K tokens (200K - 20K reserve)
- `softThresholdTokens: 32000` is the flush trigger, which is **very low** for a 200K context
- With MiniMax-M2.7's 200K context, 32K tokens is only 16% full — this means compaction fires extremely early

**Finding:** The `softThresholdTokens: 32000` seems miscalibrated. It should likely be 160,000 (80% of context) not 32,000. At current setting, the agent will attempt to flush memory every time context exceeds 32K tokens — potentially once per complex task. This could cause frequent, unnecessary memory flushes that interrupt work flow.

---

## 9. CONFIGURATION MISALIGNMENTS SUMMARY

| # | Issue | Severity | Type |
|---|-------|----------|------|
| 1 | ZAI costs set to zero — cost tracking blind | HIGH | Data |
| 2 | `compaction.softThresholdTokens: 32000` too low (should be ~160K) | HIGH | Config |
| 3 | Main agent `allowAgents: ["researcher"]` can't spawn local-ops | HIGH | Policy |
| 4 | `groupPolicy: "open"` on Telegram — uncontrolled group access | HIGH | Security |
| 5 | Researcher `skills: ["github"]` — skill may not exist | MEDIUM | Integrity |
| 6 | QMD `maxResults: 2`, `maxSnippetChars: 300` — very minimal memory | MEDIUM | Config |
| 7 | `bootstrapTotalMaxChars: 20000` with 6.6K+ already used by core files | MEDIUM | Capacity |
| 8 | ZAI completions API used for chat models (GLM) | MEDIUM | Compatibility |
| 9 | AGENTS.md tool limits (3 searches, 5 reads) may be counterproductive | MEDIUM | Prompt |
| 10 | Local-ops agent defined but never spawnable — dead code | LOW | Cleanup |
| 11 | `MiniMax-M2.7` model alias entry is redundant (no distinct params) | LOW | Cleanup |
| 12 | `~` path expansion in memory.qmd.paths may be inconsistent | LOW | Reliability |

---

## 10. KNOWN UNKNOWNS

- Whether `github` skill exists for the researcher agent
- Whether ZAI completions API works correctly for GLM-4.7 chat models
- Whether ZAI `reasoning` param in alias is actually honored by the provider
- Whether the bootstrap budget is actually truncating content or handling overflow gracefully
- Why the runtime model is M2.5 when default is M2.7
