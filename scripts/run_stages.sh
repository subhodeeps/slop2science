#!/usr/bin/env bash
# Run a topic's stages in the order its manifest declares.
#
#   scripts/run_stages.sh <topic> [stage|export]
#
# Order comes from symbolic/<topic>/stages.txt, never from a shell glob. Glob order is
# lexical, which silently reorders stages when one is renamed or a tenth is added -- a bug
# the project this template came from actually hit (docs/failure_modes.md). The manifest also
# lets one topic mix languages, which a glob over a single extension cannot.
#
# stages.txt format: one path per line, relative to symbolic/<topic>/; blank lines and
# lines starting with '#' ignored. Export stages are the lines whose basename starts with
# 'export_'.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
topic="${1:?usage: run_stages.sh <topic> [stage|export]}"
kind="${2:-stage}"
dir="$ROOT/symbolic/$topic"
manifest="$dir/stages.txt"

[ -d "$dir" ] || { echo "no directory symbolic/$topic" >&2; exit 66; }
[ -f "$manifest" ] || { echo "no manifest symbolic/$topic/stages.txt (see symbolic/README.md)" >&2; exit 66; }

ran=0
while IFS= read -r line; do
  line="${line%%#*}"; line="$(echo "$line" | xargs || true)"
  [ -z "$line" ] && continue
  base="$(basename "$line")"
  case "$kind" in
    export) [[ "$base" == export_* ]] || continue ;;
    stage)  [[ "$base" == export_* ]] && continue ;;
    *)      echo "unknown kind: $kind (expected stage|export)" >&2; exit 64 ;;
  esac
  [ -f "$dir/$line" ] || { echo "manifest lists a missing file: symbolic/$topic/$line" >&2; exit 66; }
  echo "=== symbolic/$topic/$line"
  "$ROOT/scripts/run" "symbolic/$topic/$line"
  ran=$((ran+1))
done < "$manifest"

[ "$ran" -gt 0 ] || echo "no $kind scripts listed in symbolic/$topic/stages.txt yet"
