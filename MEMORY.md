# MEMORY.md - Long-Term Memory

## About Mohamad
- Name: Mohamad
- Timezone: GST (Dubai, UTC+4)
- Style: Casual
- Communication: Telegram
- Vibe: Operator mindset — "figure it out, ship results"

## Lessons Learned
- Prefers practical ROI over theory
- Focused on token efficiency and cost savings
- Running on server (Linux, no GPU)
- **Token bloat incident (Mar 2026):** 2.7M input tokens from Mission Control Docker install = $0.80 charge
- **Avoid:** Let Docker build logs fill context; use tail -20 for outputs; start fresh session for big projects

## Durable Facts
- User prefers short responses
- User works from 9 to 6 as software engineer
- User is building OpenClaw on VPS
- User has history of kidney stones
- User wants $20k/month income
- User struggles with perfectionism
- User prefers direct feedback
- User uses MiniMax-M2.5 model (current session)
- User uses GLM-4.7-flash as default model
- User wants to build a psychological product
- User tracks token usage carefully

## Skills Installed
- qmd: Local markdown search (BM25, needs embeddings for semantic)
- dory-memory: Session continuity
- self-improving-agent: Captures learnings, errors, corrections for continuous improvement

## Communication Preferences
- Always include **Model** and **Token usage** on a separate line below every response
- Format: `Model: <model> | Tokens: <input> → <output> | Cost: <cost>`
- Example:
  ```
  Response text here...

  Model: zai/glm-4.7-flash | Tokens: 1.2K → 0.3K | Cost: $0.001
  ```

## 🚨 Consumption Alert Rule
After EVERY prompt/response:
- Check session status (`session_status` or read from tool result)
- Alert Mohamad if:
  - Input tokens > 5,000 for a simple query
  - Context growing significantly between turns (>10K increase)
  - Total context > 50% — suggest session reset
- Be proactive — don't wait for him to ask
- **Critical:** If building Docker or running long commands, redirect output to file, don't let logs fill context

## Todo
- [ ] Run qmd embed (when GPU available or time permits)
- [ ] Index more note collections as needed
- [ ] Debug: Mission Control frontend can't reach backend API (network_mode issue)

## Token & Model Display
- Footer is at the bottom of each message
- If you can't see it, let me know — I'll put it at the top
- Shows actual usage for that specific response

## OpenClaw Optimizations
**Current (applied):**
- Memory backend: qmd (BM25, no GPU needed)
- Memory update interval: 15min
- Memory limits: maxResults=2, maxSnippetChars=200, maxInjectedChars=1000
- DM scope: per-channel-peer (not all sessions)
- Session maintenance: 30-day prune, 200 max entries, 10MB rotate, 14-day archive
- Default model: glm-4.7-flash with low reasoning, 1500 maxTokens
- Cache retention: 24h
- GLM-4.7/5: 0 input/output cost (free tier)
- Token budget: 10k session, warning at 8k, alert at 9.5k
- Current session: MiniMax-M2.5, 21k/200k ctx, 66% cached

**Recommended (not yet applied):**
- Reduce flash model maxTokens: 2000 → 1500
- Tighten memory limits: maxSnippetChars 300 → 200, maxInjectedChars 1500 → 1200
- Longer memory update interval: 5m → 10m
- Reduce memory maxResults: 3 → 2

**Agent behavior:**
- Uses memory_search → memory_get (qmd BM25)
- Short, concise responses
- Always includes Model/token footer
- Uses flash for daily, coding for complex work
