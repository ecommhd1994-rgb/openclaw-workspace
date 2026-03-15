# OpenClaw Release Summary - Version 2026.3.13

## Release Overview

**Version:** 2026.3.13  
**Release Date:** March 14, 2026  
**Type:** Stable Release  

## Key Features & Changes

This release includes numerous bug fixes, improvements, and new features:

### Core Fixes
- **Session Management:** Preserved `lastAccountId` and `lastThreadId` on session reset
- **Compaction:** Use full-session token count for post-compaction sanity check
- **Agent Memory:** Avoid injecting memory file twice on case-insensitive mounts

### Platform Improvements

**Android:**
- Redesigned chat settings UI
- Fixed HttpURLConnection leak in TalkModeVoiceResolver
- Added Google Code Scanner for onboarding QR

**iOS:**
- Added onboarding welcome pager

**macOS:**
- Respects exec-approvals.json settings in gateway prompter
- Prevents PortGuard from killing Docker Desktop in remote mode
- Aligns minimum Node.js version with runtime guard (22.16.0)

### Messaging Integrations
- **Telegram:** Thread media transport policy into SSRF; retry media downloads over IPv4 fallback
- **Discord:** Handle gateway metadata fetch failures
- **Signal:** Added groups config to Signal channel schema
- **Slack:** Added opt-in interactive reply directives
- **Feishu:** Preserve non-ASCII filenames in file uploads; add early event-level dedup

### UI/UX
- Mobile navigation drawer & theme variant refinements
- Fixed chat context notice icon sizing
- Stopped dashboard chat history reload storm
- Keep oversized chat replies readable

### Docker & Infrastructure
- Added OPENCLAW_TZ timezone support
- Prevents gateway token leak in Docker build context
- Add apt-get upgrade to all Dockerfiles

### Model & AI
- Updated default model from openai-codex/gpt-5.3-codex to openai-codex/gpt-5.4 in tests
- Fixed Ollama native reasoning-only output hiding
- Applied Gemini model-id normalization to google-vertex provider

## Statistics
- Total PRs: 60+
- New Contributors: 19
- Release Reactions: 103 (70 👍, 11 🚀, 7 ❤️)

## Previous Version
v2026.3.12
