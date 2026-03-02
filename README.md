# OpenClaw Agent Workspace

**Personal AI Assistant Environment** - Customized for high-value, token-efficient operations on a VPS server.

---

## 📋 Overview

This is a self-hosted OpenClaw workspace configured for **token-efficient, cost-conscious AI operations**. Built on GLM-4.7 model tiering with qmd memory search and automated maintenance.

**Purpose:** Personal productivity system for software engineer with 9-6 work schedule, psychological product development, and $20k/month income goal.

---

## 🚀 Quick Start (One-Time Setup)

### Prerequisites
- Node.js 22+ installed
- Telegram account (for direct messaging)
- VPS or server environment
- Git repository created (e.g., GitHub/GitLab)

### Installation Steps

```bash
# 1. Install OpenClaw globally
npm install -g openclaw@latest

# 2. Run onboard wizard
openclaw onboard

# 3. Install as daemon/service (if on server)
openclaw onboard --install-daemon

# 4. Pair Telegram channel
openclaw channels login

# 5. Start Gateway
openclaw gateway --port 18789

# 6. Clone this repo
git clone <your-repo-url> /root/.openclaw/workspace
cd /root/.openclaw/workspace

# 7. Create OpenClaw config from config-optimizations.md
# (Copy settings from config-optimizations.json to ~/.openclaw/openclaw.json)

# 8. Run doctor to validate config
openclaw doctor

# 9. Start the gateway
openclaw gateway --port 18789
```

**Access the Web UI:** `http://<server-ip>:18789`

---

## 🧠 Core Features

### 1. **Memory System (qmd + dory-memory)**
- **qmd-skill:** Local markdown search using BM25 (no GPU needed)
- **dory-memory:** Session continuity across context resets
- **Config:**
  - Update interval: 5 minutes
  - Max results: 3
  - Snippet chars: 300
  - Injected chars: 1500
- **Daily cron:** Runs at 2 AM UTC for memory maintenance

### 2. **Model Tiering (GLM-4.7)**
- **zai/glm-4.7-flash (alias: daily):** Casual chat, maxTokens=2000
- **zai/glm-4.7 (alias: coding):** Heavy coding, maxTokens=8000
- **Expected savings:** 37% token reduction on daily sessions

### 3. **Session Management**
- **Token budget:** 10,000 per session
- **Warning at:** 8,000 tokens
- **Critical at:** 9,500 tokens
- **Auto-pruning:** 30-day retention, 200 max entries, 10MB rotate

### 4. **Telegram Channel**
- **Enabled:** Yes
- **DM policy:** Pairing
- **Group policy:** Allowlist (needs sender IDs configured)
- **Streaming:** Off

### 5. **Cron System**
- **Daily memory maintenance:** 2 AM UTC (isolated session, glm-4.7, light context)
- **Runs:** Session maintenance via `openclaw sessions cleanup`

### 6. **Skills Installed**
- **qmd-skill:** Local markdown search (BM25-based)
- **dory-memory:** Session continuity

---

## 🎯 Strategy & Philosophy

### Operator Mindset
- "I can't" is not in vocabulary — figure it out, ship results
- External actions require approval (emails, tweets, public posts)
- Internal actions: read, explore, organize, learn (free)
- **Operators ship** — focus on delivery over explanations

### Token Efficiency Goals
1. Reduce casual chat token usage by 75% (8K → 2K maxTokens)
2. Monitor session budgets with automatic alerts
3. Use flash model for daily tasks, full model for heavy coding
4. Target 37% overall reduction in monthly costs

### Memory Strategy
- **Daily files:** Raw logs in `memory/YYYY-MM-DD.md`
- **Long-term:** Curated in `MEMORY.md` (distilled learnings)
- **Review frequency:** Every few days during heartbeats
- **Prune:** Remove outdated info, keep what matters long-term

### Communication
- **Platform:** Telegram
- **Style:** Casual, direct, concise
- **Always include:** Model + token usage footer

---

## 📁 Project Structure

