#!/usr/bin/env bash
# Installs the remaining DFIR analysis tools on the Ubuntu VM:
#   1. Docker CE + Docker Compose        (https://docs.docker.com/engine/install/ubuntu/)
#   2. TimeSketch                        (https://timesketch.org/guides/admin/install/)
#   3. .NET runtime + Eric Zimmerman's Tools (net9 builds) into /opt/EZTools
#   4. Splunk manual instructions (license/URL churn makes scripting unreliable)
#
# Run as root inside the VM:
#   sudo bash /home/vagrant/Tools/install_vm_tools.sh
# (or from the host: make tools)

set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "ERROR: Please run this script as root."
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { echo "[$(date +'%H:%M:%S')] $*"; }

# Docker
log "Step 1/4: Installing Docker CE + Compose"
if ! command -v docker >/dev/null 2>&1; then
  bash "$SCRIPT_DIR/docker.sh"
else
  log "Docker already installed: $(docker --version)"
fi

# Let the vagrant user drive docker without sudo.
usermod -aG docker vagrant 2>/dev/null || true

# TimeSketch
log "Step 2/4: Deploying TimeSketch"
cd /home/vagrant
if [ -d ./timesketch ]; then
  log "TimeSketch already deployed (timesketch/ exists) - skipping."
else
  bash "$SCRIPT_DIR/deploy_timesketch.sh" --start-container --skip-create-user
fi

# .NET + EZ Tools
log "Step 3/4: Installing .NET runtime and Eric Zimmerman's Tools"
if ! command -v dotnet >/dev/null 2>&1; then
  # EZ Tools net9 builds need .NET 9+; the Ubuntu archive ships .NET (Microsoft
  # no longer publishes .NET packages for Ubuntu). Prefer the newest runtime.
  apt-get update -qq
  apt-get install -y dotnet-runtime-10.0 \
    || apt-get install -y dotnet-runtime-9.0 \
    || apt-get install -y dotnet-runtime-8.0
fi
# Allow a net9 app to run on a newer runtime if only net10 is installed.
export DOTNET_ROLL_FORWARD=Major

# .NET 9 (Linux-compatible) builds from the official CDN.
EZ_BASE="https://download.ericzimmermanstools.com/net9"
EZ_TOOLS="PECmd AmcacheParser AppCompatCacheParser SrumECmd SumECmd MFTECmd RECmd EvtxECmd RBCmd LECmd SQLECmd bstrings"

mkdir -p /opt/EZTools
for tool in $EZ_TOOLS; do
  if [ -f "/opt/EZTools/$tool/$tool" ]; then
    log "  $tool already installed, skipping"
    continue
  fi
  log "  Downloading $tool..."
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/$tool.zip" "$EZ_BASE/$tool.zip"
  mkdir -p "/opt/EZTools/$tool"
  unzip -q -o "$tmp/$tool.zip" -d "/opt/EZTools/$tool"
  chmod +x "/opt/EZTools/$tool/$tool" 2>/dev/null || true
  rm -rf "$tmp"
done

# Quick sanity check on one tool (prints its usage/version header).
log "Sanity check (PECmd):"
/opt/EZTools/PECmd/PECmd 2>&1 | head -n 3 || true

#  Splunk
log "Step 4/4: Splunk"
log "Splunk is intentionally NOT scripted (license + download URLs change often)."
cat <<'EOF'
Manual Splunk Free install on the VM:
  1. Download the latest Linux .tgz from https://www.splunk.com/ (account required):
       cd /tmp && wget "https://download.splunk.com/products/splunk/releases/<VERSION>/linux/splunk-<VERSION>-<HASH>-linux-amd64.tgz"
  2. Extract and start (accepts the license, seeds the admin password):
       sudo tar -C /opt -xzf splunk-*.tgz
       sudo /opt/splunk/bin/splunk start --accept-license --answer-yes --seed-passwd '<YourAdminPassword>'
  3. Open http://192.168.121.123:8000, log in as admin, then import the event
     logs (Splunk_logs_export.csv) as shown in the course.
EOF

log "Done. Docker, TimeSketch, and the Eric Zimmerman tools are installed."
