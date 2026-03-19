# OpenClaw Sandbox Architecture & Security Analysis

## Executive Summary

OpenClaw's sandbox is a Docker-based isolation layer for tool execution that reduces blast radius when AI models execute commands. It runs **optional** containerized tool execution alongside the host-based Gateway, providing filesystem and process isolation.

---

## 1. How the Sandbox Works

### Core Architecture

- **What it is**: Docker container-based isolation for tool execution (`exec`, `read`, `write`, `edit`, `process`, `apply_patch`, etc.)
- **Not sandboxed**: The Gateway itself, tools explicitly allowed via `tools.elevated`
- **When enabled**: Tools run inside containers; Gateway stays on host

### Isolation Model

| Component | Isolation |
|-----------|-----------|
| Tool execution | Docker containers per session/agent/shared |
| Filesystem | Sandboxed workspace (`~/.openclaw/sandboxes/`) or mounted agent workspace |
| Process | Containerized via Docker |
| Network | `none` by default (configurable) |
| Browser | Optional sandboxed browser via CDP |

### Subagent Isolation

- Each **session** gets its own container (default `scope: "session"`)
- Subagents inherit parent workspace automatically via `cwd` mount
- Can force sandbox requirement for children: `sessions_spawn` with `sandbox: "require"`
- Main agent runs outside sandbox by default; non-main sessions (groups/channels) are sandboxed in `non-main` mode

---

## 2. Security Model

### Trust Model

OpenClaw follows a **personal assistant security model**:
- One trusted operator boundary per gateway
- NOT designed for hostile multi-tenant isolation
- For adversarial users: run separate gateways per trust boundary

### Protection Layers

| Layer | Control | What It Does |
|-------|---------|--------------|
| **Identity** | `gateway.auth`, channel allowlists, DM policies | Who can talk to the bot |
| **Scope** | `sandbox.mode`, group policies, mention gating | Where the bot can act |
| **Tool Policy** | `tools.allow/deny`, tool profiles | Which tools are callable |
| **Sandbox** | Docker containers | Limits blast radius of tool execution |
| **Elevated** | `tools.elevated` | Exec-only escape hatch to host |

### Key Security Features

1. **Sandbox modes**:
   - `"off"`: No sandboxing (tools on host)
   - `"non-main"`: Sandbox only non-main sessions (groups/channels) — **default recommended**
   - `"all"`: Every session in sandbox

2. **Workspace access control**:
   - `"none"`: Sandbox workspace only (`~/.openclaw/sandboxes`)
   - `"ro"`: Agent workspace read-only at `/agent`
   - `"rw"`: Agent workspace read/write at `/workspace`

3. **Network isolation**: Default `network: "none"`; blocked: `host`, `container:*`

4. **Bind mount restrictions**: Blocks dangerous paths (`docker.sock`, `/etc`, `/proc`, `/sys`, `/dev`)

5. **Browser security**: noVNC password protection, CIDR-restricted CDP, isolated Chrome flags

### Security Audit

```bash
openclaw security audit
openclaw security audit --deep
```

---

## 3. Configuration Options

### Core Sandbox Keys

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `agents.defaults.sandbox.mode` | string | `"non-main"` | When to sandbox: `"off"`, `"non-main"`, `"all"` |
| `agents.defaults.sandbox.scope` | string | `"session"` | Container allocation: `"session"`, `"agent"`, `"shared"` |
| `agents.defaults.sandbox.workspaceAccess` | string | `"none"` | Filesystem access: `"none"`, `"ro"`, `"rw"` |
| `agents.defaults.sandbox.docker.image` | string | `openclaw-sandbox:bookworm-slim` | Custom container image |
| `agents.defaults.sandbox.docker.network` | string | `"none"` | Container network mode |
| `agents.defaults.sandbox.docker.binds` | array | `[]` | Additional host mounts (`host:container:mode`) |
| `agents.defaults.sandbox.browser.autoStart` | boolean | `true` | Auto-start sandboxed browser |

### Per-Agent Overrides

```json5
{
  agents: {
    list: [
      {
        id: "work",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
      },
    ],
  },
}
```

---

## 4. Practical Recommendations

### For Personal Use

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "rw",
      },
    },
  },
}
```

### For Shared Access / Team Bot

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        scope: "session",
        workspaceAccess: "ro",
      },
    },
    tools: {
      deny: ["group:automation", "gateway", "cron"],
    },
  },
  session: {
    dmScope: "per-channel-peer",
  },
}
```

---

## 5. Debugging

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --json
```

---

## 6. Risks & Limitations

1. **Not a perfect security boundary**: Docker container escape is possible
2. **Bind mounts bypass isolation**: Expose host paths with configured permissions
3. **Main session on host in non-main mode**: Personal chats have full access
4. **Elevated bypasses sandbox**: Grants host exec but respects tool policy
5. **Prompt injection**: Sandbox limits blast radius but doesn't prevent manipulation

---

## Summary

OpenClaw's sandbox provides **practical isolation** via Docker containers, reducing the blast radius of tool execution. It integrates with tool policy and elevated exec for fine-grained control. The `non-main` default balances security for shared sessions while keeping personal assistant use cases simple.
