#!/bin/bash
BACKUP="$1"
if [ -z "$BACKUP" ]; then echo 'Usage: ./restore-openclaw.sh /path/to/backup.tar.gz'; exit 1; fi
mkdir -p /tmp/restore && cd /tmp/restore
tar -xzf "$BACKUP"
DIR=$(ls -d /tmp/restore/*/ | head -1)
cp "$DIR/openclaw.json" ~/.openclaw/
cp "$DIR/.env" ~/.openclaw/
tar -xzf "$DIR/workspace.tar.gz" -C ~/.openclaw/
tar -xzf "$DIR/agents.tar.gz" -C ~/.openclaw/
tar -xzf "$DIR/skills.tar.gz" -C ~/.openclaw/workspace/
rm -rf ~/.openclaw/credentials && cp -r "$DIR/credentials" ~/.openclaw/
rm -rf ~/.openclaw/identity && cp -r "$DIR/identity" ~/.openclaw/ 2>/dev/null || true
rm -rf ~/.openclaw/telegram && cp -r "$DIR/telegram" ~/.openclaw/ 2>/dev/null || true
rm -rf ~/.openclaw/devices && cp -r "$DIR/devices" ~/.openclaw/ 2>/dev/null || true
crontab "$DIR/crontab.txt" 2>/dev/null || true
systemctl start ollama
echo 'Done! Run: openclaw gateway start'
