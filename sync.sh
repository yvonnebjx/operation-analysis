#!/usr/bin/env bash
# sync.sh — Sync latest skill files from Accio agent-core to this repo
#
# Usage:
#   bash sync.sh        # Copy from default agent-core path
#   bash sync.sh -f     # Copy and then commit+push to git
#
# Modify AGENT_SKILLS_DIR below if your agent-core path is different.

set -euo pipefail

AGENT_SKILLS_DIR="$HOME/.accio/accounts/1749485990/agents/DID-F456DA-81F456DAU1777909-6587-476156/agent-core/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Syncing from: $AGENT_SKILLS_DIR"
echo "Syncing to:   $REPO_DIR"

SKILLS=("financial-report-visualizer" "category-management-matrix" "cbec-operating-analysis")

for skill in "${SKILLS[@]}"; do
    src="$AGENT_SKILLS_DIR/$skill"
    dst="$REPO_DIR/$skill"
    if [ -d "$src" ]; then
        ditto "$src" "$dst"
        echo "  ✓ $skill"
    else
        echo "  ✗ $skill (not found in agent-core)"
    fi
done

# Check if --commit flag is passed
if [ "${1:-}" = "-f" ]; then
    cd "$REPO_DIR"
    git add -A
    if ! git diff --cached --quiet; then
        git commit -m "sync: update skills from agent-core ($(date '+%Y-%m-%d %H:%M'))"
        git push
        echo "✓ Committed and pushed."
    else
        echo "No changes to commit."
    fi
fi

echo "Done."
