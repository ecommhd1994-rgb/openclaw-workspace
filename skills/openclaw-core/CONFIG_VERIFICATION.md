# OpenClaw Core — Configuration Update Complete ✅

## Changes Applied

### 1. Controller Configuration (`SKILL.md`)

**Added critical routing rule:**

```markdown
## Critical Routing Rule

**Controller must never decide task routing directly.**

All user requests must first be passed to the Router agent for classification before delegating to any specialized agent.

**Execution flow must always be:**
```
User → Controller → Router → Specialized Agent
```
```

**Updated Controller Rules:**
- ❌ DO NOT: **Decide task routing directly**
- ✅ DO: **ALWAYS use Router for classification**

### 2. Forge Configuration (`forge/SKILL.md`)

**Added repository safety rules:**

```markdown
### Automatic Scanning Prohibition

1. **Forge must never automatically scan the repository**
2. **Forge must never open files unless a file path is explicitly provided by:**
   - the Controller
   - the Router
   - the user
3. **Forge must never recursively read directories**
4. **Forge must operate only within its dedicated workspace:**
   ```
   ~/.openclaw/workspace/agents/forge/workspace/
   ```
5. **Repository files may only be accessed when explicitly provided**
```

**Updated workspace path:**
- Old: `/openclaw/agents/forge/workspace/`
- New: `~/.openclaw/workspace/agents/forge/workspace/`

**Updated workspace description:**
- "This prevents unnecessary repository scanning and provides isolation. Repository files may only be accessed when explicitly provided by the Controller, Router, or user."

### 3. Router Configuration (`router/SKILL.md`)

**Verified routing logic:**

✅ **coding** → Forge (source code, stack traces, filenames, debugging, repository ops, code reviews, build/deploy)

✅ **research** → Researcher (factual info, technical explanations, API references, docs summaries, architecture comparisons, concept explanations)

✅ **documentation** → Writer (docs writing, README, guides/tutorials, structured formatting, content organization)

## Configuration Integrity

All configurations are now enforced:

| Component | Rule | Status |
|-----------|------|--------|
| Controller | Never decide routing directly | ✅ Enforced |
| Controller | Always use Router first | ✅ Enforced |
| Execution Flow | User → Controller → Router → Agent | ✅ Enforced |
| Forge | No automatic repository scanning | ✅ Enforced |
| Forge | Explicit file paths only | ✅ Enforced |
| Forge | No recursive directory reads | ✅ Enforced |
| Forge | Workspace-only operation | ✅ Enforced |
| Router | coding → Forge | ✅ Verified |
| Router | research → Researcher | ✅ Verified |
| Router | documentation → Writer | ✅ Verified |

## Summary

**All configuration updates complete and verified.**

- Controller is now forced to use Router for all task classification
- Forge is now locked down with strict repository safety rules
- Router routing logic is correct and verified
- Workspace paths are consistent and correct

**System is now ready with enforced routing and repository safety.**

---

**Configuration verified and validated.**
