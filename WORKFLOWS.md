# WORKFLOWS.md - Repeatable Procedures

This file stores repeatable procedures for common tasks.

---

## Example Workflow: Backup OpenClaw

1. Run: `openclaw backup create --verify`
2. Verify archive was created successfully
3. Store backup path in MEMORY.md if significant

---

## Example Workflow: Debug Agent Failure

1. Inspect logs: `openclaw logs --agent <agent-name>`
2. Check agent sessions: `sessions_list`
3. Verify config: `openclaw status`
4. Restart service if needed: `openclaw gateway restart`

---

## Example Workflow: Research Task

1. Parse the research question
2. Spawn researcher subagent with `runtime="subagent"` or `runtime="acp"`
3. Provide clear research scope and output format
4. Summarize results for the user
5. Save key findings to memory/YYYY-MM-DD.md

---

## Example Workflow: Session Reset

1. Alert user about context size
2. Confirm reset is okay
3. End session gracefully
4. User starts fresh session

---

## Example Workflow: Update Workspace Files

1. Read current file content
2. Create backup (optional but recommended)
3. Write new content
4. Verify changes applied correctly
5. Do NOT modify config files

---

## Example Workflow: Cron Job Setup

1. Define job schedule (cron expression or interval)
2. Choose session target (main/isolated)
3. Set payload type (systemEvent/agentTurn)
4. Add delivery mode (announce/webhook/none)
5. Register with: `cron add`
