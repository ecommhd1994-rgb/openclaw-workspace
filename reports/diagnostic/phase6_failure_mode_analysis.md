# PHASE 6 — FAILURE MODE ANALYSIS

**Generated:** 2026-03-19 19:18 UTC

---

## 1. DOCUMENTED FAILURE PATTERNS

### From incidents/debugging.md

| Issue | Date | Status | Root Cause | Impact |
|-------|------|--------|-----------|--------|
| Docker build log token bloat | 2026-03-09 | RESOLVED | `docker build` logs flooded context with 2.7M tokens | $0.80 unexpected charge |
| Mission Control frontend/backend isolation | 2026-03-09 | OPEN | `network_mode` Docker config issue | MC deployment blocked |

### From .learnings/ERRORS.md
- **Empty** — template only, no actual errors logged
- Pattern: self-improving-agent is installed but errors are not being actively captured

### From incidents/ERRORS.md
- **Empty** — template only, no actual errors logged
- Pattern: incident logging not actively used

---

## 2. SESSION FAILURE EVIDENCE

### Stale Sessions (local-ops)
- **8 sessions** from 6 days ago (2026-03-13) still in session store
- All show `model: qwen3.5:0.8b`, `totalTokens: unknown` or `6.8k/33k (21%)`
- Sessions not cleaned up → likely cron job ran but sessions were orphaned
- **Pattern:** local-ops sessions not being properly archived

### Session Files in various states
| State | Count | Implication |
|-------|-------|-------------|
| `.reset` | 3 | Session was reset mid-operation |
| `.deleted` | 4 | Session manually deleted |
| `sessions.json` | 1 (active) | Current session store |

---

## 3. FAILURE MODE TABLE

### FM-1: MiniMax API Outage
| Property | Value |
|----------|-------|
| **Root cause** | External API downtime or network routing failure |
| **Reproduction** | MiniMax API returns 5xx or times out |
| **Severity** | CRITICAL |
| **Frequency** | Unknown (no historical data in this system) |
| **Detection** | Bot stops responding in Telegram/webchat |
| **Impact** | 100% of agents blocked — main, researcher, local-ops (if Ollama also down) |
| **Mitigation** | No fallback configured; GLM-4.7-flash exists but not wired as fallback |

### FM-2: Ollama Crash / Unreachable
| Property | Value |
|----------|-------|
| **Root cause** | Ollama process death, port 11434 blocked, or model unloaded |
| **Reproduction** | `curl localhost:11434` fails |
| **Severity** | MEDIUM |
| **Frequency** | Unknown |
| **Detection** | local-ops cron jobs fail; heartbeat fails silently |
| **Impact** | Heartbeat disabled (cron `enabled: false`); local-ops effectively offline |
| **Mitigation** | Cron job disabled; heartbeat has no delivery |

### FM-3: Prompt Injection (Telegram Open Group)
| Property | Value |
|----------|-------|
| **Root cause** | Malicious message in Telegram group with crafted instructions |
| **Reproduction** | Any group member sends message with embedded prompt injection |
| **Severity** | **CRITICAL** |
| **Frequency** | Unknown; open groupPolicy increases exposure |
| **Detection** | Unexpected file writes, exec calls in gateway logs |
| **Impact** | With main agent unsandboxed: direct RCE on host via `exec` tool |
| **Mitigation** | None currently; `exec.ask=off`, no input sanitization |

### FM-4: Token Bloat (Recurrence of FM from 2026-03-09)
| Property | Value |
|----------|-------|
| **Root cause** | Large command outputs (docker build, long logs) injected into context |
| **Reproduction** | Run `docker build` or similar without output truncation |
| **Severity** | HIGH |
| **Frequency** | Documented once (Mar 9); pattern may recur |
| **Detection** | Session token count spikes; unexpected API charges |
| **Impact** | $0.80+ per incident; context pollution |
| **Mitigation** | `tail -20` pattern documented in incidents/debugging.md |

### FM-5: Docker Daemon Failure
| Property | Value |
|----------|-------|
| **Root cause** | Docker crash, OOM kill, or `/var/run/docker.sock` inaccessible |
| **Reproduction** | `docker ps` fails |
| **Severity** | HIGH |
| **Frequency** | Unknown |
| **Detection** | Sandbox tool calls fail; containers show "exited" |
| **Impact** | All sandboxed subagent sessions terminate; tool execution fails for sandboxed tools |
| **Mitigation** | Gateway survives (runs on host); non-sandboxed tools continue |

### FM-6: Gateway Process Crash / OOM
| Property | Value |
|----------|-------|
| **Root cause** | OOM kill, segfault, or upstream dependency failure |
| **Reproduction** | OpenClaw node process dies |
| **Severity** | CRITICAL |
| **Frequency** | Unknown |
| **Detection** | Systemd restarts gateway; `openclaw status` shows gateway down |
| **Impact** | All agents offline; Telegram bot unreachable |
| **Mitigation** | Systemd restart policy; recent session data in session store |

