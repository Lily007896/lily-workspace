---
name: daily-idea-candidate-scan
description: Daily scan for app ideas using the “validated apps (1% better)” methodology. Pull candidate projects from X/Twitter (via web search), Product Hunt, and Reddit (r/SideProject + r/AppIdeas). Filter out crypto. Output a Top 3 candidate list with traction/traffic hints and maintenance risk. Write the results into Allen’s Lily Obsidian vault under Brainstorm/Signals/IdeaCandidates/_raw/YYYY-MM-DD.md.
---

# Daily Idea Candidate Scan (Allen)

## Defaults (Allen)
- Audience: mixed (B2B/B2C)
- Exclude categories: **crypto** (hard exclude)
- Time budget: not specified (prefer simple/low-maintenance projects)
- Delivery time: 08:00 Europe/London (handled by cron job)

## Search order
Use this search order:
1. **Exa first** when `EXA_API_KEY` is available
2. **Brave Search / web_search fallback** when Exa is weak or unavailable
3. **Direct page fetches** to verify claims or extract details

## Sources (required)
Scan these sources (best-effort):
1) **X/Twitter**: use search queries for build-in-public + revenue proof (MRR/Stripe).
2) **Product Hunt**: search for today/recent Product Hunt launches/trending.
3) **Reddit**: r/SideProject and r/AppIdeas (use search and/or Reddit JSON listing endpoints).

## Output
Produce **Top 3 candidates** only, ranked in descending order of conviction (**#1 best**, then **#2**, then **#3**).
For each candidate include:
- Name (or best-guess product name)
- Link
- Source (X / Product Hunt / Reddit)
- What it is (1–2 lines)
- Traction evidence (exact quote if available: MRR/Stripe/users/pricing/testimonials)
- Traffic / acquisition hypothesis (ads / SEO / community / affiliates)
- Maintenance risk (low/med/high + why)
- “1% better” wedge (one concrete angle)
- Why this is a strong opportunity for Allen

## Filtering rules
- Hard exclude if crypto-related.
- Prefer candidates with:
  - revenue proof (MRR/Stripe) OR clear paid pricing + positive user evidence
  - simple workflow + low ops burden
- Rank aggressively and keep only the **best 3**.

## Storage (required)
Write a single markdown note to:
- `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault/Brainstorm/Signals/IdeaCandidates/_raw/YYYY-MM-DD.md`

The note format:
- Title: `Idea Candidates — YYYY-MM-DD`
- Then Top 3 numbered list with the fields above.

## Telegram delivery (required)
- After writing the vault note, output the **full Top 3 list** in the same markdown format to the chat (no streaming).

## Implementation guidance
- Prefer Exa for discovery when available.
- Use Brave/web_search as fallback when Exa is weak or unavailable.
- Use direct fetches for detail verification where useful.
- Keep the note skimmable; avoid long essays.
- Strong filtering is better than broad coverage.
