#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

# Detect compose command: prefer `docker compose`, fallback to `docker-compose`
compose_cmd()
{
  if docker compose version >/dev/null 2>&1; then
    echo "docker compose"
  elif command -v docker-compose >/dev/null 2>&1; then
    echo "docker-compose"
  else
    echo "ERROR: Neither 'docker compose' nor 'docker-compose' found. Install Docker Desktop." >&2
    exit 1
  fi
}

usage()
{
  cat <<USAGE
Usage:
  $(basename "$0") [-d|--detach] [--build]
  $(basename "$0") down

Options:
  -d, --detach   Run in detached (daemon) mode
  --build        Rebuild the image before starting

Examples:
  # Run attached with logs
  bash $(basename "$0")

  # Run detached
  bash $(basename "$0") -d

  # Stop and remove containers
  bash $(basename "$0") down
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage; exit 0
fi

# Ensure Saved.pkl exists as a file so the bind mount maps correctly
if [[ ! -f "Saved.pkl" ]]; then
  echo "Saved.pkl not found. Creating an empty file for initial run..."
  : > Saved.pkl
fi

CMD=$(compose_cmd)

if [[ ${1:-} == "down" ]]; then
  exec $CMD down
fi

DETACH=""
BUILD=""
for arg in "$@"; do
  case "$arg" in
    -d|--detach) DETACH="-d" ;;
    --build) BUILD="--build" ;;
    *) echo "Unknown argument: $arg" >&2; usage; exit 1 ;;
  esac
done

exec $CMD up $DETACH $BUILD
