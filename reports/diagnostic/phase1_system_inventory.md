# PHASE 1 — SYSTEM INVENTORY

**Generated:** 2026-03-19 18:50 UTC  
**Scope:** Full OpenClaw deployment diagnostic

---

## 1. ACTIVE AGENTS

| ID | Name | Model | Context | Workspace | Role |
|----|------|-------|---------|-----------|------|
| `main` | Jarvis | `minimax/MiniMax-M2.7` | 200k | `/root/.openclaw/workspace` | Primary orchestrator |
| `local-ops` | Local Ops | `ollama/qwen3.5:0.8b` (0.8B) | 33k | `/root/.openclaw/workspace` | Cron/heartbeat tasks |
| `researcher` | researcher | `minimax/MiniMax-M2.7` | 200k | `/root/.openclaw/workspace-researcher` | Deep research delegation |

---

## 2. MODELS PER AGENT

| Agent | Model | Params | API | Max Tokens | Cache |
|-------|-------|--------|-----|------------|-------|
| main | MiniMax-M2.7 | ~200B? | minimax | 200k ctx | 24h retention |
| main (fallback) | GLM-4.7-flash | ~20B? | zai | 1500 max | 6h |
| local-ops | qwen3.5:0.8b | 0.8B | ollama (local) | 1024 | N/A |
| researcher | MiniMax-M2.7 | ~200B? | minimax | 200k ctx | 24h |

**Note:** `glm-4.7` model defined with `alias: "coding"`, `reasoning: "on"`, `maxTokens: 8000` — but no agent currently uses it directly.

---

## 3. TOOL ACCESS PER AGENT

| Tool Group | main | local-ops | researcher |
|------------|------|-----------|------------|
| `exec` | ✓ gateway/host | ✓ gateway/host | ✓ gateway/host |
| `process` | ✓ | ✓ | ✓ |
| `read` | ✓ | ✓ | ✓ |
| `write` | ✓ | ✓ | ✓ |
| `edit` | ✓ | ✓ | ✓ |
| `sessions_*` | ✓ | unknown | ✓ |
| `gateway` | ✓ | unknown | ✓ |
| `cron` | ✓ | unknown | unknown |
| `nodes` | ✓ (limited) | unknown | unknown |
| `browser` | DENIED | DENIED | DENIED |
| `group:web` | DENIED | DENIED | DENIED |

**Web tools globally denied** via `tools.deny: ["group:web", "browser"]`.

---

## 4. SANDBOX MODE

| Setting | Value | Implication |
|---------|-------|-------------|
| `agents.defaults.sandbox.mode` | `"non-main"` | Main agent runs on host; subagents/group sessions in containers |
| `agents.defaults.sandbox.workspaceAccess` | `"rw"` | Sandboxes get full read-write to workspace |
| `agents.defaults.sandbox.scope` | `"session"` | Each session gets own container |
| `tools.exec.host` | `"gateway"` | Exec tools target gateway/host |

**CRITICAL ISSUE:** `sandbox.mode="non-main"` but main agent has `exec/process` tools exposed on host. All agents (including main) have `sandbox=non-main` meaning they can run unsandboxed. No effective sandbox enforcement for the primary agent.

---

## 5. WORKSPACE STRUCTURE

```
/root/.openclaw/workspace/          # Main workspace (Jarvis)
├── agents/forge/                   # Agent forge templates
├── archive/                        # Archived files
├── clawbench/                      # Benchmarking tools
├── docs/                           # Local documentation
├── incidents/                      # Incident logs
├── infrastructure/                 # Infra configs
├── memory/                         # 345 files BM25-indexed
├── openclaw-config/                # Config source
├── openclaw-config.json            # ACTIVE CONFIG (11.7KB)
├── ops/                            # Operations scripts
├── projects/                       # Project files
├── promptinspector/                # Prompt inspection tools
├── reports/                        # Output reports
│   ├── diagnostic/                # THIS DIAGNOSTIC
│   └── existing analyses...
├── researcher/                     # Research agent workspace
├── skills/                         # Installed skills
│   ├── dory-memory/
│   ├── healthcheck.md
│   ├── openclaw-core/
│   ├── openclaw-github-assistant/  ⚠️ SECURITY FLAW (env harvesting)
│   ├── qmd-skill/
│   ├── self-improving-agent/
│   ├── session-logs/
│   ├── sonoscli/
│   └── supermemory/
└── state/                          # Runtime state

/root/.openclaw/workspace-researcher/ # Researcher workspace (isolated)
├── AGENTS.md, SOUL.md, IDENTITY.md
├── memory/, notes/, reports/, sources/
└── isolated from main workspace
```

