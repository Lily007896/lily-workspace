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
- Otis agent: agent id `tech`, identity `Otis 🛠️`, workspace `/home/allen6qi/.openclaw/workspace-otis`, Obsidian folder `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault/Otis`.
- Valuable AI answers: when Allen wants to save/revisit an answer, save the full polished note in Obsidian and keep only a short pointer/index in memory. Use Lily notes by default, e.g. `Lily/Learning/`.
- OpenClaw release updates: the daily `openclaw-release-check` cron should explain changelog items in plain English with "Simple version", "What it means for you", "Worth knowing", and "My read", avoiding raw technical bullets unless used as supporting notes.

## Promoted From Short-Term Memory (2026-05-18)

<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:2:2 -->
- - Allen set the Obsidian convention for all agents: use the shared default vault `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault`, with per-agent folders `Lily/`, `Moss/`, and `Iris/`; agents should create/open Obsidian notes in their own folder by default unless Allen specifies another location. [score=0.805 recalls=0 avg=0.620 source=memory/2026-05-13.md:2-2]
