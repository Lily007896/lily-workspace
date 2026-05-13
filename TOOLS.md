# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Obsidian

- Shared default vault:
  - WSL path: `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault`
  - Windows path: `C:\Users\allen\Documents\Obsidian\Lily's vault`
- Agent folders:
  - Lily: `Lily/`
  - Moss: `Moss/`
  - Iris: `Iris/`
- Lily should create/open Obsidian notes in `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault/Lily` by default unless Allen explicitly names another location.
