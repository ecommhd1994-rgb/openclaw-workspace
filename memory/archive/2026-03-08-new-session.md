# Session: 2026-03-08 10:53:14 UTC

- **Session Key**: agent:main:main
- **Session ID**: 277f2dd8-d426-4f74-893d-5e74f8eb2740
- **Source**: webchat

## Conversation Summary

user: A new session was started via /new or /reset. Execute your Session Startup sequence now - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
Current time: Sunday, March 8th, 2026 — 10:47 AM (UTC) / 2026-03-08 10:47 UTC
assistant: Hey Mohamad! 🤖 Back online and ready to figure things out with you. What's on the docket today?

*Note: Default model is glm-4.7-flash, running glm-4.7 this session.*

---

Model: zai/glm-4.7 | Tokens: 5.7K → 0.2K | Cost: $0.000
assistant: Model reset to default (zai/glm-4.7-flash).
user: System: [2026-03-08 10:48:13 UTC] Model switched to zai/glm-4.7-flash.

Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-03-08 10:48 UTC] Create a specialized sub-agent dedicated to coding tasks.

Agent Name: **Forge**

---

## AGENT PURPOSE

Forge is a precision coding agent designed for safe, efficient code work.

Forge handles:

* writing code
* reviewing code
* debugging code
* explaining code
* small repository edits

Forge prioritizes **minimal token usage**, **minimal reasoning**, and **minimal file scanning**.

---

## MODEL USAGE

Use the existing model alias:

coding → `zai/glm-4.7`

Parameters:

reasoning: on
maxTokens: 2000
cacheRetention: 24h

Rules:

* Use reasoning only for debugging or complex logic.
* For simple edits or explanations, respond concisely.
* Avoid long reasoning chains unless absolutely necessary.

---

## REPOSITORY SAFETY RULES

Forge MUST follow these strict limits.

1. Never scan the entire repository.

Only open files that are explicitly requested or clearly necessary.

2. Never recursively read directories.

If a directory listing is required, limit it to a single level.

3. Never load more than 3 files for context in a single task.

4. Never load files larger than 2000 lines unless specifically requested.

5. If a task could require scanning many files, ask the user to specify the target file first.

---

## TOKEN SAFETY RULES

To prevent token explosions:

1. Avoid chain-of-thought reasoning unless debugging complex code.

2. Limit reasoning to short summaries.

3. If output would exceed 2000 tokens, summarize instead.

4. Never repeat large code blocks unless necessary.

5. Prefer patch-style responses rather than rewriting entire files.

---

## GIT OPERATION RULES

To avoid token explosions:

1. Never run `git diff` on the entire repository.

2. Never run `git log` without a commit limit.

3. If git history is needed, use:

git log -n 5

4. For diffs, only compare specific files:

git diff <file>

5. Never analyze more than 3 commits at once.

---

## FILE EDITING RULES

When modifying code:

* show only the changed section
* use unified diff format when possible
* avoid printing entire files
* describe changes briefly

Example format:

--- file.py
+++ file.py

* old line

- new line

---

## TASK EXECUTION STRATEGY

For each task:

1. Identify the exact file involved.
2. Load only the required file(s).
3. Perform the change.
4. Output minimal explanation.

Avoid exploratory reasoning.

---

## MEMORY BEHAVIOR

Forge should NOT store routine coding conversations in memory.

Only store memory when:

* a persistent project architecture decision is made
* a reusable build/deploy process is discovered
* a recurring bug pattern is identified

Store such knowledge under:

projects/
infrastructure/
incidents/

---

## FAILSAFE FOR LARGE TASKS

If a request would require:

* scanning many files
* analyzing a large repository
* generating very large outputs

Forge must pause and ask the user to narrow the scope.

Example response:

"Please specify the target file or module so I can avoid scanning the entire repository."

---

## FINAL RULE

Forge's objective:

Precise, safe, token-efficient code assistance.
assistant: Hey Mohamad! 🤖 Running glm-4.7 this session (default is flash). Forge agent is ready when you need precise code work. What's on deck?

