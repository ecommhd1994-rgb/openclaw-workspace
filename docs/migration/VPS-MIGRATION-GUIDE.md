# OpenClaw VPS Migration Guide

> Complete guide to migrate your OpenClaw setup to a new VPS
> Last updated: 2026-03-18

---

## What Gets Backed Up

### Core Configuration
- `~/.openclaw/openclaw.json` - Main config (providers, models, skills)
- `~/.openclaw/.env` - API keys (ZAI_API_KEY)
- `~/.openclaw/exec-approvals.json` - Approved commands

### Workspaces & Data
- `~/.openclaw/workspace/` (~13MB)
  - AGENTS.md, MEMORY.md, SOUL.md, USER.md
  - memory/, state/, projects/, reports/
  - docs/, workflows/, .learnings/

### Agent Data (~59MB)
- `~/.openclaw/agents/` - All agent directories
  - **Main QMD index** (~22MB) - Your searchable docs
  - Researcher, Writer, Local-ops QMD indexes
  - Session history and state

### Skills
- **Installed skills (53 total)** in `/usr/lib/node_modules/openclaw/skills/`
  - clawhub, coding-agent, gh-issues, healthcheck, mcporter, etc.
- **Custom skills** in `~/.openclaw/workspace/skills/`
  - qmd-skill, session-logs, sonoscli, dory-memory, self-improving-agent

### Integration State
- `~/.openclaw/credentials/` - Telegram pairing
- `~/.openclaw/identity/` - Identity certificates
- `~/.openclaw/telegram/` - Telegram state
- `~/.openclaw/devices/` - Paired devices

### System Integration
- **Cron:** `0 2 * * * cd /root/.openclaw && openclaw sessions cleanup`
- **Ollama:** qwen3.5:0.8b model (1GB)
- **NPM:** openclaw@2026.3.13, clawhub@0.7.0


---

## Quick Start

### On CURRENT VPS
```bash
# Run backup script
cd ~/.openclaw/workspace/docs/migration
./backup-openclaw.sh
# Transfer to new VPS
scp /tmp/openclaw-backup-*.tar.gz root@new-vps:/tmp/
```

## Post-Migration Checklist

- [ ] OpenClaw status: `openclaw status`
- [ ] Gateway running: `systemctl status openclaw-gateway`
- [ ] Ollama running: `systemctl status ollama && ollama list`
- [ ] Agents available: `openclaw agents list`
- [ ] QMD works (search test)
- [ ] Telegram bot responds
- [ ] Cron jobs: `crontab -l`
- [ ] Skills installed: `ls /usr/lib/node_modules/openclaw/skills/`
- [ ] Devices paired: `openclaw devices list`

## Troubleshooting

### Gateway won't start
```bash
journalctl -u openclaw-gateway -n 50
openclaw config validate
```

### Devices won't connect
- Check firewall: `ufw allow 8080:8089/tcp`
- Re-scan QR code on companion apps
- Update gateway URL in ~/.openclaw/openclaw.json if IP changed

### QMD not working


## Troubleshooting

### Gateway won't start
```bash
journalctl -u openclaw-gateway -n 50
openclaw config validate
systemctl restart openclaw-gateway
```

### Devices won't connect
- Check firewall: `ufw allow 8080:8089/tcp`
- Re-scan QR code on companion apps
- Update gateway URL in ~/.openclaw/openclaw.json if IP changed

### Ollama model missing
```bash
ollama pull qwen3.5:0.8b
ollama list
```

## Backup Size Estimate

- Workspace: ~13MB
- Agent data: ~59MB (including 22MB QMD)
- Config & credentials: <1MB
- **Total data: ~73MB**
- Ollama model: 1GB (if exported)
- **Archive size: ~500MB - 1.5GB**

---

**Created:** 2026-03-18  |  **Branch:** feature/optimized-workspace