### FM-7: Disk Full
| Property | Value |
|----------|-------|
| **Root cause** | Session logs, memory files, or Docker containers fill disk |
| **Reproduction** | `df -h /` shows 100% |
| **Severity** | HIGH |
| **Frequency** | Unknown |
| **Detection** | Write operations fail with ENOSPC |
| **Impact** | Agent crashes on write attempts; session state loss |
| **Mitigation** | 62GB free (36% used); session rotation at 10MB; ample headroom |

### FM-8: Session Store Corruption
| Property | Value |
|----------|-------|
| **Root cause** | Concurrent writes to sessions.json, or crash during write |
| **Reproduction** | sessions.json becomes invalid JSON |
| **Severity** | HIGH |
| **Frequency** | Unknown |
| **Detection** | Agent fails to load sessions; `sessions_list` errors |
| **Impact** | Session history lost; active sessions may be orphaned |
| **Mitigation** | Session rotation creates .jsonl files; maintenance prune at 30d |

### FM-9: Config Reload Race Condition
| Property | Value |
|----------|-------|
| **Root cause** | Config written while agent is processing a request |
| **Reproduction** | `gateway config.patch` during active session |
| **Severity** | MEDIUM |
| **Frequency** | Unknown |
| **Detection** | Unexpected behavior after config change; no atomicity guarantee |
| **Impact** | Inconsistent state between config and running agent |
| **Mitigation** | None documented; config hot-reloads without session restart |

### FM-10: Local-Ops Cron Job Timeout / Orphaning
| Property | Value |
|----------|-------|
| **Root cause** | Ollama too slow (124s for health check) causes cron job to timeout |
| **Reproduction** | Every local-ops cron run with current Ollama config |
| **Severity** | MEDIUM |
| **Frequency** | **100%** — cron job disabled due to this |
| **Detection** | Cron job lastRunStatus: would show timeout |
| **Impact** | local-ops agent never completes tasks; 8 stale sessions |
| **Mitigation** | Cron job disabled; no remediation attempted |

---

## 4. FAILURE PROPAGATION GRAPH

```
MiniMax API outage
  └── main agent: BLOCKED
  └── researcher agent: BLOCKED
  └── Telegram: NO RESPONSE
  └── local-ops: UNAFFECTED (uses Ollama)

Ollama crash
  └── local-ops: BLOCKED
  └── heartbeat: FAILS SILENTLY
  └── main agent: UNAFFECTED

Docker daemon crash
  └── sandboxed subagents: TERMINATED
  └── sandboxed tools: FAIL
  └── main agent: UNAFFECTED (host tools)
  └── gateway: UNAFFECTED

Gateway crash
  └── ALL AGENTS: OFFLINE
  └── Telegram: BOT UNREACHABLE
  └── [Systemd restarts gateway]

Disk full
  └── writes: FAIL
  └── sessions: CORRUPT
  └── Docker: STOPS
```

---

## 5. MISSING FAILURE INFRASTRUCTURE

| Missing | Impact |
|---------|--------|
| **No error logging** | ERRORS.md and .learnings/ERRORS.md are empty templates — failures not tracked |
| **No alerting** | No webhook/Slack/Telegram alerts for failures |
| **No health endpoint** | No /health or /ready endpoint probed |
| **No retry logic** | Failed cron jobs not retried; no dead letter queue |
| **No fallback model** | MiniMax is sole API provider with no automatic fallback |
| **Stale session leak** | 8 local-ops sessions from 6 days ago not cleaned up |

---

## 6. SECURITY FAILURE MODES (from Phase 4 context)

| Mode | Severity | Trigger | Impact |
|------|----------|---------|--------|
| Prompt injection in open group | **CRITICAL** | Telegram message | RCE via unsandboxed main agent |
| Gateway token brute force | **CRITICAL** | 7-char "test123" token | Unauthorized gateway access |
| Elevated tool abuse | **CRITICAL** | tools.elevated=enabled | Sandbox escape |
| github skill env-harvest | **HIGH** | Use github skill | Credentials exfiltrated |

---

## PHASE 6 SUMMARY

- **Most likely failure:** Token bloat recurrence (operational risk) and local-ops Ollama slowness (already disabled cron job)
- **Most severe failure:** MiniMax API outage (100% block) and prompt injection (RCE via unsandboxed main agent)
- **No failure tracking infrastructure** — ERRORS.md files are empty templates; self-improving-agent skill not actively capturing failures
- **8 stale local-ops sessions** from 6 days ago = session cleanup not working properly
- **No alerting or retry logic** — failures are silent unless user notices; no dead letter queue, no fallback models
- **Documented incident (Mar 9)** was resolved but same pattern could recur since exec.ask=off and no output truncation enforcement
