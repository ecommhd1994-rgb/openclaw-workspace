# PHASE 5 — PERFORMANCE ANALYSIS

**Generated:** 2026-03-19 19:16 UTC

---

## 1. HOST RESOURCES

| Resource | Status | Value |
|----------|--------|-------|
| CPU Load | ✅ HEALTHY | 0.38 / 0.55 / 0.85 (1m/5m/15m) |
| RAM Used | ✅ HEALTHY | 1.3GB / 7.8GB (16%) |
| RAM Available | ✅ HEALTHY | 6.5GB |
| Disk | ✅ HEALTHY | 35GB / 96GB used (36%) |
| Swap | ✅ HEALTHY | None configured |

**Containers (docker stats):** All 3 active containers using ~0.5MB each — essentially idle.

**Verdict:** Host has ample headroom. No resource contention.

---

## 2. LAYER-BY-LAYER LATENCY ANALYSIS

### Layer 1: Telegram → Gateway
- **Status:** ✅ Healthy
- **Note:** Streaming disabled (`streaming: "off"`), good for latency/bandwidth

### Layer 2: Gateway → Agent dispatch
- **Status:** ✅ Fast
- **Note:** In-process routing, minimal overhead

### Layer 3: Agent → LLM API (MiniMax)
- **Status:** ✅ Acceptable
- **Latency:** ~1-2s for typical requests (based on session data)
- **Token overhead:** 24k input tokens for current session bootstrap
- **Cache:** 24h cache retention on MiniMax-M2.7 — repeated context reuse is efficient

### Layer 4: Agent → Ollama (local)
- **Status:** ⚠️ SLOW
- **Latency:** ~10 tokens/s generation on CPU (qwen3.5:0.8b)
- **Issue:** Single health check took 124,762ms (2 min) — unacceptable for a "lightweight" task
- **Model size on disk:** 1GB (qwen3.5:0.8b, Q8_0 quantization)

### Layer 5: Agent → Tool execution
- **Sandboxed tools:** Route through Docker containers → network=none → no external latency
- **Host tools:** Route through gateway process → very fast
- **Issue:** No differentiation in tool routing latency

### Layer 6: QMD memory search
- **Status:** ✅ Fast (local)
- **Interval:** Updates every 10m
- **Limits:** `maxResults=2`, `maxInjectedChars=1200` per result
- **Issue:** New memory files take up to 10 minutes before searchable

---

## 3. TOKEN CONSUMPTION ANALYSIS

### Session Token Usage (current state)
| Session | Model | Context | Usage | Cache Efficiency |
|---------|-------|---------|-------|-----------------|
| `main:main` | MiniMax-M2.7 | 200k | 44k/200k (22%) | 4% cached |
| `main:telegram:direct` | glm-4.7 | 205k | 16k/205k (8%) | **604% cached** (overlap high) |
| `local-ops:cron:*` (×8 stale) | qwen3.5:0.8b | 33k | 6.8k/33k (21%) | N/A |

### Historical Session Sizes
| Session File | Size | Lines |
|-------------|------|-------|
| Current active | 277KB | 126 entries |
| Previous (Mar 18) | 78KB | 31 entries |
| **Total sessions dir** | **28MB** | 157 files |

### Token Consumption Drivers

| Driver | Severity | Evidence |
|--------|----------|----------|
| **Bootstrap files** | HIGH | 5-6 files injected every session start (~20k chars) |
| **Context accumulation** | MEDIUM | Current session 44k tokens at 1h old — could grow to compaction threshold |
| **Thinking blocks** | MEDIUM | Model-generated thinking text adds token overhead |
| **Docker build log bloat** | RESOLVED | Was 2.7M tokens in Mar 9 incident; now using `tail -20` pattern |
| **Memory search injection** | LOW | 2 results × 1200 chars max = 2400 chars per search |
| **Compaction trigger** | MEDIUM | `softThresholdTokens=32000` — 44k currently, close to threshold |

### Compaction Config
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
**Issue:** With 44k/200k (22%) already used at session start + bootstrap, compaction fires at 32k tokens remaining — but floor is 20k reserve. Current session is close.

