#!/usr/bin/env bash

# Dependencies installation (Fedora 44+)
# Use: bash scripts_shell/install_tools.sh

set -euo pipefail

VAGRANT_VERSION="2.4.9"
VAGRANT_RPM="vagrant-${VAGRANT_VERSION}-1.x86_64.rpm"
VAGRANT_URL="https://releases.hashicorp.com/vagrant/${VAGRANT_VERSION}/${VAGRANT_RPM}"

ensure_dnf_packages() {
  local missing=()
  local pkg

  for pkg in "$@"; do
    if ! rpm -q "$pkg" &>/dev/null; then
      missing+=("$pkg")
    fi
  done

  if (( ${#missing[@]} > 0 )); then
    sudo dnf install -y "${missing[@]}"
  else
    echo "[INFO] All requested DNF packages are already installed: $*"
  fi
}

echo "========================================"
echo "   Installing the necessary tools ..."
echo "   Cible : Fedora $(rpm -E %fedora)"
echo "========================================"

# 1. KVM / Libvirt
echo ""
echo "[1/5] KVM / Libvirt..."
ensure_dnf_packages \
  qemu-kvm libvirt libvirt-daemon-kvm libvirt-client \
  virt-install virt-viewer libguestfs-tools bridge-utils

if ! sudo systemctl is-enabled libvirtd &>/dev/null; then
  sudo systemctl enable libvirtd
fi

if ! systemctl is-active --quiet libvirtd; then
  sudo systemctl start libvirtd
fi

# Add the current user to the necessary groups only if missing
for group in libvirt kvm; do
  if ! id -nG "$USER" | tr ' ' '\n' | grep -qx "$group"; then
    sudo usermod -aG "$group" "$USER"
  fi
done

# Default libvirt URI (avoid qemu:///session vs system)
if ! grep -q 'LIBVIRT_DEFAULT_URI' ~/.bashrc; then
  echo 'export LIBVIRT_DEFAULT_URI="qemu:///system"' >> ~/.bashrc
  echo "[INFO] LIBVIRT_DEFAULT_URI added to ~/.bashrc"
fi
export LIBVIRT_DEFAULT_URI="qemu:///system"

# 2. Packer
echo ""
echo "[2/5] Packer..."
if ! command -v packer &>/dev/null; then
  ensure_dnf_packages dnf-plugins-core
  if ! sudo dnf repolist --enabled | grep -q '^hashicorp'; then
    sudo dnf config-manager addrepo \
      --from-repofile=https://rpm.releases.hashicorp.com/fedora/hashicorp.repo
  fi
  ensure_dnf_packages packer
else
  echo "[INFO] Packer already installed: $(packer version)"
fi

# 3. Vagrant
echo ""
echo "[3/5] Vagrant ${VAGRANT_VERSION}..."
if command -v vagrant &>/dev/null; then
  INSTALLED=$(vagrant --version | grep -oP '\d+\.\d+\.\d+' || true)
  if [[ -n "$INSTALLED" && "$INSTALLED" == "$VAGRANT_VERSION" ]]; then
    echo "[INFO] Vagrant ${VAGRANT_VERSION} already installed."
  else
    echo "[WARN] Installed version: ${INSTALLED:-unknown} — updating to ${VAGRANT_VERSION}..."
    wget -q "$VAGRANT_URL" -O "/tmp/${VAGRANT_RPM}"
    sudo dnf install -y "/tmp/${VAGRANT_RPM}"
    rm -f "/tmp/${VAGRANT_RPM}"
  fi
else
  echo "[INFO] Downloading Vagrant ${VAGRANT_VERSION}; please wait..."
  wget -q "$VAGRANT_URL" -O "/tmp/${VAGRANT_RPM}"
  sudo dnf install -y "/tmp/${VAGRANT_RPM}"
  rm -f "/tmp/${VAGRANT_RPM}"
fi

# 4. Build dependencies for vagrant-libvirt
echo ""
echo "[4/5] Build dependencies..."
ensure_dnf_packages gcc make libvirt-devel libxml2-devel ruby-devel libguestfs-tools

# 5. vagrant-libvirt plugin
echo ""
echo "[5/5] vagrant-libvirt plugin..."
if vagrant plugin list | grep -q 'vagrant-libvirt'; then
  echo "[INFO] vagrant-libvirt plugin already installed."
else
  vagrant plugin install vagrant-libvirt
fi

# Vérification finale
echo ""
echo "========================================"
echo "          Final Verifications"
echo "========================================"
echo "Vagrant      : $(vagrant --version)"
echo "Packer       : $(packer version)"
echo "Libvirt      : $(systemctl is-active libvirtd)"
echo "Plugins      : $(vagrant plugin list | grep libvirt || echo 'NOT INSTALLED')"
echo ""
echo "[!] Reconnect to apply the libvirt/kvm group changes."
echo "[!] Source ~/.bashrc or restart the shell to use LIBVIRT_DEFAULT_URI."