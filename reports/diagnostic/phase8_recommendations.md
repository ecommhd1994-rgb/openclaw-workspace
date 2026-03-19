# PHASE 8 — ACTIONABLE IMPROVEMENTS

**Generated:** 2026-03-19 19:29 UTC
**Prioritization:** Stability → Performance → Cost Reduction

---

## STABILITY FIXES

---

### FIX-1: Close Telegram Prompt Injection Attack Surface

| Property | Detail |
|----------|--------|
| **Problem** | `groupPolicy: "open"` + unsandboxed main agent + `exec.ask: "off"` = trivial RCE via Telegram group message |
| **Root Cause** | Any Telegram user who adds the bot to a group can send prompt injection that calls `exec` on the host with no approval required |
| **Severity** | CRITICAL |
| **Evidence** | Phase 6, FM-3; Phase 7, finding #4 |

**Exact Fix:**
```json
// config.patch
{
  "channels": {
    "telegram": {
      "groupPolicy": "allowlist"
    }
  }
}
```
Or, if open group access is intentional: add `@admin` commands to restrict group interactions, and inject a system-level input sanitization step for Telegram messages.

**Alternative (less safe):** Keep `open` but change `exec.ask` to `on-miss` so unapproved exec commands trigger approval rather than auto-denial.

**Expected Impact:** Eliminates the most severe attack vector in the system. Zero cost.

---

### FIX-2: Wire `allowAgents` Correctly

| Property | Detail |
|----------|--------|
| **Problem** | Main agent can only spawn `researcher`, not `local-ops`. AGENTS.md says "System operations → local-ops agent" — policy and config contradict |
| **Root Cause** | `agents.list[main].subagents.allowAgents` only lists `["researcher"]` |
| **Severity** | HIGH (operational — blocks a stated workflow) |
| **Evidence** | Phase 7, finding #3 |

**Exact Fix:**
```json
// config.patch
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "allowAgents": ["researcher", "local-ops"],
          "model": "minimax/MiniMax-M2.7"
        }
      }
    ]
  }
}
```

**Also update AGENTS.md** — either add `local-ops` to `allowAgents` OR remove the "System operations → local-ops" delegation rule if local-ops is only for cron-triggered isolated sessions.

**Expected Impact:** Enables the orchestration pattern described in AGENTS.md. No cost.

---

### FIX-3: Fix Compaction Threshold (Stop Premature Memory Flushes)

| Property | Detail |
|----------|--------|
| **Problem** | `softThresholdTokens: 32000` on a 200K context fires compaction at 16% context fill. This interrupts every moderately complex task |
| **Root Cause** | Value miscalibrated; 32K is appropriate for a 32K context window, not 200K |
| **Severity** | HIGH (performance — disrupts active work) |
| **Evidence** | Phase 7, finding #2; Phase 5 likely shows context churn |

**Exact Fix:**
```json
// config.patch
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 160000
        }
      }
    }
  }
}
```

`160000` = 80% of 200K context. Compaction fires at ~180K tokens (200K - 20K reserve), so 160K gives a comfortable 20K buffer before compaction triggers.

**Expected Impact:** Stops spurious memory flushes interrupting tasks. Reduces token churn. At ~3 flushes prevented per day × 1500 tokens per flush × $0.30/M output = negligible direct savings, but significant latency reduction.

---

### FIX-4: Investigate and Fix Stale Session Leak

| Property | Detail |
|----------|--------|
| **Problem** | 8 orphaned `local-ops` sessions from 6 days ago (2026-03-13) still in session store; `archiveAfterMinutes: 30` not being respected |
| **Root Cause** | Unknown — likely cron job for archive not running, or sessions not reaching `archiveAfterMinutes` threshold due to inactivity loop |
| **Severity** | MEDIUM (resource leak) |
| **Evidence** | Phase 6, FM-10 and stale session evidence |

**Action Steps:**
1. Run `sessions_list` to confirm current orphaned session count
2. Check cron job history: `cron(action=runs, jobId=<local-ops-cron-id>)` 
3. Verify session archive mechanism fires for `local-ops` sessions specifically
4. Manually clean up stale sessions via `sessions_delete` or process removal

**Manual cleanup:**
```bash
# List all sessions
openclaw sessions list

# Force-archive or delete stale ones
```

**Expected Impact:** Frees memory, reduces session store bloat. No direct cost but prevents eventual OOM from session accumulation.

---

### FIX-5: Activate Self-Improving-Agent Error Capture

| Property | Detail |
|----------|--------|
| **Problem** | `skills.entries.self-improvement.enabled: false` — error capturing is disabled; ERRORS.md files are empty templates |
| **Root Cause** | Skill explicitly disabled in config |
| **Severity** | MEDIUM (no failure learning loop) |
| **Evidence** | Phase 6: "no error logging", Phase 7: self-improvement skill disabled |