```
/root/.openclaw/workspace/
├── AGENTS.md                    # Agent behavior rules
├── HEARTBEAT.md                 # Periodic check tasks
├── IDENTITY.md                  # Agent persona
├── LESSONS.md                   # Documented lessons
├── MEMORY.md                    # Long-term memory
├── SOUL.md                      # Agent soul/purpose
├── TOOLS.md                     # Local notes (cameras, SSH, etc.)
├── USER.md                      # User profile
├── config-optimizations.md      # Config changes history
├── README.md                    # This file
├── test-coding-module.js        # Testing artifacts
├── test-report.md               # Test results
├── .clawhub/                    # ClawHub cache
├── .openclaw/                   # OpenClaw config & state
├── memory/                      # Daily memory logs
│   ├── 2026-03-01.md
│   └── 2026-03-02.md
├── ops/                         # Operations scripts
├── skills/                      # Installed skills
│   ├── dory-memory/
│   ├── mcporter/
│   ├── qmd-skill/
│   ├── sonoscli/
│   ├── skill-creator/
│   ├── tmux/
│   └── video-frames/
└── state/                       # Runtime state
```

---

## 🔄 Maintenance & Automation

### Heartbeat Checks (Every ~30 min)
Rotate through:
- Telegram notifications
- Calendar events (next 24-48h)
- Social mentions
- Weather (if going out)

### Cron Jobs (Server-time precise)
1. **Daily Memory Maintenance:** 2 AM UTC
   - Task: Read recent memory files, update MEMORY.md, prune outdated info
   - Model: zai/glm-4.7
   - Context: Lightweight bootstrap

2. **Session Cleanup:** (via systemd cron)
   - Task: Prune old sessions, rotate memory
   - Schedule: 2 AM UTC (standard cron)

### Memory Review (Manual, during heartbeats)
Every few days:
1. Read recent `memory/YYYY-MM-DD.md` files
2. Identify significant events/lessons
3. Update `MEMORY.md` with distilled learnings
4. Remove outdated info

---

## 🔧 Configuration

### Current Settings (Optimized)
```json
{
  "model": {
    "daily": "zai/glm-4.7-flash",
    "coding": "zai/glm-4.7"
  },
  "memory": {
    "backend": "qmd",
    "interval": "5m",
    "maxResults": 3,
    "maxSnippetChars": 300,
    "maxInjectedChars": 1500
  },
  "session": {
    "dmScope": "per-channel-peer",
    "tokenBudget": {
      "budget": 10000,
      "warningThreshold": 8000,
      "alertThreshold": 9500
    },
    "maintenance": {
      "pruneAfter": "30d",
      "maxEntries": 200,
      "rotateBytes": "10mb"
    }
  }
}
```

### Recommended (Not Yet Applied)
```json
{
  "flashModel": {
    "maxTokens": 1500  // Reduce from 2000
  },
  "memory": {
    "maxSnippetChars": 200,  // Reduce from 300
    "maxInjectedChars": 1200,  // Reduce from 1500
    "interval": "10m"  // Increase from 5m
  },
  "maxResults": 2  // Reduce from 3
}
```

---

## 🤖 Agent Behavior

### Core Rules
- Be genuinely helpful, not performatively helpful
- Have opinions (disagree when appropriate)
- Be resourceful before asking (search, read, check context)
- Earn trust through competence
- Remember you're a guest (don't exfiltrate private data)

### In Group Chats
- **Respond when:** Directly mentioned, adding value, correcting misinformation, summarizing
- **Stay silent:** Casual banter, already answered, "yeah" or "nice" responses, conversation flowing fine

### Platform Formatting
- **Discord/WhatsApp:** No markdown tables (use bullet lists)
- **Discord links:** Wrap in `< >` to suppress embeds
- **WhatsApp:** No headers (use bold or CAPS for emphasis)

---

## 📊 Performance Metrics

### Expected Monthly Usage (50 sessions)
- **Before optimizations:** ~400K tokens (~$0.03)
- **After optimizations:** ~250K tokens (~$0.02)
- **Savings:** 37% (~$0.01)

