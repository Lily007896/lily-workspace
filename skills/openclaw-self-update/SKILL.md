---
name: openclaw-self-update
description: Safely update or upgrade OpenClaw from inside Allen's chat without leaving the system stuck offline. Use this skill whenever Allen asks to update OpenClaw, upgrade OpenClaw, update yourself, update the bot/agent/runtime, install the latest OpenClaw version, recover from an OpenClaw update, or asks whether you can die/restart and recover on your own. This skill is the required guardrail for OpenClaw self-updates from Telegram or any OpenClaw-hosted session.
---

# OpenClaw Self Update

## Goal
Update OpenClaw without repeating the 2026-05-22 incident where the active chat turn was killed mid-response when the gateway restarted.

The important distinction:
- The assistant may go offline briefly while the gateway restarts.
- Allen should not need to manually log into the machine to recover it.
- The detached updater should send Allen a completion message after OpenClaw comes back.

## Required Rule
Do not run `openclaw update` directly from an active OpenClaw chat turn.

Reason: the chat agent is running inside the OpenClaw gateway process tree. A direct update either refuses for safety or stops the gateway that owns the active turn, which closes the Codex app-server connection and surfaces an avoidable "Something went wrong" error.

## Safe Workflow
1. Check the current installed version and the latest available version:
   ```bash
   openclaw --version
   npm view openclaw version dist-tags --json
   ```

2. If already current, tell Allen briefly and stop. Do not launch the updater.

3. If an update is needed, send Allen one short visible message before starting:
   ```text
   I’m starting the OpenClaw update now. I may go offline for a few minutes, but the detached updater should restart OpenClaw and send you a completion message after it comes back.
   ```

4. Launch the tested detached helper from the Lily workspace:
   ```bash
   /home/allen6qi/.openclaw/workspace/scripts/openclaw-self-update-detached.sh
   ```

5. Immediately end/yield the active turn after launching the helper. Do not continue with more tool calls, log checks, or commentary in the same turn.

6. Let the detached systemd unit perform the update, restart the gateway, and send the completion Telegram message.

## Testing Without Restarting
Use dry-run mode when Allen asks to test the mechanism without actually restarting OpenClaw:

```bash
OPENCLAW_UPDATE_DRY_RUN=1 OPENCLAW_UPDATE_NO_SEND=1 /home/allen6qi/.openclaw/workspace/scripts/openclaw-self-update-detached.sh
```

Then verify:
```bash
openclaw --version
openclaw status
ls -lt /home/allen6qi/.openclaw/logs/manual-update-*.log | head
```

The dry run should:
- launch a detached `systemd-run --user` unit
- write a `manual-update-*.log`
- skip the actual `openclaw update`
- suppress Telegram status messages
- leave the gateway reachable

## Recovery Checks
If Allen reports that the update crashed or did not recover, check:
```bash
openclaw --version
openclaw status
systemctl --user status openclaw-gateway.service --no-pager
ls -lt /home/allen6qi/.openclaw/logs/manual-update-*.log | head
tail -200 /tmp/openclaw/openclaw-$(date +%F).log
```

Interpretation:
- If the version changed and the gateway is reachable, the update succeeded and only the active turn was interrupted.
- If the gateway service is inactive, restart it with the normal OpenClaw service mechanism and report the exact failure log to Allen.
- If the detached update log says `update_exit=0`, treat the update itself as successful.

## Communication Style
Keep messages short and operational. Allen mainly needs to know:
- whether an update is needed
- that OpenClaw may go offline briefly
- whether recovery completed
- current installed version after recovery

Avoid long technical changelog detail unless Allen asks.

## Incident Memory
The incident and runbook are also recorded in:
- `/home/allen6qi/.openclaw/workspace/memory/topics/openclaw-ops.md`
- `/home/allen6qi/.openclaw/workspace/memory/2026-05-22.md`

Use those only for background context; this skill is the primary trigger and procedure.