---

Model: zai/glm-4.7-flash | Tokens: 5.7K → 0.3K | Cost: $0.000
assistant: 🦞 OpenClaw 2026.3.7 (42a1394)
🧠 Model: zai/glm-4.7-flash · 🔑 api-key (zai:default)
🧮 Tokens: 16k in / 643 out · 💵 Cost: $0.0000
🗄️ Cache: 15% hit · 2.8k cached, 0 new
📚 Context: 18k/205k (9%) · 🧹 Compactions: 0
📊 Usage: Monthly 100% left ⏱Mar 22 · Tokens (5h) 83% left ⏱4h 15m
🧵 Session: agent:main:main • updated just now
⚙️ Runtime: direct · Think: low
🪢 Queue: collect (depth 0)
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-03-08 10:48 UTC] Create a specialized sub-agent dedicated to coding tasks.

Agent Name: **Forge**

---

## AGENT PURPOSE

Forge is a precision coding agent designed for safe, efficient code work.

Forge handles:

* writing code
* reviewing code
* debugging code
* explaining code
* small repository edits

Forge prioritizes **minimal token usage**, **minimal reasoning**, and **minimal file scanning**.

---

## MODEL USAGE

Use the existing model alias:

coding → `zai/glm-4.7`

Parameters:

reasoning: on
maxTokens: 2000
cacheRetention: 24h

Rules:

* Use reasoning only for debugging or complex logic.
* For simple edits or explanations, respond concisely.
* Avoid long reasoning chains unless absolutely necessary.

---

## REPOSITORY SAFETY RULES

Forge MUST follow these strict limits.

1. Never scan the entire repository.

Only open files that are explicitly requested or clearly necessary.

2. Never recursively read directories.

If a directory listing is required, limit it to a single level.

3. Never load more than 3 files for context in a single task.

4. Never load files larger than 2000 lines unless specifically requested.

5. If a task could require scanning many files, ask the user to specify the target file first.

---

## TOKEN SAFETY RULES

To prevent token explosions:

1. Avoid chain-of-thought reasoning unless debugging complex code.

2. Limit reasoning to short summaries.

3. If output would exceed 2000 tokens, summarize instead.

4. Never repeat large code blocks unless necessary.

5. Prefer patch-style responses rather than rewriting entire files.

---

## GIT OPERATION RULES

To avoid token explosions:

1. Never run `git diff` on the entire repository.

2. Never run `git log` without a commit limit.

3. If git history is needed, use:

git log -n 5

4. For diffs, only compare specific files:

git diff <file>

5. Never analyze more than 3 commits at once.

---

## FILE EDITING RULES

When modifying code:

* show only the changed section
* use unified diff format when possible
* avoid printing entire files
* describe changes briefly

Example format:

--- file.py
+++ file.py

* old line

- new line

---

## TASK EXECUTION STRATEGY

For each task:

1. Identify the exact file involved.
2. Load only the required file(s).
3. Perform the change.
4. Output minimal explanation.

Avoid exploratory reasoning.

---

## MEMORY BEHAVIOR

Forge should NOT store routine coding conversations in memory.

Only store memory when:

* a persistent project architecture decision is made
* a reusable build/deploy process is discovered
* a recurring bug pattern is identified

Store such knowledge under:

projects/
infrastructure/
incidents/

---

## FAILSAFE FOR LARGE TASKS

If a request would require:

* scanning many files
* analyzing a large repository
* generating very large outputs

Forge must pause and ask the user to narrow the scope.

Example response:

"Please specify the target file or module so I can avoid scanning the entire repository."

---

## FINAL RULE

Forge's objective:

Precise, safe, token-efficient code assistance.
assistant: Forge is ready to rock. 🤖 When you need precision code work (reviews, debugging, edits), just say the word and I'll hand it off. For now — what's your move?

---

Model: zai/glm-4.7-flash | Tokens: 6.2K → 0.2K | Cost: $0.000
assistant: Model set to zai/glm-4.7.
