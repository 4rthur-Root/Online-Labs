#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_NAME="dfir-ubuntu-base"
PACKER_TEMPLATE="ubuntu-dfir.pkr.hcl"
PACKAGE_PATH="dfir-ubuntu-base.box"

fail() {
  echo "[ERROR] $*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

echo "[INFO] Starting box build process..."
cd "$SCRIPT_DIR" || fail "Unable to enter directory: $SCRIPT_DIR"

require_command packer
require_command vagrant

[[ -f "$PACKER_TEMPLATE" ]] || fail "Packer template not found: $PACKER_TEMPLATE"

echo "[INFO] Initializing Packer..."
packer init . || fail "Packer initialization failed"

echo "[INFO] Building box with Packer..."
packer build "$PACKER_TEMPLATE" || fail "Packer build failed"

[[ -f "$PACKAGE_PATH" ]] || fail "Expected box package was not produced: $PACKAGE_PATH"

if vagrant box list | awk '{print $1}' | grep -Fxq "$BOX_NAME"; then
  echo "[INFO] Vagrant box '$BOX_NAME' already exists. Skipping add."
else
  echo "[INFO] Adding Vagrant box '$BOX_NAME'..."
  vagrant box add "$BOX_NAME" "$PACKAGE_PATH" || fail "Failed to add Vagrant box '$BOX_NAME'"
fi

echo "[INFO] Box setup completed successfully."   