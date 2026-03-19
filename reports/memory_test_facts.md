# Test Facts — Memory Stability Test
# 2026-03-19 20:58 UTC

1. OpenClaw gateway runs on port 18789
2. MiniMax M2.7 has a 200K token context window
3. Telegram channel uses allowlist group policy
4. Compaction fires at 160K tokens (80% of context)
5. QMD memory returns max 5 results with 600 char snippets
