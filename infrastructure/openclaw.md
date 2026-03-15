# OpenClaw Infrastructure

## Mission Control
- **Installed:** 2026-03-09
- **Location:** /root/openclaw-mission-control
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **Auth Token:** cfb005a47e1d8994ea60ce551514fc21f2b73079f9a5930bebb863a2471d25bd
- **Disk usage:** ~2.6GB (6GB images, 4GB cleaned)
- **Status:** Running, NOT connected to OpenClaw gateway
- **Port conflict:** Both OpenClaw and MC want port 3000

## OpenClaw Configuration
- **Gateway port:** 3000 (default)
- **Config file:** /root/.openclaw/workspace/openclaw-config.json
- **Memory backend:** qmd (BM25)
- **Default model:** glm-4.7-flash
- **Session model:** MiniMax-M2.5
- **Token budget:** 10k session, warning at 8k, alert at 9.5k

## Local LLM (Ollama)
- **Installed:** qwen3.5:0.8b
- **API:** http://localhost:11434
- **Use case:** Cron jobs, heartbeat tasks
- **RAM:** ~1GB used

## Todo
- [ ] Debug: Mission Control frontend can't reach backend API (network_mode issue)
- [ ] Connect Mission Control to OpenClaw gateway