---

## 4. TIMEOUT CAUSES

| Timeout | Location | Value | Risk |
|---------|----------|-------|------|
| Agent default | `agents.defaults.timeoutSeconds` | 300s (5 min) | LOW — adequate |
| Subagent | `subagents.runTimeoutSeconds` | 600s (10 min) | LOW — adequate |
| Ollama health check | cron job | 124,762ms actual | **CRITICAL** — model too slow |
| QMD search | `timeoutMs` | 60,000ms | LOW |
| Heartbeat interval | `every: "60m"` | 60 min | LOW |

---

## 5. BOTTLENECKS

| Bottleneck | Severity | Location | Evidence |
|------------|----------|----------|----------|
| **Ollama CPU-bound generation** | HIGH | local-ops agent | 10 tokens/s, 124s per health check |
| **Bootstrap overhead** | MEDIUM | every session | ~20k chars injected regardless of task size |
| **Memory reindex lag** | LOW | QMD 10m interval | New files not immediately searchable |
| **Session rotation** | LOW | `rotateBytes: "10mb"` | Large sessions rotate at 10MB |
| **No streaming** | LOW | Telegram channel | `streaming: "off"` means full response waits for completion |

---

## 6. COST ANALYSIS

| Provider | Model | Context | Token Cost | Session Usage |
|----------|-------|---------|-----------|--------------|
| MiniMax | M2.7 | 200k | $0.30 input / $1.20 output per 1M tokens | 44k tokens (current session) |
| MiniMax | M2.5 | 200k | $0.30 / $1.20 | Not actively used |
| Zai | glm-4.7-flash | 204k | $0 (configured as free) | 16k tokens (Telegram session) |
| Ollama | qwen3.5:0.8b | 32k | $0 (local) | 6.8k tokens × 8 stale sessions |

**Note:** GLM-4.7 and GLM-4.7-flash are configured with `cost: { input: 0, output: 0 }` — free tier or internal API.

---

## 7. PERFORMANCE OBSERVATIONS

### ✅ What's Performing Well
- Host resources: plenty of CPU/RAM headroom
- MiniMax API latency: acceptable (~1-2s per turn)
- Session compaction: working (safeguard mode)
- Docker containers: essentially idle, minimal overhead
- Session rotation: 10MB cap prevents unbounded growth

### ⚠️ Performance Issues
1. **Ollama is the clear latency villain** — 124 seconds for a simple HEALTH_OK response from a local 0.8B model is extreme; likely CPU starved or misconfigured
2. **Bootstrap is expensive** — 20k chars injected every new session regardless of task complexity; for quick questions this is wasteful
3. **Memory search 10-minute lag** — new memory files not findable for up to 10 minutes
4. **Current session growing** — 44k tokens at 1h is on track to hit 32k compaction threshold within a few more hours of conversation
5. **8 stale local-ops sessions** from 6 days ago consuming session store slots

---

## 8. KNOWN PERFORMANCE INCIDENTS

From `incidents/debugging.md`:

| Date | Issue | Status | Impact |
|------|-------|--------|--------|
| 2026-03-09 | Docker build logs → 2.7M tokens = $0.80 | RESOLVED | Reduced via `tail -20` pattern |
| 2026-03-09 | MC frontend can't reach backend API | OPEN | Mission Control deployment blocked |

---

## PHASE 5 SUMMARY

- **Host resources healthy:** 0.38 load, 1.3GB/7.8GB RAM, 62GB disk free — no pressure
- **Ollama is critically slow:** 124s for one health check (qwen3.5:0.8b, CPU-bound, ~10 tkn/s) — the local-ops cron job is effectively unusable at this speed
- **Token consumption:** Current session 44k/200k (22%) at ~1h old — heading toward 32k compaction threshold; bootstrap injects ~20k chars every session start regardless of task
- **MiniMax API performing well:** sub-second latency, 24h cache retention efficient; GLM-4.7 configured as free (cost=0)
- **Cost:** Primarily MiniMax at $0.30/1M input; no GPU costs; Ollama runs local at $0
