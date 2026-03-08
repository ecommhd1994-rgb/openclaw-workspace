# Infrastructure Runbook

Operational commands for server and OpenClaw environment.

## Server Commands

### System Status
```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep -E "node|docker|openclaw"
```

### OpenClaw Service
```bash
# Gateway status
openclaw gateway status

# Restart gateway
openclaw gateway restart

# View logs
openclaw gateway logs
```

### Docker
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container logs
docker logs <container-name>

# Restart container
docker restart <container-name>
```

## OpenClaw Configuration

### Models
```bash
# List available models
/models

# Switch model (current session)
/model <provider/model>

# View model status
/model status
```

### Memory
```bash
# Workspace location
/root/.openclaw/workspace

# Memory files
memory/YYYY-MM-DD.md  # Daily logs
MEMORY.md             # Long-term
projects/*.md         # Project knowledge
infrastructure/*.md   # Operational
incidents/debugging.md # Solved issues
```

## Networking

### Ports
- Document any services and their ports here

### Firewall
```bash
# List firewall rules (ufw example)
sudo ufw status
```

## Backup

### Important Files
- /root/.openclaw/workspace/ (entire workspace)
- /root/.openclaw/config/ (OpenClaw config)

### Backup Frequency
- Document backup schedule here

## Recovery Procedures

Add recovery steps for common issues here.

---

_Last updated: 2026-03-08_