**Exact Fix:**
```json
// config.patch
{
  "skills": {
    "entries": {
      "self-improvement": {
        "enabled": true
      }
    }
  }
}
```

**Before enabling:** Verify the skill is actually installed at `~/.openclaw/workspace/skills/self-improving-agent/SKILL.md`. If not installed, install via clawhub or create the skill directory.

**Expected Impact:** Enables the system to learn from its own mistakes. Over time, reduces repeated failure patterns. Zero cost.

---

## PERFORMANCE FIXES

---

### FIX-6: Increase QMD Memory Retrieval Limits

| Property | Detail |
|----------|--------|
| **Problem** | `maxResults: 2`, `maxSnippetChars: 300` — only 600 chars of memory injected per search. Negligible for a 200K context |
| **Root Cause** | Limits set conservatively but too restrictive for the context window size |
| **Severity** | MEDIUM (memory system underutilized) |
| **Evidence** | Phase 7, finding #6 |

**Exact Fix:**
```json
// config.patch
{
  "memory": {
    "qmd": {
      "maxResults": 5,
      "maxSnippetChars": 600,
      "maxInjectedChars": 3000
    }
  }
}
```

`maxInjectedChars: 3000` with 5 results × 600 chars = 3000 chars max, matching the cap. This gives the agent meaningful memory context without overwhelming the prompt.

**Expected Impact:** Better context awareness for cross-session tasks. No token cost increase if the agent only retrieves what's relevant (semantic search filters). Negligible cost if context is already underutilized.

---

### FIX-7: Reduce Bootstrap Total Budget or Trim AGENTS.md

| Property | Detail |
|----------|--------|
| **Problem** | Core bootstrap files (6.6K chars) already consume 33% of `bootstrapTotalMaxChars: 20000` before session history |
| **Root Cause** | `AGENTS.md` is 4,294 chars — verbose for a system that should be lean |
| **Severity** | MEDIUM (risk of truncation under heavy session load) |
| **Evidence** | Phase 7, finding #7 |

**Option A — Increase budget (safer):**
```json
// config.patch
{
  "agents": {
    "defaults": {
      "bootstrapTotalMaxChars": 40000
    }
  }
}
```

**Option B — Trim AGENTS.md (preferred):**
Remove from AGENTS.md:
- Redundant sandbox rule (already in config)
- Tool limit rules (3 searches, 5 reads) that may be counterproductive
- Loop guard rule that tells the agent to "stop tool usage" instead of escalating
- Any sections that duplicate system config

Target: reduce AGENTS.md from 4,294 to ~2,500 chars.

**Expected Impact:** Prevents context truncation during complex sessions. Zero cost.

---

### FIX-8: Verify ZAI API Compatibility

| Property | Detail |
|----------|--------|
| **Problem** | ZAI provider uses `openai-completions` API for chat models (GLM-4.7). Completions API may not correctly handle multi-turn chat models |
| **Root Cause** | API type mismatch; chat-optimized models sent through a completion endpoint |
| **Severity** | MEDIUM (possible degraded output quality or silent failures) |
| **Evidence** | Phase 7, finding #8 |

**Action Steps:**
1. Run a test: spawn a subagent with `model: zai/glm-4.7` for a simple task and verify output quality
2. Check if ZAI provider supports a messages/chat endpoint — look at `https://api.z.ai/api/coding/paas/v4` docs
3. If a chat endpoint exists, update `providers.zai.api` to `"anthropic-messages"` or appropriate chat format

**Expected Impact:** If ZAI is used as fallback, correct API ensures reliable outputs. Zero cost to investigate.

---

## COST REDUCTION FIXES

---

### FIX-9: Set Correct ZAI Cost Values

| Property | Detail |
|----------|--------|
| **Problem** | All ZAI models show `$0` cost — entire ZAI spend is invisible to cost tracking |
| **Root Cause** | Config data entry error (costs set to 0 as placeholder) |
| **Severity** | HIGH (cost visibility failure — conflicts with "tracks token usage carefully") |
| **Evidence** | Phase 7, finding #1 |

**Action:** Determine actual ZAI pricing. If free tier: document as `$0` but explicitly mark as "free tier — no cost". If paid: set actual per-token rates.

```json
// Example (replace with actual ZAI pricing once known):
"zai/glm-4.7": {
  "cost": {
    "input": 0,
    "output": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  },
  "note": "free tier"
}
```

**Expected Impact:** Full cost visibility. If ZAI is actually paid, prevents bill shock. If free, provides confidence that cost tracking is accurate.

---

### FIX-10: Investigate Runtime Model Divergence

