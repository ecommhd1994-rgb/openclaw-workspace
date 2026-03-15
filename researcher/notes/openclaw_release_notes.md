# OpenClaw Release Research Notes

## Release Identification

- **Latest stable:** v2026.3.13 (npm: 2026.3.13)
- **Latest beta:** v2026.3.13-beta.1 (npm: 2026.3.13-beta.1)
- **Published:** 2026-03-14T18:04:28Z (stable), 2026-03-14T05:17:09Z (beta)

## Release Notes Summary

### v2026.3.13 (Recovery Release)
- Recovery release to fix broken v2026.3.13 tag
- 70+ pull requests merged
- 19 first-time contributors

### Notable Changes from v2026.3.12

#### Features
- Dashboard v2 with modular views
- Fast mode for GPT-5.4 and Claude
- Provider plugin architecture for Ollama, vLLM, SGLang
- Kubernetes deployment docs
- sessions_yield for subagents
- Slack Block Kit support

#### Security
- Multiple CVE fixes
- Disabled plugin auto-load
- Improved webhook validation
- Enhanced exec approval detection

#### Bug Fixes
- Ollama reasoning visibility
- Dashboard reload storms
- Gateway request bounding
- Telegram IPv4 fallback
- Session state preservation

## Observations

1. The release follows a rapid cadence (v2026.3.12 on March 13, v2026.3.13 on March 14)
2. Strong security focus with multiple CVEs addressed
3. Cross-platform improvements for Android, iOS, macOS, Windows, Docker
4. New contributors joining the project

## Version Pattern

- Uses date-based versioning: YYYY.M.M
- Recovery releases use -1, -2 suffix
- Beta releases use -beta.X suffix

---

*Notes compiled: March 15, 2026*
