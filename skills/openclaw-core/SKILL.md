# OpenClaw Core Skill — Multi-Agent Orchestration

**Purpose:** Token-efficient multi-agent orchestration with Planner → Parallel Workers → Validator pattern using sessions_spawn.

## Architecture

```
User Request
    ↓
Planner (Main Agent)
    ↓
Parallel Workers (via sessions_spawn)
    ↓
Validator (via sessions_spawn)
    ↓
Final Response to User
```

## Phase 1 — PLANNER (YOU)

The main agent acts as the Planner. Your responsibilities:

### 1. Understand the Request

Analyze what the user wants:
- What type of task is it?
- What's the expected output?
- Any constraints or special requirements?

### 2. Classify the Task

Determine task category:

- **CODING** — Writing code, debugging, repository ops
- **RESEARCH** — Information lookup, technical explanations
- **WRITING** — Documentation, guides, structured content
- **GENERAL** — Simple tasks that don't need sub-agents

### 3. Generate Task Brief

Create a concise task brief (max 120 words) containing:
- Task goal
- Relevant user input
- Expected output format

**CRITICAL:** Do NOT include full conversation history. Workers receive ONLY the brief.

### 4. Decide Worker Strategy

Single task type → spawn ONE worker
Multiple capabilities → spawn MULTIPLE workers in parallel

Examples:
- "Explain X" → Research Worker (single)
- "Fix bug Y" → Forge Worker (single)
- "Write README for Z" → Writer Worker (single)
- "Explain this project and document it" → Research Worker + Writer Worker (parallel)

### 5. Spawn Workers (Parallel)

Use `sessions_spawn` for each worker:

**Single Worker:**
```yaml
label: worker
mode: run
runtime: subagent
model: zai/glm-4.7
timeoutSeconds: 60
task: [task brief]
```

**Parallel Workers:**
Spawn each worker independently with the same brief:
- Worker 1: `label: researcher`
- Worker 2: `label: writer`
- Worker 3: `label: forge`

Each receives the same task brief but applies their expertise.

### 6. Wait for All Workers to Complete

Do NOT poll. Wait for completion events to arrive.

### 7. Spawn Validator

Use `sessions_spawn` with:
- `label`: validator
- `mode`: run
- `runtime`: subagent
- `model`: zai/glm-4.7-flash
- `timeoutSeconds`: 30
- `task`: "Task brief: [brief]. Worker outputs: [paste all outputs]. Review, merge relevant results, check for errors. Final response: max 200 words."

### 8. Deliver Validator Output

The validator returns the final merged and verified response. Forward it directly to the user.

## Phase 2 — PARALLEL WORKERS

Workers execute tasks independently using their skill instructions.

### Worker Types

| Task Type | Worker Label | Skill | Model |
|-----------|--------------|-------|-------|
| CODING | forge | openclaw-core/forge | zai/glm-4.7 |
| RESEARCH | researcher | openclaw-core/researcher | zai/glm-4.7 |
| WRITING | writer | openclaw-core/writer | zai/glm-4.7 |

### Spawn Rules

**CODING** → spawn Forge Worker
**RESEARCH** → spawn Research Worker
**WRITING** → spawn Writer Worker
**Multiple types** → spawn all relevant workers in parallel

### Task Brief Format

Workers receive ONLY the planner brief. Example:

```
Task: Explain the difference between REST and GraphQL APIs.
Focus: Key differences in architecture, data fetching, use cases.
Format: Structured comparison with tables and examples.
Output limit: 500 words.
```

### Worker Output Limit

All workers must limit their output to **500 words**.

### Worker Safety Rules

- Avoid recursive directory scanning
- Avoid large repository reads
- Limit file context when handling code
- Keep outputs concise (max 500 words)
- Avoid long reasoning chains unless debugging code

### Parallel Execution

When spawning multiple workers:
- Spawn all workers simultaneously (not sequentially)
- Each worker receives the same task brief
- Workers apply their specialty to the brief
- All workers run in parallel
- Wait for ALL workers to complete before spawning validator

## Phase 3 — VALIDATOR

Validator reviews and merges all worker outputs.

### Validator Responsibilities

- Review all worker outputs
- Check for errors or inconsistencies
- Merge relevant results from multiple workers
- Remove redundancies
- Produce a final verified response

