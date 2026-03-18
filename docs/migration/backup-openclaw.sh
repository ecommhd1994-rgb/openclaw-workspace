#!/bin/bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/tmp/openclaw-backup-$TIMESTAMP"
mkdir -p "$BACKUP_DIR"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp ~/.openclaw/.env "$BACKUP_DIR/"
tar -czf "$BACKUP_DIR/workspace.tar.gz" ~/.openclaw/workspace
tar -czf "$BACKUP_DIR/agents.tar.gz" ~/.openclaw/agents
tar -czf "$BACKUP_DIR/skills.tar.gz" ~/.openclaw/workspace/skills
cp -r ~/.openclaw/credentials "$BACKUP_DIR/"
cp -r ~/.openclaw/identity "$BACKUP_DIR/"
cp -r ~/.openclaw/telegram "$BACKUP_DIR/"
cp -r ~/.openclaw/devices "$BACKUP_DIR/"
crontab -l > "$BACKUP_DIR/crontab.txt"
cd /tmp && tar -czf openclaw-backup-$TIMESTAMP.tar.gz openclaw-backup-$TIMESTAMP
echo Done: /tmp/openclaw-backup-$TIMESTAMP.tar.gz
