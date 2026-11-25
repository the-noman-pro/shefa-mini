#!/usr/bin/env bash
# Posts one line to Slack: notify-slack.sh <success|failure|cancelled> <text>
# Skips quietly when SLACK_WEBHOOK_URL is empty (PRs from forks get no secrets).
set -euo pipefail

if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
  echo "SLACK_WEBHOOK_URL is not set, skipping"
  exit 0
fi

case "$1" in
  success) icon=":white_check_mark:" ;;
  failure) icon=":x:" ;;
  *) icon=":warning:" ;;
esac

run_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
jq -n --arg text "$icon $2 <$run_url|run ${GITHUB_RUN_NUMBER}>" '{text: $text}' |
  curl -fsS -X POST -H 'Content-Type: application/json' --data @- "$SLACK_WEBHOOK_URL"
