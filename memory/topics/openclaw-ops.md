# OpenClaw ops (topic memory)

Technical notes about running/operating OpenClaw on this machine.

## Cron + filesystem constraints
- OpenClaw cron “agent turns” may be restricted by workspace-root file tooling.
- The built-in write tool can fail when writing to paths outside the workspace root (e.g., Obsidian vault under `/mnt/c/...`), with errors like: `Path escapes workspace root`.
- For scheduled collectors/reports that must write into the Obsidian vault, use **workspace-resident scripts** (shell/python3 doing normal filesystem operations) to write to vault paths.

## Cron reliability guidelines
- Keep cron jobs lightweight to avoid timeouts.
- Prefer two-stage pipelines: collect data → save files → generate report from files.
- Avoid relying on `python`; use `python3` explicitly.

## Manual OpenClaw updates from chat
- Use skill `openclaw-self-update` for any "update OpenClaw / update yourself" request.
- Do not run direct `openclaw update` inside chat. Send a brief offline warning, launch `scripts/openclaw-self-update-detached.sh`, then immediately end/yield. The helper runs under `systemd-run --user` and sends completion after restart.
- Incident context: on 2026-05-22, continuing tool work after launching a detached updater killed the active Codex app-server connection when the gateway stopped, even though the update succeeded.

## Agent workspace GitHub backups
- Daily cron: `backup-agent-workspaces-github` at 23:00 Europe/London.
- Script: `~/.openclaw/workspace/scripts/backup-workspaces.sh`.
- Standard repo naming: `<agent-name>-workspace`.
- Current workspace repos and QMD collection names:
  - Lily → `Lily007896/lily-workspace` (`~/.openclaw/workspace`, QMD `lily-workspace`)
  - Moss → `Lily007896/moss-workspace` (`~/.openclaw/workspace-work`, QMD `moss-workspace`)
  - Iris → `Lily007896/iris-workspace` (`~/.openclaw/workspace-iris`, QMD `iris-workspace`)
  - Otis → `Lily007896/otis-workspace` (`~/.openclaw/workspace-otis`, QMD `otis-workspace`)

## Daily memory
- 2026-07-01: Created private GitHub repo `Lily007896/otis-workspace`, set it as `origin` for `~/.openclaw/workspace-otis`, committed/pushed current Otis memory changes, and confirmed the existing `backup-agent-workspaces-github` script already includes Otis.

## Signal pipeline incident (2026-03-03)
- Root cause: 06:00 collector attempted to use OpenClaw write tool to `/mnt/c/...` and failed.
- Fix: move collector + reporter into scripts under `~/.openclaw/workspace/scripts/`.

## QMD retrieval incident (2026-03-03)
- Symptom: `memory_search` returned empty results even for known strings.
- Root cause: QMD had a large embedding backlog (indexed files without vectors), so semantic retrieval was ineffective.
- Fix: ran `qmd update` + `qmd embed`, then scheduled hourly maintenance via cron `qmd-hourly-embed` running `scripts/qmd-maintain.sh`.
- Runbook: when retrieval seems broken, check `qmd status` for pending embeddings.

## Voice toggle implementation
- State file: `~/.openclaw/workspace/state/voice-mode.json`
- Purpose: let Allen switch between text and TTS without prefixing every message.
