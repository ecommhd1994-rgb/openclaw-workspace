# VPS Migration Guide

This guide covers moving OpenClaw from one VPS to another.

---

## 1. Pre-Migration Checklist

### From Source VPS:

✅ **Workspace files** (committed to Git)
- All configs, skills, memory, and agent definitions

✅ **Cron jobs** (manual backup required)
- `~/.openclaw/cron/jobs.json`

✅ **Current branch** (note this for restore)
- `git branch` → save active branch name

✅ **Git remote** (optional but recommended)
- Verify you can push: `git remote -v`
- If not set, add: `git remote add origin <your-repo-url>`

---

## 2. Backup Source VPS

### Step 1: Push workspace to GitHub

```bash
cd ~/.openclaw/workspace
git add .
git commit -m "Pre-migration backup"
git push origin vps-migration-guide
```

### Step 2: Backup cron jobs

```bash
mkdir -p ~/openclaw-backup
cp ~/.openclaw/cron/jobs.json ~/openclaw-backup/
```

### Step 3: Backup OpenClaw config (optional)

If you have custom OpenClaw gateway config:

```bash
cp ~/.openclaw/config/gateway.yaml ~/openclaw-backup/ 2>/dev/null || true
```

---

## 3. On New VPS: Setup OpenClaw

### Step 1: Install OpenClaw

```bash
npm install -g openclaw
```

### Step 2: Verify installation

```bash
openclaw version
openclaw status
```

### Step 3: Initialize workspace

```bash
cd ~/.openclaw
git clone <your-repo-url> workspace
cd workspace
```

### Step 4: Checkout migration branch

```bash
git checkout vps-migration-guide
```

---

## 4. Restore Cron Jobs

### Step 1: Copy jobs.json

```bash
mkdir -p ~/.openclaw/cron
# Upload your backed-up jobs.json here
# scp ~/openclaw-backup/jobs.json user@new-vps:~/.openclaw/cron/
```

### Step 2: Verify cron status

```bash
openclaw cron status
openclaw cron list
```

Jobs should appear. If disabled, re-enable them:

```bash
# Get job ID from `openclaw cron list`
openclaw cron update <job-id> --patch '{"enabled": true}'
```

---

## 5. Start OpenClaw Gateway

```bash
openclaw gateway start
openclaw gateway status
```

---

## 6. Post-Migration Verification

### Check 1: Workspace loaded
- AGENTS.md should exist
- SOUL.md, USER.md should have your config
- Skills folder should be populated

### Check 2: Memory intact
- Check `memory/` folder for recent entries

### Check 3: Cron jobs
- Run `openclaw cron list` — all jobs should appear

### Check 4: Local LLM (if using Ollama)
```bash
ollama list
ollama run qwen3.5:0.8b  # Test model
```

### Check 5: Test a session
- Start a new session via your chat channel
- Verify agent responds correctly

---

## 7. Optional: Clean Up Source VPS

After confirming new VPS works:

```bash
# Stop gateway
openclaw gateway stop

# Optional: Remove old workspace (be careful!)
# rm -rf ~/.openclaw/workspace
```

---

## 8. Troubleshooting

### Cron jobs missing after migration
- Ensure `~/.openclaw/cron/jobs.json` was copied
- Run `openclaw cron status` to verify cron daemon running

### Workspace not loading
- Verify Git clone completed successfully
- Run `ls -la ~/.openclaw/workspace/AGENTS.md`

### Agent not responding
- Check `openclaw gateway status`
- Review logs: `openclaw gateway logs`

### Local LLM not responding
- Verify Ollama is installed: `ollama --version`
- Check if model exists: `ollama list`
- If missing, pull: `ollama pull qwen3.5:0.8b`

---

## File Inventory

**Critical files (must migrate):**
- `~/.openclaw/workspace/` → Git repo
- `~/.openclaw/cron/jobs.json` → Manual copy

**Optional (custom setups only):**
- `~/.openclaw/config/gateway.yaml` → Manual copy (if you customized it)

**Generated on new VPS (no migration needed):**
- `~/.openclaw/sessions/` — Session history
- `~/.openclaw/data/` — Runtime data
- `~/.openclaw/cache/` — Cache files

---

## Quick Reference Commands

```bash
# Source VPS: Backup
cd ~/.openclaw/workspace && git add . && git commit -m "backup" && git push origin vps-migration-guide
cp ~/.openclaw/cron/jobs.json ~/openclaw-backup/

# New VPS: Setup
npm install -g openclaw
cd ~/.openclaw && git clone <your-repo> workspace && cd workspace
git checkout vps-migration-guide
mkdir -p ~/.openclaw/cron && cp ~/openclaw-backup/jobs.json ~/.openclaw/cron/
openclaw gateway start
```

---

Generated: 2026-03-19
For: OpenClaw VPS migration
