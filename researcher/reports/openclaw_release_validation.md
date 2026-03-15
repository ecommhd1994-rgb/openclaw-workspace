# OpenClaw Release Validation Report

## Overview

**Latest Release:** v2026.3.13 (npm: 2026.3.13)  
**Release Date:** March 14, 2026  
**Type:** Recovery release (fixes broken v2026.3.13 tag)  
**Repository:** https://github.com/openclaw/openclaw

This is a significant patch release addressing 70+ issues across mobile apps, desktop platforms, security, and core agent functionality. The release includes a major dashboard overhaul, new model support, and important security hardening.

---

## Key Changes

### 🚀 New Features

1. **Dashboard v2 (Control UI)**
   - Modular overview, chat, config, agent, and session views
   - Command palette, mobile bottom tabs
   - Richer chat tools: slash commands, search, export, pinned messages

2. **Fast Mode for GPT-5.4 & Claude**
   - Configurable session-level fast toggles via /fast, TUI, Control UI, and ACP
   - Per-model config defaults and OpenAI/Codex request shaping
   - Direct Anthropic API service_tier requests with live verification

3. **Model Provider Plugins**
   - Ollama, vLLM, and SGLang moved to provider-plugin architecture
   - Provider-owned onboarding, discovery, model-picker setup

4. **Kubernetes Support**
   - Starter K8s install path with raw manifests, Kind setup, deployment docs

5. **Subagents: sessions_yield**
   - Orchestrators can end current turn immediately
   - Skip queued tool work and carry hidden follow-up payload into next turn

6. **Slack Block Kit Support**
   - Agents can send Block Kit messages through standard Slack outbound delivery

### 🔧 Platform Improvements

| Platform | Changes |
|----------|---------|
| **Android** | Redesigned chat settings UI, Google Code Scanner for QR onboarding |
| **iOS** | New onboarding welcome pager, stop auto-opening QR scanner |
| **macOS** | Respect exec-approvals.json in gateway prompter, PortGuard fix for Docker Desktop |
| **Windows** | Suppress console windows during restart, bound schtasks calls |
| **Docker** | OPENCLAW_TZ timezone support |

### 🛡️ Security Fixes (Multiple CVEs)

- **Device Pairing:** Bootstrap setup codes now single-use
- **Plugin Auto-load:** Disabled implicit workspace plugin auto-load
- **Exec Approvals:** Enhanced detection for pnpm, Ruby, Perl, PowerShell
- **Webhooks:** Improved validation for Telegram, Feishu, LINE, Zalo, Slack
- **Session Status:** Enforced sandbox session-tree visibility

### 🐛 Bug Fixes

- Ollama reasoning models: Hide native thinking/reasoning output
- Dashboard: Stop chat history reload storms
- Gateway: Bound unanswered client requests
- Telegram: IPv4 fallback for media downloads
- Discord: Handle gateway metadata fetch failures
- Session: Preserve lastAccountId/lastThreadId on reset
- Memory: Avoid injecting memory file twice on case-insensitive mounts

### ⚡ Performance

- **Build:** Deduplicated plugin-sdk chunks, fixed ~2x memory regression
- **Cron:** Prevent isolated cron nested lane deadlocks

---

## Why This Release Matters

1. **Security First:** Multiple security vulnerabilities fixed (CVEs documented in changelog)
2. **Better UX:** Major dashboard overhaul improves daily workflow
3. **Platform Parity:** Significant fixes across all desktop and mobile platforms
4. **Model Flexibility:** New fast mode and provider plugin architecture
5. **Stability:** 70+ fixes addressing long-standing issues

---

## New Contributors

19 first-time contributors in this release, indicating healthy community growth.

---

## Upgrade Recommendation

**Recommended for all users.** This release contains important security fixes and significant usability improvements. Users should upgrade to 2026.3.13.

---

*Report generated: March 15, 2026*
