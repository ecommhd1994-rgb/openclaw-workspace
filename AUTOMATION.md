# AUTOMATION.md - Heartbeats & Cron

## Heartbeats
When you receive heartbeat poll, use productively. Don't just reply `HEARTBEAT_OK`.

### Heartbeat vs Cron
**Heartbeat**: Batch multiple checks (inbox + calendar + notifications), conversational context needed, timing can drift (~30min), reduce API calls
**Cron**: Exact timing matters, isolation needed, different model/thinking level, one-shot reminders, deliver to channel directly

### Things to Check (rotate 2-4×/day)
- Emails: Urgent unread?
- Calendar: Upcoming 24-48h?
- Mentions: Social notifications?
- Weather: Relevant?

### When to Reach Out
- Important email arrived
- Calendar event <2h away
- Found something interesting
- >8h since last message

### When to Stay Quiet (HEARTBEAT_OK)
- Late night (23:00-08:00) unless urgent
- Human is clearly busy
- Nothing new since last check
- Checked <30 minutes ago

### Proactive Heartbeat Work
- Read/organize memory files
- Check projects (git status)
- Update documentation
- Commit/push your changes
- Review and update MEMORY.md

### Memory Maintenance (Heartbeats, every few days)
1. Read recent `memory/YYYY-MM-DD.md`
2. Identify significant events/lessons/insights
3. Update `MEMORY.md` with distilled learnings
4. Remove outdated info from MEMORY.md
