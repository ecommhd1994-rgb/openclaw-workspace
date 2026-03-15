# Debugging Log

Solved technical issues and operational fixes.

## Format

```markdown
### [Issue Title]

**Date:** YYYY-MM-DD
**Status:** RESOLVED | BLOCKED
**Symptom:** What happened
**Root Cause:** Why it happened
**Solution:** How it was fixed
**Related Files:** Any files involved
```

## Issues

---

### Token Bloat from Docker Build Logs

**Date:** 2026-03-09
**Status:** RESOLVED
**Symptom:** 2.7M input tokens from Mission Control Docker install = $0.80 charge
**Root Cause:** Docker build logs filled context window
**Solution:** 
- Use `tail -20` for command outputs instead of full logs
- Start fresh session for big projects
- Redirect long command outputs to file
**Related Files:** N/A

---

### Mission Control Frontend Can't Reach Backend API

**Date:** 2026-03-09
**Status:** OPEN
**Symptom:** Network isolation between frontend and backend containers
**Root Cause:** network_mode issue in Docker configuration
**Solution:** TBD
**Related Files:** /root/openclaw-mission-control

---

_Last updated: 2026-03-15_
