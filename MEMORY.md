# MEMORY.md - Long-Term Memory

## About Mohamad
- Name: Mohamad
- Timezone: GST (Dubai, UTC+4)
- Style: Casual
- Communication: Telegram
- Vibe: Operator mindset — "figure it out, ship results"

## Server Specs
- **CPU:** AMD EPYC 9354P 32-Core (2 cores allocated)
- **RAM:** 7.8GB total (~6.6GB available)
- **GPU:** None (CPU-only)

## Local LLM (Ollama)
- **Installed:** qwen3.5:0.8b
- **API:** http://localhost:11434
- **Use case:** Cron jobs, heartbeat tasks (save API tokens)
- **Performance:** ~10 tokens/s, 28-57s per response
- **RAM:** ~1GB used

## User Preferences
- Prefers short, concise responses
- Works from 9 to 6 as software engineer
- Building OpenClaw on VPS
- Has history of kidney stones
- Wants $20k/month income
- Struggles with perfectionism
- Prefers direct feedback
- Uses MiniMax-M2.5 model (current session)
- Uses GLM-4.7-flash as default model
- Wants to build a psychological product
- Tracks token usage carefully
- **Always backup before updates/config changes** — `openclaw backup create --verify`

## Skills Installed
- qmd: Local markdown search (BM25)
- dory-memory: Session continuity
- self-improving-agent: Captures learnings, errors, corrections

## Lessons Learned
- Prefers practical ROI over theory
- Focused on token efficiency and cost savings
- Avoid: Let Docker build logs fill context; use tail -20 for outputs; start fresh session for big projects
