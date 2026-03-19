# PHASE 2 — ARCHITECTURE ANALYSIS

**Generated:** 2026-03-19 19:08 UTC  
**Based on:** Phase 1 system inventory

---

## 1. COMPONENT MAP

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HOST (Linux 6.8)                            │
│                                                                     │
│  ┌──────────────────────┐      ┌──────────────────────────────┐    │
│  │  Gateway (pid 242243) │      │  ollama (pid 864)            │    │
│  │  openclaw-gateway     │      │  qwen3.5:0.8b @ localhost:11434│   │
│  │  :18789 (LAN bind)    │──────│                              │    │
│  │  WS→node process     │      └──────────────────────────────┘    │
│  │  Token: "test123"     │                                          │
│  │  controlUI: localhost  │      ┌──────────────────────────────┐    │
│  └──────────────────────┘      │  Docker Engine (pid 1094)    │    │
│          │                     │  /var/run/docker.sock        │    │
│          │                     │  3 active containers:        │    │
│          ▼                     │  • openclaw-sbx-agent-main-*  │    │
│  ┌──────────────────────┐      │  • openclaw-sbx-temp-slug-* │    │
│  │  Node.js process      │      │  • openclaw-sbx-agent-main-  │    │
│  │  /usr/lib/node_modul  │      │    cron-*                    │    │
│  │  /es/openclaw/dist    │      │                              │    │
│  └──────────────────────┘      └──────────────────────────────┘    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Workspace (/)                                                 │  │
│  │  ├── /root/.openclaw/workspace (main)                         │  │
│  │  │   ├── agents/main/  →  main agent (Jarvis)                 │  │
│  │  │   ├── agents/local-ops/ → local-ops agent                  │  │
│  │  │   ├── skills/                                           │  │
│  │  │   └── memory/ (345 files, QMD-indexed)                   │  │
│  │  └── /root/.openclaw/workspace-researcher (researcher)       │  │
│  │       └── isolated from main workspace                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  External APIs                                                │  │
│  │  • MiniMax API (minimax.ai) — main + researcher agents      │  │
│  │  • Telegram Bot API — channel integration                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. INTERACTION FLOWS

### Flow A: User → Gateway → Agent → Tools → Host/Container

```
Telegram/webchat → Gateway (:18789) → Agent (main) → Tool exec
                                                    ├── sandbox OFF (main agent, non-main mode)
                                                    └── sandbox ON  (subagent sessions)
```

**Path:**
1. Message arrives at `channels.telegram` plugin
2. Gateway routes to `main` agent session
3. Agent decides: native tools vs LLM call
4. LLM call → MiniMax API (external)
5. Tool call → `tools.exec.host="gateway"` → runs on host OR in Docker container

### Flow B: Cron → local-ops Agent → Ollama (local LLM)

```
Cron scheduler → local-ops agent → ollama (localhost:11434)
                               └── qwen3.5:0.8b (0.8B params, 1024 max tokens)
```

**Path:**
1. Cron job fires (every 60m heartbeat)
2. Spawns `agent:local-ops:cron:*` session
3. Uses `ollama/qwen3.5:0.8b` model (local, no API cost)
4. Executes lightweight tasks (heartbeat ack)

### Flow C: Deep Research → main → researcher Agent

```
main agent → sessions_spawn (researcher) → workspace-researcher
                                             ├── MiniMax API (MiniMax-M2.7)
                                             └── outputs: reports/, sources/, notes/
```

**Path:**
1. main determines task needs research
2. `sessions_spawn(runtime="subagent", agentId="researcher")`
3. Researcher gets isolated workspace
4. Researcher writes output files
5. main reads and summarizes

### Flow D: Memory → QMD (local search)

```
Agent → memory_search → QMD index → /root/.openclaw/workspace/memory
```

**Path:**
1. `memory_search` tool invoked
2. QMD backend searches 7 indexed paths
3. Returns top 2 results (maxInjectedChars: 1200)
4. Injected into agent context

---

## 3. BOTTLENECKS

| Bottleneck | Location | Severity | Evidence |
|------------|----------|----------|----------|
| **Single LLM API dependency** | MiniMax API | HIGH | Both main + researcher route through MiniMax; no redundancy |
| **Local Ollama CPU-bound** | AMD EPYC 9354P | MEDIUM | qwen3.5:0.8b runs on CPU; 2 cores allocated; slow generation (~10 tokens/s) |
| **Gateway token auth** | Gateway :18789 | HIGH | 7-char token "test123" — trivial to brute-force |
| **200k context + MiniMax-M2.7** | LLM layer | MEDIUM | Full context scans consume significant latency budget |
| **QMD index update interval** | memory backend | LOW | 10-minute reindex lag; new memory files not immediately searchable |
| **No CDN/caching for static assets** | Control UI | LOW | Dashboard served directly from gateway |