### Session Breakdown
- **Casual chat:** 70% (GLM-4.7-flash, 2K maxTokens)
- **Coding tasks:** 25% (GLM-4.7, 8K maxTokens)
- **Heavy coding:** 5% (GLM-4.7, 8K maxTokens)

---

## 🔐 Security

### What's Allowed (Internal)
- ✅ Read files, explore, organize, learn
- ✅ Search web, check calendars
- ✅ Work within workspace

### What Needs Approval (External)
- ⚠️ Sending emails, tweets, public posts
- ⚠️ Anything leaving the machine
- ⚠️ Anything uncertain

### Security Hardening (Recommended)
- Run `openclaw security audit --deep` regularly
- Review allowlists for Telegram groups
- Keep Node.js updated
- Monitor token usage weekly

---

## 🚦 Heartbeat vs Cron

### Use Heartbeat When
- Multiple checks can batch together
- Conversational context needed
- Timing can drift slightly (~30 min)
- Want to reduce API calls

### Use Cron When
- Exact timing matters ("9:00 AM sharp")
- Task needs isolation from main session
- Want different model/thinking level
- One-shot reminders

---

## 🛠️ Development Tools

### Git Workflow
```bash
# Clone
git clone <repo-url> /root/.openclaw/workspace
cd /root/.openclaw/workspace

# Check status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin master
```

### Skills Management
- **ClawHub:** `clawhub search <query>`
- **Install:** `clawhub install <skill-name>`
- **Update:** `clawhub update <skill-name>`
- **Publish:** `clawhub publish <skill-folder>`

---

## 📝 Documentation

### Key Files
- **AGENTS.md:** Agent behavior rules
- **MEMORY.md:** Long-term memory (curated)
- **SOUL.md:** Agent persona
- **USER.md:** User profile
- **config-optimizations.md:** Config changes history

### OpenClaw Docs
- Main: https://docs.openclaw.ai
- Docs hub: https://docs.openclaw.ai/start/hubs
- Configuration: https://docs.openclaw.ai/gateway/configuration
- Nodes: https://docs.openclaw.ai/nodes

---

## 🎯 Next Steps

### Immediate (Done)
- ✅ Switched to GLM-4.7 model
- ✅ Created daily cron job (2 AM UTC, light context)
- ✅ Configured token budget tracking
- ✅ Set up qmd memory search
- ✅ Documented all features

### Recommended
1. **Monitor first week:**
   - Track actual token usage per session
   - Verify alerts trigger correctly
   - Adjust budget based on usage

2. **Tune memory limits:**
   - Reduce flash maxTokens: 2000 → 1500
   - Tighten memory limits further
   - Extend memory update interval: 5m → 10m

3. **Security hardening:**
   - Configure Telegram group allowlist
   - Run security audit
   - Review allowlist/denylist

4. **Git repo:**
   - Create GitHub/GitLab repo
   - Push initial commit
   - Set up CI/CD if desired

---

## 📞 Getting Help

### Troubleshooting
- Check OpenClaw status: `openclaw status`
- Run doctor: `openclaw doctor`
- Check logs: `~/.openclaw/logs/`
- Docs: https://docs.openclaw.ai

### Common Issues
- **Config invalid:** Run `openclaw doctor --fix`
- **Session cleanup fails:** Check disk space, run manually
- **Telegram not working:** Verify bot token, check allowlist
- **Memory slow:** Run `qmd embed` when GPU available

---

## 🏆 Success Metrics

### Track These
1. **Token usage per session** (target: <5K for daily)
2. **Cost per month** (target: <$0.05/month)
3. **Memory relevance** (quality of search results)
4. **Response time** (should be <10s for casual chat)

### Goal
Build a **$20k/month income** psychological product while maintaining **high personal productivity** through AI automation.

---

## 📜 License

This workspace is built with OpenClaw (MIT licensed).

**Agent created by:** Mohamad
**Timezone:** GST (Dubai, UTC+4)
**Vibe:** Sharp, helpful, slightly witty — like a competent coworker
