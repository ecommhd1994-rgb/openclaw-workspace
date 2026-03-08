# OpenClaw Core Integration Guide

## Quick Setup

### 1. Enable the Skill

Add to `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "openclaw-core": {
        enabled: true,
        path: "~/.openclaw/workspace/skills/openclaw-core",
      },
    },
  },
}
```

### 2. Configure Controller Behavior

Update your main `AGENTS.md` to add Controller instructions:

```markdown
## OpenClaw Core Controller

When receiving requests:

1. Understand the task
2. Break down into steps
3. For each step:
   - Use Router skill to classify task type
   - Delegate to appropriate sub-agent:
     * Forge for coding/debugging
     * Researcher for information lookup
     * Writer for documentation
4. Combine results into final response

Do NOT perform specialized tasks directly. Always delegate.
```

### 3. Configure Forge Workspace

Ensure Forge workspace exists:

```bash
mkdir -p /openclaw/agents/forge/workspace
```

Add to config:

```json5
{
  agents: {
    defaults: {
      forgeWorkspace: "/openclaw/agents/forge/workspace",
    },
  },
}
```

### 4. Restart OpenClaw

```bash
openclaw gateway restart
```

## Usage Examples

### Coding Task

**User:** "Fix the authentication bug in auth.js"

**Controller Process:**
1. Router → classify as "forge"
2. Delegate to Forge
3. Forge reads auth.js, fixes bug
4. Returns patch
5. Controller provides summary

### Research Task

**User:** "Explain how JWT tokens work"

**Controller Process:**
1. Router → classify as "researcher"
2. Delegate to Researcher
3. Researcher explains JWT
4. Returns concise summary
5. Controller forwards to user

### Documentation Task

**User:** "Write a README for this project"

**Controller Process:**
1. Router → classify as "writer"
2. Delegate to Writer
3. Writer creates README
4. Returns formatted documentation
5. Controller forwards to user

### Complex Task

**User:** "Debug the API error, explain what's wrong, and document the fix"

**Controller Process:**
1. Step 1: Router → researcher (understand error)
2. Step 2: Router → forge (fix the code)
3. Step 3: Router → writer (document the fix)
4. Combine all results
5. Provide complete response

## Token Efficiency

This system saves tokens by:

1. **Router:** Ultra-fast classification (minimal tokens)
2. **Specialization:** Each agent uses optimal model/reasoning
3. **Context isolation:** Sub-agents don't load unnecessary context
4. **Patch editing:** Forge outputs only changes, not full files

## Monitoring

Check token usage per session:

```bash
openclaw status
```

## Troubleshooting

### Router not triggering

Ensure skill is enabled and Router skill is loaded:

```bash
openclaw skills list
```

### Forge workspace not found

Create the directory:

```bash
mkdir -p /openclaw/agents/forge/workspace
```

### Context growing too large

- Reduce maxTokens in agent configs
- Clear session history: `/new`
- Check for memory leaks in skills

## Customization

### Add New Agent

1. Create skill directory: `~/.openclaw/workspace/skills/openclaw-core/<agent-name>/`
2. Create `SKILL.md` with agent rules
3. Update Router skill to route to new agent
4. Restart OpenClaw

### Modify Routing Logic

Edit `~/.openclaw/workspace/skills/openclaw-core/router/SKILL.md`

### Adjust Token Limits

Edit agent SKILL.md files to update:
- maxTokens
- reasoning settings
- memory policies

## Cost Comparison

### Without OpenClaw Core

- Single agent for all tasks
- Full reasoning for every request
- Potential context bloat
- ~2-3x token usage

### With OpenClaw Core

- Specialized agents with minimal reasoning
- Context isolation
- Patch-style outputs
- ~60-70% token reduction

---

**Built for efficiency. Designed for scale.**
