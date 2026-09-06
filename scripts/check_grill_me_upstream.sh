#!/usr/bin/env bash
set -euo pipefail

repo="https://github.com/RobMitt/grill-me-skill.git"
pinned="$(sed -n 's/^- Imported baseline: `\([0-9a-f]\{40\}\)`$/\1/p' skills/grill-me/UPSTREAM.md)"
latest="$(git ls-remote "$repo" refs/heads/main | awk '{print $1}')"

if [[ -z "$pinned" || -z "$latest" ]]; then
  printf 'Unable to resolve grill-me upstream provenance.\n' >&2
  exit 2
fi

printf 'pinned=%s\nlatest=%s\n' "$pinned" "$latest"
if [[ "$pinned" == "$latest" ]]; then
  printf 'grill-me upstream: current\n'
else
  printf 'grill-me upstream: update available\n'
fi