| Property | Detail |
|----------|--------|
| **Problem** | Default model is `MiniMax-M2.7` but runtime is `MiniMax-M2.5`. If M2.5 is more expensive than M2.7, this is a cost leak |
| **Root Cause** | Unknown — possible session override, alias resolution, or intentional |
| **Severity** | MEDIUM (cost uncertainty) |
| **Evidence** | Phase 7, finding #5 |

**Action:** 
1. Check session_status for current session model
2. Check if `Minimax` alias (which maps to M2.5) is being applied somewhere
3. If M2.5 costs more per token than M2.7, revert to M2.7 as runtime or confirm the switch is intentional

Current M2.5 and M2.7 have identical cost in config (`$0.30 input / $1.20 output`). If actual pricing is the same, this is low priority. If M2.7 is actually cheaper, switch back.

**Expected Impact:** Eliminates cost uncertainty on the primary runtime model.

---

## SUMMARY TABLE

| # | Fix | Severity | Effort | Stability | Performance | Cost |
|---|-----|----------|--------|-----------|-------------|------|
| 1 | Telegram groupPolicy → allowlist | CRITICAL | Low | ✅ | — | — |
| 2 | Add local-ops to allowAgents | HIGH | Low | ✅ | — | — |
| 3 | Compaction threshold 32K → 160K | HIGH | Low | ✅ | ✅ | — |
| 4 | Fix stale session leak | MEDIUM | Medium | ✅ | — | — |
| 5 | Enable self-improving-agent | MEDIUM | Low | ✅ | — | — |
| 6 | QMD limits 2×300 → 5×600 | MEDIUM | Low | — | ✅ | — |
| 7 | Bootstrap budget 20K → 40K | MEDIUM | Low | ✅ | ✅ | — |
| 8 | Verify ZAI API compatibility | MEDIUM | Medium | — | ✅ | — |
| 9 | Set correct ZAI costs | HIGH | Low | — | — | ✅ |
| 10 | Investigate M2.5 vs M2.7 runtime | MEDIUM | Low | — | — | ✅ |
| **11** | **Rotate weak gateway token "test123"** | **CRITICAL** | **Low** | **✅** | **—** | **—** |
| **12** | **Remove/fix github skill (env-harvest)** | **HIGH** | **Low** | **✅** | **—** | **—** |
| **13** | **Clean up stale Docker containers** | MEDIUM | Low | ✅ | ✅ | — |
| **14** | **Wire fallback model for main/researcher** | HIGH | Low | ✅ | — | — |
| **15** | **Disable elevated tools in subagent sandbox** | MEDIUM | Low | ✅ | — | — |

---

## DO NOT IMPLEMENT (risky without further investigation)

These were considered but **should not be changed** without further analysis:

- **`exec.ask: "off"` → `"on-miss"`** — While safer, changing this affects every exec call. Could break existing workflows. Defer until FIX-1 (groupPolicy) is evaluated.
- **`bootstrapMaxChars` reduction** — AGENTS.md is already near the limit; reducing it would cause truncation.
- **Removing local-ops agent** — It's dead code but removing it could break future cron job designs that rely on it.
- **Changing `tools.deny`** — Removing `group:web` deny could expose research agents to prompts that browse malicious sites.

---

### FIX-11: Change Weak Gateway Token

| Property | Detail |
|----------|--------|
| **Problem** | Gateway auth token is the 7-char string `"test123"` — trivially brute-forced given the rate limit (10 attempts/60s, 5min lockout means ~480 guesses/day) |
| **Root Cause** | Token set during initial setup, never rotated |
| **Severity** | **CRITICAL** |
| **Evidence** | Phase 1: "weak 7-char token ('test123')" |

**Exact Fix:**
```bash
# Generate a new secure token
openclaw gateway token generate
# OR manually:
openssl rand -hex 32

# Then patch:
gateway config.patch
{
  "gateway": {
    "auth": {
      "token": "<new-32-byte-hex-token>"
    }
  }
}
```

**Expected Impact:** Eliminates the most trivially exploitable vulnerability. Token exposure via config file still requires securing the config itself (filesystem permissions). After rotation, update any scripts/webhooks that store the old token.

---

### FIX-12: Remove or Fix GitHub Skill

| Property | Detail |
|----------|--------|
| **Problem** | Researcher agent lists `github` skill but it was not found in standard skill directories; if it doesn't exist the skill silently fails; if it does exist it has **env-harvesting patterns** (Phase 1, 4) |
| **Root Cause** | Skill declared in agent config but not verified as installed; security flaw in skill itself |
| **Severity** | **HIGH** (credential exfiltration risk) |
| **Evidence** | Phase 1: "github skill with env-harvesting patterns"; Phase 7: skill location unknown |

