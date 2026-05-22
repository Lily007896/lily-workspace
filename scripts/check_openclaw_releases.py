#!/usr/bin/env python3
"""Check GitHub Releases for openclaw/openclaw and write impact-focused daily notes.

- Writes to: <Vault>/Clawbot/OpenClaw Updates/Daily/YYYY-MM-DD.md
- Keeps state in: ~/.openclaw/workspace/state/openclaw-releases.json
- Skips writing anything if no new releases since last seen.

Heuristics:
- Ignore routine bug-fix bullets.
- Keep: new features, breaking changes, deprecations, config/ops changes, security, migrations.
- Translate technical release bullets into Allen-facing impact summaries.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = "openclaw/openclaw"
API_URL = f"https://api.github.com/repos/{REPO}/releases?per_page=10"

VAULT_DIR = Path("/mnt/c/Users/allen/Documents/Obsidian/Lily's vault")
OUT_DIR = VAULT_DIR / "Clawbot" / "OpenClaw Updates" / "Daily"
STATE_PATH = Path(os.environ.get("OPENCLAW_WORKSPACE_DIR", str(Path.home() / ".openclaw" / "workspace"))) / "state" / "openclaw-releases.json"

IMPORTANT_KEYWORDS = [
    "breaking",
    "deprecat",
    "migration",
    "upgrade",
    "config",
    "gateway",
    "cron",
    "scheduler",
    "auth",
    "token",
    "permission",
    "security",
    "vulnerability",
    "model",
    "tool",
    "api",
    "protocol",
    "database",
    "storage",
]

BUGFIX_ONLY_PAT = re.compile(r"\b(fix|fixed|fixes|bug|typo|minor|cleanup|refactor|lint)\b", re.I)
FEATURE_PAT = re.compile(r"\b(add|added|new|introduc|support|enable|feature)\b", re.I)


PLAIN_CATEGORIES = [
    (
        "Messaging and replies",
        ["telegram", "discord", "whatsapp", "message", "reply", "delivery", "channel", "dm", "topic", "forum", "tts"],
        "Replies and channel messages should be more reliable, with less chance of messages landing in the wrong place or disappearing into internal output.",
    ),
    (
        "Background jobs and cron",
        ["cron", "scheduler", "scheduled", "heartbeat", "background"],
        "Scheduled jobs should interfere less with normal chat and should be easier to diagnose when something goes wrong.",
    ),
    (
        "Updates and restarts",
        ["update", "restart", "gateway", "doctor", "install", "npm", "node", "service", "windows", "docker", "podman"],
        "Updating OpenClaw and restarting the Gateway should be safer, with fewer stuck or half-updated states.",
    ),
    (
        "Agent behavior",
        ["agent", "codex", "subagent", "openai", "anthropic", "claude", "gemini", "model", "provider", "tool", "schema"],
        "Agents should make fewer tool mistakes, route work more cleanly, and recover better from stale sessions or model quirks.",
    ),
    (
        "Memory and search",
        ["memory", "search", "embedding", "vector", "qmd", "sqlite"],
        "Memory/search should feel less likely to stall or return confusing degraded results.",
    ),
    (
        "Browser automation",
        ["browser", "modal", "dialog", "evaluate", "tab", "url"],
        "Browser automation should handle popups and slower page scripts better.",
    ),
    (
        "Mac app and UI",
        ["mac app", "settings", "control ui", "dashboard", "sidebar", "pane", "menu", "dock", "canvas"],
        "The desktop UI should be cleaner and less confusing, especially around Settings and status screens.",
    ),
    (
        "Mobile and voice",
        ["android", "ios", "voice", "talk", "realtime", "audio", "mic"],
        "Mobile and voice features should behave more smoothly, especially realtime talk mode and onboarding.",
    ),
    (
        "Plugins and skills",
        ["plugin", "plugins", "skill", "skills", "mcp", "clawhub"],
        "Plugins and skills should be easier to install, manage, and recover when something is misconfigured.",
    ),
    (
        "Security and permissions",
        ["auth", "oauth", "token", "permission", "scope", "security", "secret", "credential", "allowlist", "deny"],
        "Access control and credentials should be stricter and clearer, reducing accidental exposure or confusing permission failures.",
    ),
]

WARNING_PATTERNS = [
    (re.compile(r"\bminimum supported Node\.?js|minimum .*Node|Node\.?js .*22", re.I), "This release may require a newer Node.js 22 version. If updates fail later, check Node first."),
    (re.compile(r"\bbreaking\b|\bmigration\b|\bdeprecat", re.I), "There may be compatibility or migration work for advanced/custom setups."),
    (re.compile(r"\bconfig\b|\bprotocol\b|\bapi\b", re.I), "If you maintain custom config, plugins, or scripts, skim the linked release notes before changing those pieces."),
    (re.compile(r"\bpermission\b|\bscope\b|\bauth\b|\boauth\b|\btoken\b", re.I), "If login or tool permissions act differently, it may be due to stricter auth handling rather than a broken install."),
]


def _http_json(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "openclaw-update-check/1.0",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _load_state() -> dict:
    try:
        return json.loads(STATE_PATH.read_text("utf-8"))
    except FileNotFoundError:
        return {"last_seen_tag": None}
    except Exception:
        return {"last_seen_tag": None}


def _save_state(tag: str | None):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"last_seen_tag": tag}, indent=2) + "\n", "utf-8")


def _looks_important(line: str) -> bool:
    s = line.strip().lower()
    if not s:
        return False
    if any(k in s for k in IMPORTANT_KEYWORDS):
        return True
    if FEATURE_PAT.search(s):
        return True
    # keep security even if phrased like a fix
    if "security" in s:
        return True
    return False


def _filter_body(md: str) -> list[str]:
    """Return important bullets/lines from release notes body."""
    lines = [l.rstrip() for l in md.splitlines()]
    out: list[str] = []

    for l in lines:
        s = l.strip()
        if not s:
            continue

        # Keep headings if they signal importance
        if s.startswith("#"):
            if _looks_important(s):
                out.append(s)
            continue

        is_bullet = s.startswith(('-', '*')) or re.match(r"^\d+\.", s)
        if is_bullet:
            # drop pure bugfix bullets unless they look important
            if BUGFIX_ONLY_PAT.search(s) and not _looks_important(s):
                continue
            if _looks_important(s) or not BUGFIX_ONLY_PAT.search(s):
                out.append(s)
        else:
            # keep short impactful lines that look like changes
            if _looks_important(s) and len(s) <= 200:
                out.append(s)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for l in out:
        key = l.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(l)

    return deduped[:40]


def _clean_note(line: str) -> str:
    line = re.sub(r"^\s*[-*]\s*", "", line.strip())
    line = re.sub(r"\s*\(#\d+[^)]*\)\s*", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def _plain_summary(lines: list[str]) -> tuple[str, list[tuple[str, str]], list[str]]:
    """Return simple version, impact bullets, and warnings for a release."""
    cleaned = [_clean_note(l) for l in lines if _clean_note(l)]
    if not cleaned:
        return (
            "This looks mostly like a maintenance release. No major user-facing change stood out from the release notes.",
            [("General stability", "Mostly small fixes and cleanup. You probably do not need to change how you use OpenClaw.")],
            [],
        )

    lowered = "\n".join(cleaned).lower()
    impacts: list[tuple[str, str]] = []
    for title, keywords, summary in PLAIN_CATEGORIES:
        if any(k in lowered for k in keywords):
            impacts.append((title, summary))

    if not impacts:
        impacts.append(("General stability", "This release appears to be mostly behind-the-scenes polish, bug fixes, and reliability work."))

    feature_count = sum(1 for l in cleaned if FEATURE_PAT.search(l))
    warning_count = sum(1 for l in cleaned if any(p.search(l) for p, _ in WARNING_PATTERNS))

    if warning_count:
        simple = "This update includes reliability work plus a few compatibility-sensitive changes. Most of it is internal, but custom setups may need attention."
    elif feature_count >= 4:
        simple = "This update adds several useful capabilities, but most are still practical quality-of-life improvements rather than a new way to use OpenClaw."
    else:
        simple = "This is mostly a reliability and polish update. Day to day, it should make OpenClaw feel a bit steadier rather than noticeably different."

    warnings = []
    for pat, warning in WARNING_PATTERNS:
        if any(pat.search(l) for l in cleaned) and warning not in warnings:
            warnings.append(warning)

    return simple, impacts[:8], warnings[:4]


def _plain_block(title: str, lines: list[str], url: str = "") -> str:
    simple, impacts, warnings = _plain_summary(lines)
    out = []
    out.append(f"OpenClaw update: {title}\n\n")
    out.append(f"Simple version: {simple}\n\n")
    out.append("What it means for you:\n")
    for heading, summary in impacts:
        out.append(f"- {heading}: {summary}\n")
    if warnings:
        out.append("\nWorth knowing:\n")
        for warning in warnings:
            out.append(f"- {warning}\n")
    out.append("\nMy read: you usually do not need to learn anything new for this update. Treat it as improved reliability unless you run custom plugins, custom config, or unusual hosting.\n")
    if url:
        out.append(f"\nSource: {url}\n")
    return "".join(out)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    state = _load_state()
    last_seen = state.get("last_seen_tag")

    releases = _http_json(API_URL)
    if not isinstance(releases, list) or not releases:
        print("No releases found (API returned empty).")
        return 0

    # GitHub returns newest first
    new_releases = []
    for r in releases:
        tag = r.get("tag_name")
        if not tag:
            continue
        if last_seen and tag == last_seen:
            break
        # skip drafts/prereleases
        if r.get("draft") or r.get("prerelease"):
            continue
        new_releases.append(r)

    if not new_releases:
        # Intentionally print nothing so the cron job can stay silent.
        return 0

    today = dt.datetime.now(dt.timezone.utc).astimezone().date().isoformat()
    note_path = OUT_DIR / f"{today}.md"

    blocks = []
    blocks.append(f"# OpenClaw Updates — {today}\n")
    blocks.append(f"Source: https://github.com/{REPO}/releases\n")

    # Oldest first for readability
    for r in reversed(new_releases):
        name = (r.get("name") or r.get("tag_name") or "(untitled)").strip()
        tag = (r.get("tag_name") or "").strip()
        url = (r.get("html_url") or "").strip()
        pub = (r.get("published_at") or "").strip()
        body = r.get("body") or ""

        important = _filter_body(body)

        blocks.append("---\n")
        blocks.append(f"## {name}\n")
        blocks.append(f"- Tag: `{tag}`\n")
        if pub:
            blocks.append(f"- Published: {pub}\n")
        if url:
            blocks.append(f"- Link: {url}\n")

        blocks.append("\n### Plain-English impact summary\n")
        blocks.append(_plain_block(name, important, url))
        blocks.append("\n")

        if important:
            blocks.append("\n### Technical notes used for the summary\n")
            for l in important:
                blocks.append(f"{l}\n")
        else:
            blocks.append("\n### Technical notes used for the summary\n")
            blocks.append("(No obvious impact-relevant items found; release appears mostly bug-fix / maintenance.)\n")

    note_path.write_text("".join(blocks), "utf-8")

    # update last seen to newest tag (even if multiple)
    newest_tag = next((r.get("tag_name") for r in releases if r.get("tag_name")), None)
    _save_state(newest_tag)

    # Print a short message that a cron agent can forward to Telegram.
    newest_names = [((r.get("name") or r.get("tag_name") or "").strip()) for r in new_releases]
    newest_names = [n for n in newest_names if n]
    latest_release = new_releases[0]
    latest_title = (latest_release.get("name") or latest_release.get("tag_name") or "").strip()
    latest_url = (latest_release.get("html_url") or "").strip()

    # Pull a few impact lines from the latest release only for the chat message
    latest_important = _filter_body(latest_release.get("body") or "")
    latest_important = [l for l in latest_important if l.strip()][:8]

    msg_lines = []
    msg_lines.append(f"OpenClaw release update: {len(new_releases)} new release(s) detected\n")
    if latest_title:
        msg_lines.append(_plain_block(latest_title, latest_important, latest_url).rstrip())
    else:
        msg_lines.append(_plain_block("latest release", latest_important, latest_url).rstrip())
    msg_lines.append(f"\n\nVault note: {note_path}")

    print("\n".join(msg_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