---

## 6. KEY CONFIGURATIONS

### Approval & Security

| Setting | Value | Risk |
|---------|-------|------|
| `gateway.auth.mode` | `"token"` | Weak token (7 chars: "test123") |
| `gateway.auth.rateLimit.maxAttempts` | 10 | Low |
| `tools.exec.security` | `"full"` | No exec restrictions |
| `tools.exec.ask` | `"off"` | No approval required |
| `tools.elevated` | enabled | Dangerous with open groups |

### Telegram Channel

| Setting | Value | Risk |
|---------|-------|------|
| `channels.telegram.enabled` | true | Active |
| `channels.telegram.groupPolicy` | `"open"` | **CRITICAL** — any group can interact |
| `channels.telegram.dmPolicy` | `"pairing"` | OK |
| `channels.telegram.botToken` | present (len 46) | OK |

### Heartbeat

| Agent | Heartbeat | Model Used |
|-------|-----------|------------|
| main | 60m | ollama/qwen3.5:0.8b |
| local-ops | disabled | — |
| researcher | disabled | — |

### Concurrency

| Setting | Value |
|---------|-------|
| `agents.defaults.maxConcurrent` | 2 |
| `agents.defaults.subagents.maxConcurrent` | 3 |
| `agents.defaults.subagents.maxSpawnDepth` | 2 |
| `agents.defaults.subagents.runTimeoutSeconds` | 600 |

---

## 7. SECURITY AUDIT SUMMARY (from `openclaw security audit`)

| Severity | Count | Top Issues |
|----------|-------|------------|
| CRITICAL | 4 | Small model + weak sandbox; open groupPolicy + elevated tools; open groupPolicy + runtime/fs; Telegram open group |
| WARN | 3 | Short gateway token; ineffective denyCommands; multi-user heuristic |
| INFO | 1 | Attack surface summary |

---

## 8. ACTIVE SESSIONS (9 total)

| Session Key | Kind | Age | Model | Token Usage |
|-------------|------|-----|-------|-------------|
| agent:main:main | direct | just now | MiniMax-M2.7 | 13k/200k (7%) |
| agent:main:telegram:direct:* | direct | 29h ago | glm-4.7 | 16k/205k (8%) |
| agent:local-ops:cron:* | cron | 6d ago (×8) | qwen3.5:0.8b | 6.8k/33k or unknown |

---

## 9. SKILLS INSTALLED

| Skill | Path | Status |
|-------|------|--------|
| dory-memory | skills/dory-memory | Active |
| healthcheck | skills/healthcheck.md | Active |
| openclaw-core | skills/openclaw-core | Active |
| openclaw-github-assistant | skills/openclaw-github-assistant | ⚠️ **SECURITY FLAW** — env harvesting pattern |
| qmd-skill | skills/qmd-skill | Active (local search) |
| self-improving-agent | skills/self-improving-agent | Active |
| session-logs | skills/session-logs | Active |
| sonoscli | skills/sonoscli | Active |
| supermemory | skills/supermemory | Active |

---

## 10. HOST RESOURCES

| Resource | Value |
|----------|-------|
| CPU | AMD EPYC 9354P 32-Core (2 cores allocated to OpenClaw) |
| RAM Total | 7.8GB (~6.2GB available) |
| RAM Used | ~1.5GB |
| Disk | 96GB total, 62GB available (36% used) |
| Swap | None |
| GPU | None (CPU-only) |
| OS | Linux 6.8.0-106-generic x64 |

---

## PHASE 1 SUMMARY

- **Agents:** 3 configured (main, local-ops, researcher) — only main actively used
- **Models:** MiniMax-M2.7 for main/researcher, local qwen3.5:0.8b for local-ops/heartbeat
- **Sandbox:** `non-main` mode means main agent runs UNSANDBOXED on host with exec/fs tools
- **Critical risks:** 4 CRITICAL security issues (open Telegram group + elevated tools + runtime exposure; weak token; small model + weak sandbox)
- **Workspace:** Main workspace at `/root/.openclaw/workspace`, researcher isolated at `/root/.openclaw/workspace-researcher`
- **Skills:** 9 skills installed, 1 with known security flaw (openclaw-github-assistant)
