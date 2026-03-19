# SYSTEM VALIDATION SUMMARY — OpenClaw Stress Test

**Test Date:** 2026-03-19  
**Test Runner:** Jarvis (main agent)  
**Environment:** VPS, AMD EPYC 9354P, 7.8GB RAM, MiniMax-M2.7

---

## TEST RESULTS — ALL PASS

| Test | Name | Result | Duration |
|------|------|--------|----------|
| 1 | File System Execution | ✅ PASS | < 5s |
| 2 | Subagent Execution | ✅ PASS | 1m21s |
| 3 | Tool Chain Execution | ✅ PASS | < 10s |
| 4 | Long Task (Timeout Test) | ✅ PASS | < 10s |
| 5 | Memory Stability | ✅ PASS | < 15s |
| 6 | Failure Handling | ✅ PASS | < 15s |

**Overall: 6/6 tests passed**

---

## FAILURE PATTERNS OBSERVED

### Pattern 1 — No Sandbox Enforcement on Main Agent
**Severity:** Security  
**Evidence:** Test 1 executed directly on host with zero sandbox friction. `exec.ask: off` means every exec command runs immediately without approval. Combined with Telegram `groupPolicy` now set to `allowlist`, the attack surface is reduced but the fundamental architecture remains: main agent is unsandboxed.

### Pattern 2 — Web Tools Globally Denied
**Severity:** Functional limitation  
**Evidence:** Test 3 could not use web search (group:web denied). This is a deliberate security decision but limits research agent capabilities. Internal file search used as fallback.

### Pattern 3 — Tool Approval Friction is Zero
**Severity:** Security (by design)  
**Evidence:** No approval dialogs, no confirmation prompts. Every exec command runs immediately. Appropriate for a solo operator on a private VPS, but would be dangerous on shared infrastructure.

### Pattern 4 — Subagent Workspace Isolation is Transparent
**Severity:** Low  
**Evidence:** Test 2 subagent wrote to main workspace successfully. Sandbox volume mount maps subagent workspace to the same host path. Effective isolation depends on Docker container enforcement, not on path separation.

### Pattern 5 — Error Messages Are Structured, Not Humanized
**Severity:** UX  
**Evidence:** Test 6 — ENOENT returned as raw `{"status": "error", "error": "ENOENT..."}`. Errors are machine-readable but not particularly user-friendly. No suggestion or recovery hint provided.

---

## ROOT CAUSES (Observed Behavior Only)

### Root Cause 1 — exec.ask=off is a permanent kill switch for approval workflow
Every exec command runs immediately. No per-command approval, no elevated confirmation. This is working as designed but creates a permanent security trade-off.

### Root Cause 2 — Subagent sandbox volume mount collapses workspace isolation
Subagent workspace is mapped to the same filesystem path as main workspace. Files created by subagents land in the same directory tree as main agent files. Effective isolation is only as strong as the Docker container boundary.

### Root Cause 3 — Bootstrap and memory flush consume tokens on every session regardless of task size
Even trivial tasks trigger the full bootstrap load (~6.6K chars minimum). Memory flush fires early when it does fire. This is a configuration issue (now partially fixed with the compaction threshold change from 32K to 160K).

### Root Cause 4 — No automatic fallback when primary model fails
MiniMax is the sole API provider with no tested automatic fallback path to GLM-4.7-flash. FM-1 (MiniMax API outage) results in 100% system block.

### Root Cause 5 — Self-improvement and error logging disabled
Skills for capturing failures are present but disabled. ERRORS.md files are empty templates. The system does not learn from its own failures.

---

## TOP 5 SYSTEM WEAKNESSES

### #1 — Zero Approval Friction on Exec (CRITICAL by design)
`exec.ask: off` combined with unsandboxed main agent means any successful prompt injection = immediate RCE. Now partially mitigated by Telegram allowlist, but exec itself remains frictionless for anyone with session access.

### #2 — No Automatic Model Fallback (HIGH)
MiniMax is the only wired provider for main and researcher agents. GLM-4.7-flash exists in config but is not confirmed as automatic fallback. A MiniMax outage = complete system failure.

### #3 — Bootstrap Inefficiency (MEDIUM)
~6.6K chars of bootstrap loaded before every session regardless of task scope. With bootstrap budget now 40K, headroom exists, but the minimum load is still heavy for trivial tasks.

### #4 — Weak Error Recovery Visibility (MEDIUM)
Errors are structured but lack recovery hints. When a tool fails, the agent receives `{"error": "..."}` with no suggestion for remediation. Loop detection fires late (after 6-12 repeats).

### #5 — Stale Session Accumulation (MEDIUM — partial fix applied)
8 orphaned sessions accumulated over 6 days because local-ops cron job was disabled and session archive didn't fire. Session cleanup is now running, but the root cause (Ollama slowness disabling the cron job) has not been addressed.

---

## FILES PRODUCED

| File | Purpose |
|------|---------|
| `reports/test_results_1.md` | File system execution results |
| `reports/test_results_2.md` | Subagent execution results |
| `reports/test_results_3.md` | Tool chain execution results |
| `reports/test_results_4.md` | Long task results |
| `reports/test_results_5.md` | Memory stability results |
| `reports/test_results_6.md` | Failure handling results |
| `reports/subagent_test.md` | Subagent output (307 words) |
| `reports/tool_chain.md` | Tool chain output (3 key points) |
| `reports/long_task.md` | Long task output (565 words) |
| `reports/memory_test_facts.md` | Memory test source facts |
| `reports/memory_test_summary.md` | Memory test summary |
| `reports/recovery_success.md` | Failure recovery proof |
| `reports/system_validation_summary.md` | This document |

---

*Test suite completed: 2026-03-19 20:59 UTC*
