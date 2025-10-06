#!/usr/bin/env zsh
# Simple helper to activate the Julia environment in this directory and install deps

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v julia > /dev/null 2>&1; then
  echo "Julia not found in PATH. Please install Julia first (e.g. 'brew install julia' or download from julialang.org)"
  exit 2
fi

echo "Using Julia at: $(which julia)"
echo "Activating environment at: $ROOT_DIR"

julia -e "import Pkg; Pkg.activate(\"$ROOT_DIR\"); Pkg.instantiate(); println(\"Done: instantiated environment.\")"

echo "If you want additional common packages (IJulia, Pluto, Revise), run:"
echo "  julia -e 'using Pkg; Pkg.activate(\"$ROOT_DIR\"); Pkg.add([\"IJulia\",\"Pluto\",\"Revise\"])'"

echo "To start a REPL with this environment active, run: julia --project=$ROOT_DIR"
