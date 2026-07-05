# MEMORY.md (Long-term)

This file is the curated long-term memory. Keep it short and high-signal.

## Index
- [[memory/topics/brainstorm.md]] — Brainstorming system (signals → problems → ideas), Obsidian structure, and cron pipeline.
- [[memory/topics/signal-sourcing.md]] — How we source signals (Reddit subreddits, feed mix Top(week)+New, scoring, link hygiene).
- [[memory/topics/meta.md]] — Meta rules (memory hygiene, reporting formats).
- [[memory/topics/openclaw-ops.md]] — Technical ops notes (cron reliability, filesystem constraints).

## Preferences (high level)
- Allen: concise + proactive, but no proactive monitoring unless requested.
- Always reply in English.
- Do not commit/push to GitHub unless Allen explicitly asks; backups happen via cron.
- YouTube: transcript-first; summarize/translate using transcript only unless asked otherwise.
- Browser: default to most efficient (no browser/headless); only use Browser UI when necessary and close it after.
- TTS: English Edge TTS on-demand (tagged); Cantonese TTS unreliable, prefer English TTS.
- Brainstorm: keep the **08:00 Telegram signal report** in the canonical “Top 10 signals (1–10)” template (see `memory/topics/brainstorm.md`).
- Browser: when a real browser is needed, prefer **agent-browser** (project-local in workspace) over the built-in OpenClaw `browser` tool.
- Skill creation preference: when Allen asks to create/update skills, use Anthropic’s **skill-creator** method/reference first.
- Search policy preference (all agents): Exa first by default; prefer original/primary sources; avoid low-quality SEO pages; use stronger evidence standards for health topics; use transcript-first for YouTube; always honor explicit source/tool requests.
- Obsidian: all agents use the shared default vault `C:\Users\allen\Documents\Obsidian\Lily's vault` (`/mnt/c/Users/allen/Documents/Obsidian/Lily's vault`), but each agent creates/opens its own notes in its own folder by default: `Lily/`, `Moss/`, `Iris/`, `Otis/`.
- Agent creation checklist: when Allen asks to create a new agent, handle all three setup layers: (1) OpenClaw agent + workspace, (2) workspace backup, and (3) Obsidian location/settings.
- Otis agent: agent id `tech`, identity `Otis 🛠️`, workspace `/home/allen6qi/.openclaw/workspace-otis`, GitHub backup repo `Lily007896/otis-workspace`, Obsidian folder `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault/Otis`.
- Valuable AI answers: when Allen wants to save/revisit an answer, save the full polished note in Obsidian and keep only a short pointer/index in memory. Use Lily notes by default, e.g. `Lily/Learning/`.
- OpenClaw release updates: the daily `openclaw-release-check` cron should explain changelog items in plain English with "Simple version", "What it means for you", "Worth knowing", and "My read", avoiding raw technical bullets unless used as supporting notes.

## Promoted From Short-Term Memory (2026-05-18)

<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:2:2 -->
- - Allen set the Obsidian convention for all agents: use the shared default vault `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault`, with per-agent folders `Lily/`, `Moss/`, and `Iris/`; agents should create/open Obsidian notes in their own folder by default unless Allen specifies another location. [score=0.805 recalls=0 avg=0.620 source=memory/2026-05-13.md:2-2]

## Promoted From Short-Term Memory (2026-05-26)

<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:3:4 -->
- - Allen asked for the daily OpenClaw release-check cron to explain updates in the same plain-English style used in chat: "Simple version", "What it means for you", "Worth knowing", and "My read", avoiding overly technical changelog bullets. Updated `scripts/check_openclaw_releases.py` and the `openclaw-release-check` cron payload accordingly. - OpenClaw self-update lesson: direct in-chat updates can kill the active agent turn when the gateway restarts. Use the new `openclaw-self-update` skill and `scripts/openclaw-self-update-detached.sh`; launch the detached updater, then immediately end/yield so recovery happens outside the chat process. Dry-run tested successfully on 2026.5.20. [score=0.857 recalls=0 avg=0.620 source=memory/2026-05-22.md:3-4]

## Promoted From Short-Term Memory (2026-06-23)

<!-- openclaw-memory-promotion:memory:memory/2026-06-19.md:3:4 -->
- Allen asked to update OpenClaw to latest and check the smooth-update skill. Used `openclaw-self-update`; detached update completed from `2026.5.20` to `2026.6.8`, `update_exit=0`, gateway recovered and is running. Verified `openclaw-self-update` skill is ready and helper `scripts/openclaw-self-update-detached.sh` is intact. Remaining doctor warnings: legacy/conflicting codex plugin install metadata, cron command-conversion issues, plaintext secret-bearing config fields, command owner not configured. - After the update, Allen asked about memory settings and approved the small recall cleanup.... [score=0.857 recalls=0 avg=0.620 source=memory/2026-06-19.md:3-4]

## Promoted From Short-Term Memory (2026-07-05)

<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:1:1 -->
- Allen asked to make Otis's workspace backup setup match Lily, Moss, and Iris. Created private GitHub repo `Lily007896/otis-workspace`, added it as `origin` for `/home/allen6qi/.openclaw/workspace-otis`, pushed existing history, committed/pushed current Otis memory changes, and updated Lily's ops memory to record the repo. [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-01.md:1-1]
