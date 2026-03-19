# Memory Stability Test — Summary

**Source:** `reports/memory_test_facts.md`  
**Read-back verified:** 2026-03-19 20:58 UTC

---

## 5 Facts Extracted and Verified

1. **Gateway Port** — OpenClaw gateway listens on port 18789
2. **Model Context** — MiniMax M2.7 supports a 200,000 token context window
3. **Telegram Security** — Group policy set to allowlist (locked down from open)
4. **Compaction Threshold** — Memory compaction triggers at 160K tokens (80% of available context)
5. **Memory Retrieval** — QMD configured to return max 5 results with 600 character snippets per result

---

## Summary

All 5 facts were written to the source file, read back successfully without modification, and accurately summarized here. No data loss, corruption, or truncation observed across the write-read-write cycle. Memory persistence is stable for file-based storage.

---

*Test confirms: file write → read → summarize chain completes without context reset or data loss*
