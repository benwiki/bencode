#!/usr/bin/env bash
set -euo pipefail

# Bootstrap a WSL/Ubuntu environment for this repo.
# - Installs system packages needed to build Kivy/Pillow when wheels aren't available.
# - Creates/updates a local venv (.venv) using Python 3.12.
# - Installs Python deps from requirements.txt.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3.12}"
SYSTEM_PYTHON_BIN="${SYSTEM_PYTHON_BIN:-/usr/bin/python3}"
VENV_DIR="${VENV_DIR:-.venv}"
RECREATE_VENV="${RECREATE_VENV:-0}"

usage() {
  cat <<'EOF'
Usage:
  scripts/bootstrap_wsl.sh [--recreate] [--python python3.12]

Env vars:
  PYTHON_BIN=python3.12   (default: python3.12)
  SYSTEM_PYTHON_BIN=/usr/bin/python3 (default: /usr/bin/python3)
  VENV_DIR=.venv          (default: .venv)
  RECREATE_VENV=1         (same as --recreate)

Examples:
  ./scripts/bootstrap_wsl.sh
  ./scripts/bootstrap_wsl.sh --recreate
  PYTHON_BIN=python3.12 ./scripts/bootstrap_wsl.sh --recreate
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --recreate)
      RECREATE_VENV=1
      shift
      ;;
    --python)
      PYTHON_BIN="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if ! grep -qi microsoft /proc/version 2>/dev/null; then
  echo "Warning: this script is intended for WSL, but will continue." >&2
fi

if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo not found. On Ubuntu, install it or run as root." >&2
  exit 1
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python interpreter not found: $PYTHON_BIN" >&2
  echo "Hint: on Ubuntu 24.04, python3.12 is usually available as /usr/bin/python3.12" >&2
  exit 1
fi

if [[ ! -x "$SYSTEM_PYTHON_BIN" ]]; then
  echo "System python not found/executable: $SYSTEM_PYTHON_BIN" >&2
  exit 1
fi

# Ensure apt hooks are healthy (they use system python3).
"$SYSTEM_PYTHON_BIN" -c "import apt_pkg" >/dev/null 2>&1 || {
  echo "System python3 can't import apt_pkg; apt is likely broken. Fix python3 alternatives first." >&2
  exit 1
}

echo "Installing system build deps (requires sudo password if not cached)..."
sudo apt-get update
sudo apt-get install -y \
  autoconf automake libtool gettext \
  build-essential pkg-config \
  git zip unzip \
  openjdk-17-jdk \
  "$PYTHON_BIN"-dev \
  "$PYTHON_BIN"-venv \
  libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev libtiff-dev libwebp-dev \
  libgl1-mesa-dev \
  libavcodec-dev libavformat-dev libswscale-dev

if [[ "$RECREATE_VENV" == "1" ]]; then
  echo "Removing $VENV_DIR"
  rm -rf "$VENV_DIR"
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Creating venv: $VENV_DIR using $PYTHON_BIN"
  "$PYTHON_BIN" -m venv --system-site-packages "$VENV_DIR"
fi

if [[ -f "$VENV_DIR/pyvenv.cfg" ]]; then
  # Enforce the setting even if the venv pre-existed.
  sed -i 's/^include-system-site-packages = .*/include-system-site-packages = true/' "$VENV_DIR/pyvenv.cfg" || true
fi

if [[ -f "$VENV_DIR/pyvenv.cfg" ]] && ! grep -q "^include-system-site-packages = true$" "$VENV_DIR/pyvenv.cfg"; then
  echo "Expected include-system-site-packages = true in $VENV_DIR/pyvenv.cfg" >&2
  echo "Hint: delete the venv and re-run with --recreate." >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

python -V
python -c "import sys; print('venv:', sys.executable)"

echo "Upgrading packaging tooling..."
pip install -U pip setuptools wheel

if [[ -f requirements.txt ]]; then
  echo "Installing Python requirements from requirements.txt"
  pip install -r requirements.txt
else
  echo "requirements.txt not found; skipping pip installs" >&2
fi

echo "Installing buildozer with pip --user (writes to ~/.local/bin)..."
echo "Note: On Ubuntu, system pip may be blocked by PEP 668; using venv pip with --user avoids that."
pip install --user -U buildozer

echo "Ensuring ~/.local/bin is on PATH permanently..."
if ! grep -q "# >>> language_learning local bin >>>" "$HOME/.bashrc" 2>/dev/null; then
  {
    echo
    echo "# >>> language_learning local bin >>>"
    echo "# Added by language_learning/scripts/bootstrap_wsl.sh"
    echo "if [ -d \"$HOME/.local/bin\" ] ; then"
    echo "  case :\"$PATH\": in"
    echo "    *:\"$HOME/.local/bin\":*) ;;"
    echo "    *) export PATH=\"$HOME/.local/bin:$PATH\" ;;"
    echo "  esac"
    echo "fi"
    echo "# <<< language_learning local bin <<<"
  } >> "$HOME/.bashrc"
fi

echo "Done. Activate with: source $VENV_DIR/bin/activate"
echo "Buildozer installed to: $HOME/.local/bin (open a new shell or run: source ~/.bashrc)"