---

## 4. TIGHT COUPLING

| Coupling | Type | Risk |
|----------|------|------|
| **Gateway ↔ node process** | Process-level | If node process dies, gateway (systemd) restarts it; recovery is automatic |
| **Gateway ↔ Docker** | Socket-level | Docker socket exposed to host; gateway container (if any) shares docker.sock access |
| **Main agent ↔ MiniMax API** | Network + model | If MiniMax is down, main + researcher are fully blocked |
| **local-ops ↔ Ollama** | localhost:11434 | If Ollama crashes, heartbeat/cron tasks fail silently |
| **Agent configs ↔ JSON files** | File-level | Config hot-reloads on write; no atomicity guarantee |
| **Skills ↔ workspace files** | Path coupling | Skills reference absolute paths; workspace move breaks them |

---

## 5. FAILURE PROPAGATION PATHS

### Path 1: MiniMax API Outage
```
MiniMax down
  → main agent: ALL requests fail (100% blocked)
  → researcher agent: ALL requests fail (100% blocked)
  → Telegram channel: bot stops responding
  → No graceful degradation (no fallback model configured for these agents)
```

### Path 2: Ollama Crash
```
Ollama down (localhost:11434)
  → local-ops agent: heartbeat/cron tasks fail
  → Tool call timeouts in local-ops sessions
  → Cron jobs: marked failed but not retried automatically
  → main agent: unaffected
```

### Path 3: Docker Failure
```
Docker daemon crash
  → All sandboxed subagent sessions: terminated
  → tools.exec: fails for sandboxed sessions
  → tools.process: fails for sandboxed sessions
  → Gateway continues (host-level tools still work)
```

### Path 4: Disk Full
```
Disk 100%
  → writes fail (workspace, memory, logs)
  → agent sessions crash on write attempts
  → Docker containers: unable to write logs
  → OpenClaw compacted state may be lost
```

### Path 5: Telegram Token Leak
```
Bot token exposed
  → Any group can reconfigure groupPolicy
  → Attacker controls bot behavior in open groups
  → With open groupPolicy + elevated tools: full system compromise
```

### Path 6: Prompt Injection (Telegram Open Group)
```
Malicious message in Telegram group
  → Bot responds (mention-gated but open groupPolicy)
  → Prompt injection in message content
  → Tool execution triggered (exec, write, edit)
  → Because main agent runs unsandboxed: direct host access
  → Workspace files modified
```

---

## 6. ARCHITECTURAL OBSERVATIONS

### Strengths

1. **Separated workspaces**: main and researcher have isolated workspaces — researcher can't corrupt main's files
2. **Sandbox containers**: 3 containers active; subagent isolation works when triggered
3. **Local LLM for cron**: qwen3.5:0.8b via Ollama saves API costs for lightweight tasks
4. **Memory indexing**: QMD provides fast semantic search across 7 path sources
5. **Systemd-managed gateway**: gateway survives process death via systemd restart policy

### Weaknesses

1. **non-main sandbox mode means main agent is unsandboxed** — the single biggest architectural risk
2. **No model redundancy** — both main and researcher depend solely on MiniMax-M2.7
3. **Control UI bound to localhost only** — no remote dashboard access on a VPS
4. **Docker socket exposed** — any container breakout can control Docker daemon
5. **Gateway bind = LAN** — accessible on LAN but the VPS public IP has no firewall blocking 18789 (only localhost restricted)
6. **Weak gateway token** — 7-char "test123" is trivial for brute force

---

## 7. DATA FLOW DIAGRAM

```
External:
  Telegram ──► Gateway :18789 ──► Plugin: telegram
                              │
                              ▼
                    ┌─────────────────┐
                    │  Session Router │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         agent:main    agent:local-ops  agent:researcher
              │              │              │
              ▼              ▼              ▼
         MiniMax        Ollama         MiniMax
         API            localhost      API
              │              │              │
              ▼              ▼              ▼
         Tool Layer     Tool Layer     Tool Layer
         (UNSANDBOXED)  (sandboxed)   (sandboxed)
              │              │              │
              ▼              ▼              ▼
         Host FS/       Docker        Docker
         Docker socket  Container     Container
```

---

## 8. PHASE 2 SUMMARY

- **Single points of failure**: MiniMax API, Ollama, Docker daemon, Gateway token
- **Critical path**: Telegram → Gateway → main agent → MiniMax → tools (unsandboxed)
- **Tight coupling**: Gateway↔Docker, main↔MiniMax, local-ops↔Ollama
- **Failure propagation**: MiniMax outage = total bot failure; prompt injection in Telegram open group = direct host access via unsandboxed main agent
- **No redundancy**: No fallback LLM, no backup gateway, no Docker HA