**Action Steps:**
1. Verify if `~/.openclaw/workspace/skills/github/` or `/usr/lib/node_modules/openclaw/skills/github/` exists
2. If exists: audit the skill's `SKILL.md` and scripts for `GITHUB_TOKEN`, `GH_TOKEN`, or other env var access patterns
3. If skill doesn't exist: remove from researcher agent `skills` array:
```json
// config.patch
{
  "agents": {
    "list": [
      {
        "id": "researcher",
        "skills": ["clawhub", "session-logs"]
      }
    ]
  }
}
```
4. If skill exists and is clean: keep it but monitor for unusual env access

**Expected Impact:** Removes credential exfiltration vector. Zero cost.

---

### FIX-13: Clean Up Stale Docker Containers

| Property | Detail |
|----------|--------|
| **Problem** | 4-day-old cron container + 29h-old `slug-generator` container still present; container lifecycle cleanup broken |
| **Root Cause** | Unknown — likely containers not tied to a cleanup hook, or cleanup cron job disabled |
| **Severity** | MEDIUM (resource leak, potential security exposure from old containers) |
| **Evidence** | Phase 4: "Stale containers — 4-day-old cron container + 29h slug-generator still running" |

**Immediate Action:**
```bash
# List all containers (including stopped)
docker ps -a

# Remove containers older than 24h
docker rm $(docker ps -a --format '{{.ID}} {{.CreatedAt}}' | awk '$2 < "'$(date -d '24 hours ago' -I)'" { print $1 }')

# Or remove by name pattern:
docker rm $(docker ps -a --format '{{.Names}}' | grep -E 'cron|slug-generator') 2>/dev/null

# Prune all stopped containers
docker container prune -f
```

**Root-Cause Fix:** Investigate why containers aren't being cleaned up — check if the cron job that spawns them has a corresponding cleanup step, or add a weekly `docker system prune` cron job.

**Expected Impact:** Frees disk space, removes potential attack surface from old container images. Zero cost.

---

### FIX-14: Wire Fallback Model for Main and Researcher

| Property | Detail |
|----------|--------|
| **Problem** | GLM-4.7-flash exists in config as fallback for `minimax/MiniMax-M2.7` but is not actually wired as a fallback in the agent definitions; Phase 6 confirmed no automatic fallback occurs |
| **Root Cause** | `agents.defaults.model.fallbacks` lists `zai/glm-4.7-flash` but this may only apply when the primary provider (MiniMax) is unreachable, not when the model itself is unavailable |
| **Severity** | HIGH (100% block when MiniMax API fails) |
| **Evidence** | Phase 2: "no fallback configured"; Phase 3: "No fallback if MiniMax API fails"; Phase 6, FM-1 |

**Verification:** Check if `agents.defaults.model.fallbacks` is actually honored at runtime by testing with a MiniMax API failure simulation. If the fallback doesn't fire:

```json
// config.patch — ensure fallback is explicitly set per agent
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "minimax/MiniMax-M2.7",
        "fallbacks": ["zai/glm-4.7-flash", "ollama/qwen3.5:0.8b"]
      }
    },
    "list": [
      {
        "id": "main",
        "model": "minimax/MiniMax-M2.7",
        "fallbackModel": "zai/glm-4.7-flash"
      },
      {
        "id": "researcher",
        "model": "minimax/MiniMax-M2.7",
        "fallbackModel": "zai/glm-4.7-flash"
      }
    ]
  }
}
```

**Expected Impact:** System stays operational during MiniMax API outages. Zero cost.

---

### FIX-15: Disable Elevated Tools in Subagent Sandbox

| Property | Detail |
|----------|--------|
| **Problem** | Subagent sandbox configures `tools.elevated=enabled` — this is an explicit escape hatch that defeats the purpose of sandboxing; if a subagent is compromised, elevated tools allow container escape to host |
| **Root Cause** | Default sandbox config includes elevated tool permission; not reviewed after initial setup |
| **Severity** | MEDIUM/HIGH (reduces sandbox isolation) |
| **Evidence** | Phase 4: "subagent sandbox is strong but they get workspaceAccess='rw' and tools.elevated=enabled (escape hatch)" |

**Verification:** Check if any subagent actually needs elevated tools. If not:
```json
// config.patch — remove elevated tool escape hatch
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "workspaceAccess": "rw",
        "scope": "session",
        "elevatedTools": false
      }
    }
  }
}
```

If some subagents genuinely need elevated tools (e.g., `systemctl` for service management), document which ones and restrict via per-agent sandbox config rather than a global default.

**Expected Impact:** Hardens sandbox isolation. Zero cost.

---

## AFTER APPLYING FIXES
