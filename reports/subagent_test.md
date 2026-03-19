# OpenClaw Architecture Report

## Overview

OpenClaw is a self-hosted multi-channel gateway for AI agents. It bridges chat applications (WhatsApp, Telegram, Discord, iMessage, and more) to AI coding agents, running as a single process on the user's own hardware.

## Main Components

### Gateway
The Gateway is the central hub—the single source of truth for sessions, routing, and channel connections. It runs as one always-on process on a configurable port (default 18789), handling:
- WebSocket control/RPC
- HTTP APIs (OpenAI-compatible endpoints)
- Control UI and hooks
- All channel connections

### Agents
OpenClaw supports multi-agent routing with isolated sessions per agent, workspace, or sender. Each agent can have:
- Custom model configuration (primary + fallbacks)
- Custom tool profiles and permissions
- Dedicated workspace directory
- Per-user or per-channel session scoping

### Tool Layer
First-class typed agent tools replace legacy shell-based skills. Tool access is controlled through profiles:
- `minimal`: session_status only
- `coding`: filesystem, runtime, sessions, memory, image
- `messaging`: messaging tools + session tools
- `full`: no restrictions

Tools can be globally allowed/denied via configuration, with wildcard support and provider-specific restrictions.

## Message Flow

```
Chat apps + plugins → Gateway → Agent → Tools → Response → Gateway → User
```

1. Inbound message arrives from any connected channel
2. Gateway routes to appropriate agent based on session rules
3. Agent processes with tool access per its profile
4. Response flows back through Gateway to the originating channel

## Key Design Decisions

1. **Self-hosted**: Data stays on user's hardware; no dependency on hosted services
2. **Single-process multiplexed port**: Simplifies deployment while handling multiple protocols
3. **Tool security profiles**: Prevent unintended tool access per agent/provider
4. **Hot reload**: Config changes apply without full restarts (hybrid mode)
5. **Session isolation**: Per-peer or per-channel scoping prevents cross-contamination
6. **Multi-channel unification**: One Gateway serves all chat platforms simultaneously