### Validator Input

Validator receives ONLY:
- The planner task brief
- All worker outputs (pasted together)

### Validator Output Limit

Final response must be **max 200 words**.

### Validator Task Format

```
Task brief: [paste brief]
Worker outputs:
[Worker 1 output]
[Worker 2 output]
[etc]

Review all outputs, merge relevant information, check for errors,
remove redundancies. Produce final response (max 200 words).
```

## Token Optimization Rules

To minimize token usage:

✅ DO:
- Workers receive ONLY the planner brief
- NO conversation history forwarded to workers
- Validator processes ONLY worker outputs
- Use concise task briefs (max 120 words)
- Workers limit output to 500 words
- Validator limits output to 200 words

❌ DO NOT:
- Forward conversation history to workers
- Repeat large text blocks
- Send full context to workers
- Allow verbose worker outputs
- Duplicate information unnecessarily

## Execution Flow Summary

```
1. Main agent receives request
2. Planner analyzes and classifies the task
3. Planner generates concise task brief (120 words max)
4. Planner spawns required worker(s) in parallel
5. Workers execute tasks independently (500 words max output)
6. Planner spawns Validator when all workers complete
7. Validator reviews, merges, verifies (200 words max output)
8. Final validated result returned to user
```

## Example: Single Worker

**User:** "Explain the difference between REST and GraphQL APIs"

**Planner:**
1. Classify: RESEARCH
2. Task brief: "Explain REST vs GraphQL APIs. Focus: architecture, data fetching, use cases. Format: structured comparison. Output limit: 500 words."
3. Spawn Research Worker with brief
4. Worker returns [500-word explanation]
5. Spawn Validator with brief + worker output
6. Validator returns [200-word verified summary]
7. Deliver: [final response]

## Example: Parallel Workers

**User:** "Explain this Python project and write documentation for it"

**Planner:**
1. Classify: RESEARCH + WRITING
2. Task brief: "Project: Python CSV CLI tool. Research: explain architecture and features. Write: create README. Focus: clarity, completeness. Output limit: 500 words each."
3. Spawn Research Worker (parallel)
4. Spawn Writer Worker (parallel)
5. Research Worker returns [500-word technical explanation]
6. Writer Worker returns [500-word README]
7. Spawn Validator with brief + both outputs
8. Validator returns [200-word merged documentation]
9. Deliver: [final response]

## Example: Coding Task

**User:** "Fix this Python error: ModuleNotFoundError: No module named requests"

**Planner:**
1. Classify: CODING
2. Task brief: "Fix Python ModuleNotFoundError for 'requests' module. Provide solution and explanation. Output limit: 500 words."
3. Spawn Forge Worker with brief
4. Worker returns [500-word fix]
5. Spawn Validator with brief + worker output
6. Validator returns [200-word verified solution]
7. Deliver: [final response]

## Critical Rules

✅ DO:
- Use sessions_spawn for all sub-agent execution
- Create concise task briefs (max 120 words)
- Spawn workers in parallel when multiple types needed
- Workers limit output to 500 words
- Validator limits output to 200 words
- Wait for ALL workers before spawning validator

❌ DO NOT:
- Forward conversation history to workers
- Spawn workers sequentially when parallel is possible
- Allow verbose worker outputs
- Skip validation
- Poll for sub-agent status

## Token Efficiency Summary

| Component | Token Limit |
|-----------|-------------|
| Planner brief | ~100 tokens |
| Worker output | ~500 words (max) |
| Validator output | ~200 words (max) |
| Total (typical task) | ~1,000-2,000 tokens |

## Testing the System

Run these tests to confirm parallel orchestration:

**Test 1 (Single Worker):** "Explain the difference between REST and GraphQL APIs"
- Expected: Planner → Research Worker → Validator

**Test 2 (Single Worker):** "Fix this Python error: ModuleNotFoundError: No module named requests"
- Expected: Planner → Forge Worker → Validator

**Test 3 (Parallel Workers):** "Create documentation for a Python CLI tool that processes CSV files"
- Expected: Planner → Research Worker + Writer Worker (parallel) → Validator

---

**You are the Planner. Create briefs. Spawn parallel workers. Validate thoroughly.**
