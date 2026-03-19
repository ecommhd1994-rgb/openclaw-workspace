# PHASE 4 — TOOLING & SANDBOX ANALYSIS

**Generated:** 2026-03-19 19:14 UTC

---

## 1. TOOL ACCESS MATRIX

### Global Tool Denylist
```json
"tools.deny": ["group:web", "browser"]
```
| Tool/Group | Status | Impact |
|------------|--------|--------|
| `group:web` | DENIED | All agents blocked from web search, web fetch |
| `browser` | DENIED | No browser automation |

**Effect:** No agent can access the internet. Researcher cannot do web research.

### Per-Tool Settings
```json
"tools.exec": { "host": "gateway", "security": "full", "ask": "off" }
```
| Setting | Value | Implication |
|---------|-------|-------------|
| `exec.host` | `"gateway"` | Exec runs on gateway process |
| `exec.security` | `"full"` | No exec restrictions — any command allowed |
| `exec.ask` | `"off"` | **Zero approval required for ANY exec command** |
| `tools.elevated` | enabled | Elevated exec escape hatch to host |

---

## 2. SANDBOX ANALYSIS

### Sandbox Configuration
```json
"agents.defaults.sandbox": {
  "mode": "non-main",      // main=host, non-main=sandboxed
  "workspaceAccess": "rw",  // read-write workspace mount
  "scope": "session"        // one container per session
}
```

### Active Containers
| Container | Age | Network | Workspace Mount |
|-----------|-----|---------|-----------------|
| `openclaw-sbx-agent-main-subagent-*` | 19h | `none` | `/root/.openclaw/workspace` → `/workspace` (rw) |
| `openclaw-sbx-temp-slug-generator-*` | 29h | `none` | (unknown) |
| `openclaw-sbx-agent-main-cron-*` | 4 days | `none` | `/root/.openclaw/workspace` → `/workspace` (rw) |

### Container Isolation Properties
| Property | Value | Safe? |
|----------|-------|-------|
| Network | `none` (no network) | ✅ Yes |
| Capabilities | None added | ✅ Yes |
| Workspace mount | rw bind mount | ⚠️ Can write to host filesystem |
| Propagation | `rprivate` | ✅ Prevents escape |

---

## 3. CRITICAL FINDING: MAIN AGENT IS UNSANDBOXED

`sandbox.mode = "non-main"` means:
- **`main` agent:** runs on **host** (no container) with full exec/fs/process access
- **All non-main sessions** (subagents, cron, group chats): sandboxed in Docker

### The Problem
```
main agent (UNSANDBOXED)
  ├── exec → runs on host (gateway process)
  ├── process → runs on host
  ├── read/write/edit → operates directly on host filesystem
  ├── Docker socket → accessible (gateway host has /var/run/docker.sock)
  └── tools.elevated → enabled → can escape container

sandboxed subagent (SANDBOXED)
  ├── exec → runs in Docker container (isolated)
  ├── network → none (fully isolated)
  └── workspace → bind mount to host (but contained)
```

**The main agent is the most capable AND the least sandboxed.**

---

## 4. APPROVAL FRICTION ANALYSIS

### Current: `tools.exec.ask = "off"`
| Risk | Severity | Evidence |
|------|----------|----------|
| No approval for destructive commands | CRITICAL | `rm -rf`, `dd`, `fdisk` all execute without prompt |
| No approval for network exfiltration | CRITICAL | `curl`, `wget` to external servers work without approval |
| No approval for credential access | CRITICAL |读取 tokens, keys from env/files |
| tools.elevated.enabled | CRITICAL | Escape hatch from sandbox to host |

### Approval Modes Available
| Mode | Behavior |
|------|----------|
| `off` | No approval, all exec runs immediately |
| `on-miss` | Approve only if no prior approval exists |
| `always` | Always ask for approval |

**Current setting:** `ask: "off"` — all exec commands run without any approval step.

---

## 5. FILE SYSTEM CONSTRAINTS

### Current: `tools.fs.workspaceOnly = false` (not explicitly set)

| Path | main agent | Sandboxed subagent |
|------|-----------|-------------------|
| `/root/.openclaw/workspace` | rw | rw (bind mount) |
| `/root/.openclaw/workspace-researcher` | rw | no access (different workspace) |
| `/root/.openclaw/agents/*` | rw | unknown |
| `/root/.openclaw/cron` | rw | unknown |
| `/etc` | rw (blocked by OS perms) | blocked |
| `/proc` | partially blocked | blocked |
| `/var/run/docker.sock` | rw (gateway host) | blocked by container |

