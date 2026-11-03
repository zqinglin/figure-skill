#!/usr/bin/env bash
# Install figure-skill into Claude Code and/or Codex skills directories.
#
#   bash install.sh            # both ~/.claude/skills and ~/.codex/skills
#   bash install.sh --claude   # Claude Code only
#   bash install.sh --codex    # Codex only
#
# Safe to re-run: it refreshes an existing install in place.
set -euo pipefail

SKILL_NAME="figure-skill"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

targets=()
case "${1:-both}" in
  --claude) targets=("$HOME/.claude/skills") ;;
  --codex)  targets=("$HOME/.codex/skills") ;;
  both|"")  targets=("$HOME/.claude/skills" "$HOME/.codex/skills") ;;
  *) echo "usage: bash install.sh [--claude|--codex]" >&2; exit 2 ;;
esac

for base in "${targets[@]}"; do
  dest="$base/$SKILL_NAME"
  mkdir -p "$base"
  rm -rf "$dest"
  mkdir -p "$dest/references"
  cp "$SRC_DIR/SKILL.md"                    "$dest/"
  cp "$SRC_DIR/figure_style.py"            "$dest/"
  cp "$SRC_DIR/references/palettes.md"     "$dest/references/"
  cp "$SRC_DIR/references/chart-selection.md" "$dest/references/"
  echo "installed -> $dest"
done

echo "done."
