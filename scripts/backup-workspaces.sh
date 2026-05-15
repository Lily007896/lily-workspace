#!/usr/bin/env bash
set -euo pipefail

# Backup all personal-agent workspaces.
# - Lily workspace repo: ~/.openclaw/workspace
# - Moss workspace repo: ~/.openclaw/workspace-work
# - Iris workspace repo: ~/.openclaw/workspace-iris
# - Otis workspace repo: ~/.openclaw/workspace-otis
#
# This script commits + pushes changes if any. If a newer workspace has no
# remote yet, it still creates a local commit and prints a clear setup warning.

backup_repo() {
  local dir="$1"
  local label="$2"

  if [[ ! -d "$dir" ]]; then
    echo "[$label] Missing dir: $dir" >&2
    return 2
  fi

  pushd "$dir" >/dev/null

  # Ensure we're on a branch and have a remote.
  local branch
  branch="$(git branch --show-current)"
  if [[ -z "$branch" ]]; then
    echo "[$label] Not on a branch (detached HEAD)." >&2
    popd >/dev/null
    return 2
  fi

  local has_origin=1
  git remote get-url origin >/dev/null 2>&1 || has_origin=0

  git add -A

  if git diff --cached --quiet; then
    echo "[$label] No changes." 
    popd >/dev/null
    return 0
  fi

  local stamp
  stamp="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  git commit -m "${label} backup ${stamp}" >/dev/null || true
  if [[ "$has_origin" -eq 1 ]]; then
    git push -u origin "$branch" >/dev/null
    echo "[$label] Backed up to origin/${branch} (${stamp})."
  else
    echo "[$label] Local backup commit only (${stamp}); missing git remote 'origin'." >&2
  fi

  popd >/dev/null
}

# Backup Lily + Moss + Iris + Otis (workspace repos only)
LILY_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
backup_repo "$LILY_DIR" "lily-workspace"
backup_repo "$HOME/.openclaw/workspace-work" "moss-workspace"
backup_repo "$HOME/.openclaw/workspace-iris" "iris-workspace"
backup_repo "$HOME/.openclaw/workspace-otis" "otis-workspace"