### FS Risk in Open Groups
With `groupPolicy="open"` and `tools.fs.workspaceOnly=false`:
1. Telegram message triggers a tool call
2. If routed to main agent (unsandboxed): full workspace access
3. Malicious actor could: `write` to `~/.ssh/authorized_keys`, modify cron, inject agents

---

## 6. TOOL ROUTING INEFFICIENCIES

### Issue 1: `exec.host = "gateway"` for ALL tools
```
All exec calls route to gateway host
  → No differentiation between "safe read-only" and "dangerous write"
  → No per-command security filtering
```

### Issue 2: No tool profiles
OpenClaw supports tool profiles (e.g., `tools.profile: "messaging"`) to restrict tool subsets per context.
- Not configured anywhere
- Open Telegram group has the same tool access as DM

### Issue 3: Loop detection is reactive, not preventive
```
historySize=20, warning@6, critical@12, circuitBreaker@20
  → Model can make 6+ bad tool calls before warning
  → 12+ bad calls before critical alert
  → 20+ before circuit breaker fires
  → All at cost of wasted tokens + API calls
```

### Issue 4: `exec.security = "full"` with no restrictions
```
No allowlist of permitted commands
No denylist of dangerous commands
No path restrictions on exec
No parameter sanitization enforced
```

---

## 7. SANDOX EFFECTIVENESS ASSESSMENT

### What Works
| Feature | Status |
|---------|--------|
| Container per session | ✅ Working (3 containers active) |
| Network isolation | ✅ `none` — no container can reach network |
| Filesystem isolation via bind mount | ✅ `rprivate` propagation |
| Dangerous path blocking (docker.sock, /etc, /proc, /sys, /dev) | ✅ Blocked |

### What Doesn't Work
| Feature | Status |
|---------|--------|
| Main agent sandboxing | ❌ Runs on host, completely outside containers |
| Exec approval | ❌ `ask: "off"` — zero friction |
| Tool routing by context | ❌ All tools available in all contexts |
| Workspace-only FS for non-main | ❌ `workspaceOnly=false` — full workspace exposed |
| exec.security allowlist | ❌ `"full"` — no restrictions |

### Overall Sandbox Effectiveness: **WEAK**
- **For subagents/cron:** Strong (network=none, filesystem contained)
- **For main agent:** Non-existent (no sandbox, full host access)
- **Combined with open Telegram group:** HIGH RISK

---

## 8. DETECTED ISSUES

### CRITICAL
1. **Main agent unsandboxed + open Telegram group** = trivial remote code execution via message
2. **exec.ask="off"** = any successful prompt injection runs immediately
3. **tools.elevated=enabled** = sandboxed subagent can escape to host via elevated exec
4. **No exec security filtering** = no protection against `rm -rf`, `dd`, credential exfil

### HIGH
5. **tools.fs.workspaceOnly=false** = subagent can write anywhere in workspace including SSH keys, cron, agents
6. **sandbox.workspaceAccess="rw"** = even sandboxed containers have full read-write workspace access
7. **exec.host="gateway"** = all exec runs on host, no safe/sandboxed split

### MEDIUM
8. **Loop detection is reactive** = 6-12 bad tool calls before warning, wastes tokens
9. **denyCommands ineffective** = wrong command names (calendar.add instead of calendar.event.add), miss targeting
10. **No tool profiles** = messaging context gets same tools as admin context

### LOW
11. **Stale containers** — cron container 4 days old, slug-generator 29h old (should be cleaned up)
12. **No container resource limits** — no CPU/memory caps on sandbox containers

---

## PHASE 4 SUMMARY

- **Sandbox works well for subagents** (network=none, contained FS, private propagation) but **main agent runs completely outside the sandbox** on host with full exec/fs/process access
- **Zero exec approval friction** (`ask="off"`) means any prompt injection that tricks the model immediately executes — no human-in-the-loop
- **Combined risk:** open Telegram group + unsandboxed main agent + no exec approval = trivially exploitable remote code execution path from any Telegram message
- **tools.elevated=enabled** is an additional escape hatch that bypasses sandbox for "elevated" operations — not reviewed/approved per-agent
- **Stale containers** (4-day-old cron container) suggest cleanup gaps in container lifecycle management
