#!/usr/bin/env bash
set -euo pipefail

# Launch OpenClaw updates outside the gateway process tree.
# Important: after starting a real update from chat, end/yield the active turn.
#
# Test mode:
#   OPENCLAW_UPDATE_DRY_RUN=1 OPENCLAW_UPDATE_NO_SEND=1 ./scripts/openclaw-self-update-detached.sh

OPENCLAW_BIN="${OPENCLAW_BIN:-/home/allen6qi/.npm-global/bin/openclaw}"
UNIT="openclaw-manual-update-$(date +%s)"
RUNNER="/tmp/${UNIT}.sh"

if [[ ! -x "$OPENCLAW_BIN" ]]; then
  echo "OpenClaw binary not found or not executable: $OPENCLAW_BIN" >&2
  exit 1
fi

if ! command -v systemd-run >/dev/null 2>&1; then
  echo "systemd-run is required for detached self-update recovery." >&2
  exit 1
fi

cat >"$RUNNER" <<'SH'
#!/usr/bin/env bash
set -u

OPENCLAW_BIN="${OPENCLAW_BIN:-/home/allen6qi/.npm-global/bin/openclaw}"
LOG="$HOME/.openclaw/logs/manual-update-$(date +%Y%m%d-%H%M%S).log"
TARGET="${OPENCLAW_UPDATE_TARGET:-8508259382}"
ACCOUNT="${OPENCLAW_UPDATE_ACCOUNT:-default}"
CHANNEL="${OPENCLAW_UPDATE_CHANNEL:-telegram}"
DRY_RUN="${OPENCLAW_UPDATE_DRY_RUN:-0}"
NO_SEND="${OPENCLAW_UPDATE_NO_SEND:-0}"

mkdir -p "$(dirname "$LOG")"

send_status() {
  local msg="$1"
  if [[ "$NO_SEND" == "1" ]]; then
    echo "status_message_suppressed: $msg"
    return 0
  fi
  "$OPENCLAW_BIN" message send \
    --channel "$CHANNEL" \
    --account "$ACCOUNT" \
    --target "$TARGET" \
    --message "$msg" >/dev/null 2>&1 || true
}

{
  echo "== start $(date -Is) =="
  echo "dry_run=$DRY_RUN"
  echo "before: $("$OPENCLAW_BIN" --version 2>&1)"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "dry run: skipping openclaw update"
    rc=0
  else
    "$OPENCLAW_BIN" update --yes --json
    rc=$?
  fi
  echo "update_exit=$rc"
  echo "after: $("$OPENCLAW_BIN" --version 2>&1)"
  "$OPENCLAW_BIN" status || true
  echo "== end $(date -Is) =="
} >"$LOG" 2>&1

rc=1
if grep -q 'update_exit=0' "$LOG"; then
  rc=0
fi

version="$("$OPENCLAW_BIN" --version 2>&1 | tr '\n' ' ')"
if [[ "$rc" -eq 0 ]]; then
  send_status "OpenClaw update finished successfully. Current version: $version"
else
  send_status "OpenClaw update did not finish cleanly. Current version: $version Log: $LOG"
fi

exit "$rc"
SH

chmod +x "$RUNNER"

systemd-run --user \
  --unit="$UNIT" \
  --collect \
  --setenv=OPENCLAW_BIN="$OPENCLAW_BIN" \
  --setenv=OPENCLAW_UPDATE_DRY_RUN="${OPENCLAW_UPDATE_DRY_RUN:-0}" \
  --setenv=OPENCLAW_UPDATE_NO_SEND="${OPENCLAW_UPDATE_NO_SEND:-0}" \
  --setenv=OPENCLAW_UPDATE_TARGET="${OPENCLAW_UPDATE_TARGET:-8508259382}" \
  --setenv=OPENCLAW_UPDATE_ACCOUNT="${OPENCLAW_UPDATE_ACCOUNT:-default}" \
  --setenv=OPENCLAW_UPDATE_CHANNEL="${OPENCLAW_UPDATE_CHANNEL:-telegram}" \
  "$RUNNER"

echo "Started detached OpenClaw update unit: $UNIT"
echo "Runner: $RUNNER"
