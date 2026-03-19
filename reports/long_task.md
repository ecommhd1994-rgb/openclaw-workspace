# OpenClaw System Test — Long Task Report

**Generated:** 2026-03-19 20:57 UTC

---

## Section 1 — System Overview

OpenClaw is a self-hosted AI gateway system that bridges chat applications to AI agents. It runs as a single process on a configurable port (default 18789), handling WebSocket control, HTTP APIs, channel connections, and the control UI. The system supports multiple chat platforms including Telegram, WhatsApp, Discord, iMessage, and Signal through a unified plugin architecture. Each channel connects through the Gateway, which maintains session state and routes messages to the appropriate agent based on configurable rules. The Gateway is designed to be always-on, runs on the operator's own hardware, and keeps all data local rather than relying on hosted services. Configuration is hot-reloaded without full restarts, allowing runtime changes to agents, channels, and tools.

---

## Section 2 — Agent Architecture

OpenClaw supports multiple concurrent agents, each with isolated sessions and workspaces. The main agent (Jarvis) serves as the primary orchestrator, delegating research tasks to a dedicated researcher agent and system operations to a local-ops agent. Each agent can have custom model configurations with primary and fallback providers, custom tool profiles and permissions, and a dedicated workspace directory. Session scoping options include per-peer, per-channel, or per-agent isolation. Subagents run in Docker containers when sandboxed, with network access restricted to none and no Linux capabilities. The tool layer exposes typed first-class tools replacing legacy shell-based skills, with security profiles controlling access at the agent level.

---

## Section 3 — Tool Security Model

Tools in OpenClaw are globally allowed or denied via configuration with wildcard support and provider-specific restrictions. Four security profiles exist: minimal (session_status only), coding (filesystem, runtime, sessions, memory, image), messaging (messaging tools plus session tools), and full (no restrictions). Loop detection monitors for generic repeats, known poll-no-progress patterns, and ping-pong oscillations, with configurable warning and critical thresholds. The exec tool can run on the gateway host or in sandboxed containers depending on configuration, with approval modes set to off, on-miss, or always. Sandbox isolation uses Docker containers with network=none, cap_drop=ALL, and read-only root filesystems where applicable.

---

## Section 4 — Memory and Session Management

OpenClaw implements a five-tier memory hierarchy: working memory (daily session notes), project memory (architecture and design docs), infrastructure memory (server config and runbooks), incidents memory (solved bugs and fixes), and core memory (permanent truths and preferences). Promotion between tiers follows documented rules, with significant discoveries moving from daily session notes toward permanent storage. Session state is maintained per-peer or per-channel, with 30-day automatic pruning and 50-entry caps. The system rotates session logs at 10MB and maintains a 14-day archive retention window. Compaction triggers at configurable token thresholds to prevent context overflow while preserving critical state.

---

## Section 5 — Current Deployment Status

The active deployment runs on a VPS with 32 AMD EPYC cores, 7.8GB RAM, and 62GB free disk. MiniMax M2.7 serves as the primary model with a 200K token context window, backed by GLM-4.7-flash as a configured fallback. Local inference via Ollama (qwen3.5:0.8b) handles lightweight cron and heartbeat tasks. Recent diagnostic work identified and remediated several issues: Telegram group policy tightened from open to allowlist, bootstrap budget increased from 20K to 40K characters, QMD memory retrieval limits raised, compaction threshold recalibrated to fire at 80% context, and stale session files and containers cleaned up. Remaining items include token rotation, ZAI cost verification, and fallback model wiring.
