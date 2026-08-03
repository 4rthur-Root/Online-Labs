#!/usr/bin/env bash

# Installation Docker CE + Compose sur Debian
# Usage : bash docker.sh 


set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

# Vérification si Docker est déjà installé
if command -v docker &>/dev/null; then
  log "Docker already installed : $(docker --version)"
  log "Checking APT repository..."

  if [ ! -f /etc/apt/sources.list.d/docker.list ]; then
    log "  → Docker repository missing, reinstalling..."
  else
    log "  → Docker repository present ✓"
    log "Checking Docker Compose..."
    if docker compose version &>/dev/null; then
      log "  → Docker Compose available ✓"
      log "Docker is up to date, nothing to do."
      exit 0
    fi
  fi
fi

log "=== Installation of Docker CE + Compose ==="

# 1. Prérequis
log "Installation of the prerequisites..."
apt-get update -qq
apt-get install -y -qq ca-certificates curl

# 2. Clé GPG officielle
log "Adding Docker GPG key..."
install -m 0755 -d /etc/apt/keyrings
DISTRO=$(. /etc/os-release && echo "$ID")
curl -fsSL "https://download.docker.com/linux/${DISTRO}/gpg" -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# 3. Dépôt APT
log "Adding Docker repository..."
CODENAME=$(. /etc/os-release && echo "$VERSION_CODENAME")
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/${DISTRO} $CODENAME stable" \
  > /etc/apt/sources.list.d/docker.list

# 4. Installation
log "Installation of Docker CE + Compose..."
apt-get update -qq
apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Docker group
if id -nG "${SUDO_USER:-root}" 2>/dev/null | grep -qw docker; then
  log "Your user is already in the docker group"
else
  usermod -aG docker "${SUDO_USER:-root}" 2>/dev/null || true
  log "User added to the docker group"
fi

# 6. Activate the service
systemctl enable docker
systemctl start docker

# 7. Vérification
log ""
log "============================================================"
log "             ✅ Docker installed with success"
log "             $(docker --version)"
log "             $(docker compose version)"
log "============================================================"
