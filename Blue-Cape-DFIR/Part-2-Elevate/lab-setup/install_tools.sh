#!/usr/bin/env bash

# Dependencies installation for Linux hosts
# Supports Fedora/RHEL, Debian/Ubuntu, and other common package managers.

set -euo pipefail

VAGRANT_VERSION="2.4.9"

warn() {
  echo "[WARN] $*"
}

fail() {
  echo "[ERROR] $*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

detect_architecture() {
  case "$(uname -m)" in
    x86_64|amd64) echo "x86_64" ;;
    aarch64|arm64) echo "aarch64" ;;
    armv7l|armhf|arm) echo "arm" ;;
    *) fail "Unsupported architecture: $(uname -m)" ;;
  esac
}

build_vagrant_rpm_url() {
  local arch="$1"
  echo "https://releases.hashicorp.com/vagrant/${VAGRANT_VERSION}/vagrant-${VAGRANT_VERSION}-1.${arch}.rpm"
}

build_vagrant_deb_url() {
  local arch="$1"
  echo "https://releases.hashicorp.com/vagrant/${VAGRANT_VERSION}/vagrant_${VAGRANT_VERSION}_${arch}.deb"
}

ensure_prerequisites() {
  local pm="$1"
  case "$pm" in
    apt)
      sudo apt-get update
      sudo DEBIAN_FRONTEND=noninteractive apt-get install -y curl wget gnupg ca-certificates lsb-release
      ;;
    dnf|yum)
      sudo "$pm" install -y curl wget gnupg ca-certificates
      ;;
    zypper)
      sudo zypper --non-interactive install -y curl wget gpg ca-certificates
      ;;
    pacman)
      sudo pacman -Syu --noconfirm curl wget gnupg ca-certificates
      ;;
  esac
}

detect_package_manager() {
  if command -v dnf >/dev/null 2>&1; then
    echo "dnf"
  elif command -v yum >/dev/null 2>&1; then
    echo "yum"
  elif command -v apt-get >/dev/null 2>&1; then
    echo "apt"
  elif command -v apt >/dev/null 2>&1; then
    echo "apt"
  elif command -v zypper >/dev/null 2>&1; then
    echo "zypper"
  elif command -v pacman >/dev/null 2>&1; then
    echo "pacman"
  else
    fail "No supported package manager found (expected dnf/yum/apt/zypper/pacman)."
  fi
}

resolve_package_name() {
  local pm="$1"
  local pkg="$2"

  case "$pm" in
    apt)
      case "$pkg" in
        qemu-kvm) echo "qemu-system-x86" ;;
        libvirt) echo "libvirt-daemon" ;;
        libvirt-daemon-kvm) echo "libvirt-daemon-system" ;;
        libvirt-client) echo "libvirt-clients" ;;
        virt-install) echo "virtinst" ;;
        virt-viewer) echo "virt-viewer" ;;
        libvirt-devel) echo "libvirt-dev" ;;
        libxml2-devel) echo "libxml2-dev" ;;
        ruby-devel) echo "ruby-dev" ;;
        *) echo "$pkg" ;;
      esac
      ;;
    *)
      echo "$pkg"
      ;;
  esac
}

package_installed() {
  local pm="$1"
  local pkg="$2"
  local resolved
  resolved="$(resolve_package_name "$pm" "$pkg")"

  case "$pm" in
    dnf|yum|zypper)
      rpm -q "$resolved" >/dev/null 2>&1
      ;;
    apt)
      dpkg -s "$resolved" >/dev/null 2>&1
      ;;
    pacman)
      pacman -Q "$resolved" >/dev/null 2>&1
      ;;
    *)
      return 1
      ;;
  esac
}

install_packages() {
  local pm="$1"
  shift
  local missing=()
  local pkg
  local resolved

  for pkg in "$@"; do
    if ! package_installed "$pm" "$pkg"; then
      resolved="$(resolve_package_name "$pm" "$pkg")"
      missing+=("$resolved")
    fi
  done

  if (( ${#missing[@]} > 0 )); then
    echo "[INFO] Installing packages with ${pm}: ${missing[*]}"
    case "$pm" in
      dnf)
        sudo dnf install -y "${missing[@]}"
        ;;
      yum)
        sudo yum install -y "${missing[@]}"
        ;;
      apt)
        sudo apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${missing[@]}"
        ;;
      zypper)
        sudo zypper --non-interactive install -y "${missing[@]}"
        ;;
      pacman)
        sudo pacman -Syu --noconfirm "${missing[@]}"
        ;;
    esac
  else
    echo "[INFO] All requested packages are already installed: $*"
  fi
}

enable_service() {
  local service="$1"
  if ! sudo systemctl is-enabled "$service" >/dev/null 2>&1; then
    sudo systemctl enable "$service"
  fi

  if ! systemctl is-active --quiet "$service"; then
    sudo systemctl start "$service"
  fi
}

append_shell_export() {
  local line="$1"
  if ! grep -Fq "$line" ~/.bashrc 2>/dev/null; then
    echo "$line" >> ~/.bashrc
    echo "[INFO] Added shell export to ~/.bashrc"
  fi
}

PACKAGE_MANAGER="$(detect_package_manager)"
ensure_prerequisites "$PACKAGE_MANAGER"

if [[ "$PACKAGE_MANAGER" == "apt" ]]; then
  echo "[INFO] Detected package manager: apt"
elif [[ "$PACKAGE_MANAGER" == "dnf" ]]; then
  echo "[INFO] Detected package manager: dnf"
elif [[ "$PACKAGE_MANAGER" == "yum" ]]; then
  echo "[INFO] Detected package manager: yum"
elif [[ "$PACKAGE_MANAGER" == "zypper" ]]; then
  echo "[INFO] Detected package manager: zypper"
else
  echo "[INFO] Detected package manager: pacman"
fi

echo "===================================================================="
echo "      Installing the necessary tools for your lab creation ..."
echo "                   Target OS: $(uname -s)"
echo "===================================================================="

# 1. KVM / Libvirt
echo ""
echo "[1/5] KVM / Libvirt..."
install_packages "$PACKAGE_MANAGER" \
  qemu-kvm libvirt libvirt-daemon-kvm libvirt-client \
  virt-install virt-viewer libguestfs-tools bridge-utils

enable_service libvirtd

# Add the current user to the necessary groups only if missing
for group in libvirt kvm; do
  if ! id -nG "$USER" | tr ' ' '\n' | grep -qx "$group"; then
    sudo usermod -aG "$group" "$USER"
  fi
done

# Default libvirt URI (avoid qemu:///session vs system)
append_shell_export 'export LIBVIRT_DEFAULT_URI="qemu:///system"'
export LIBVIRT_DEFAULT_URI="qemu:///system"

# 2. Packer
echo ""
echo "[2/5] Packer..."
if ! command -v packer &>/dev/null; then
  case "$PACKAGE_MANAGER" in
    dnf|yum)
      install_packages "$PACKAGE_MANAGER" dnf-plugins-core
      if ! sudo "$PACKAGE_MANAGER" repolist --enabled 2>/dev/null | grep -q '^hashicorp'; then
        if [[ "$PACKAGE_MANAGER" == "dnf" ]]; then
          sudo dnf config-manager addrepo \
            --from-repofile=https://rpm.releases.hashicorp.com/fedora/hashicorp.repo
        else
          sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/fedora/hashicorp.repo
        fi
      fi
      install_packages "$PACKAGE_MANAGER" packer
      ;;
    apt)
      if ! grep -q 'hashicorp' /etc/apt/sources.list.d/hashicorp.list 2>/dev/null; then
        sudo install -d -m 0755 /etc/apt/keyrings
        curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/hashicorp-archive-keyring.gpg
        echo "deb [signed-by=/etc/apt/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(. /etc/os-release && echo "$VERSION_CODENAME") main" | sudo tee /etc/apt/sources.list.d/hashicorp.list >/dev/null
      fi
      sudo apt-get update
      sudo DEBIAN_FRONTEND=noninteractive apt-get install -y packer
      ;;
    *)
      warn "Automatic Packer installation is not implemented for $PACKAGE_MANAGER. Please install it manually."
      ;;
  esac
else
  echo "[INFO] Packer already installed: $(packer version)"
fi

# 3. Vagrant
echo ""
echo "[3/5] Vagrant ${VAGRANT_VERSION}..."
if command -v vagrant &>/dev/null; then
  INSTALLED=$(vagrant --version 2>/dev/null | grep -oE '\d+\.\d+\.\d+' || true)
  if [[ -n "$INSTALLED" && "$INSTALLED" == "$VAGRANT_VERSION" ]]; then
    echo "[INFO] Vagrant ${VAGRANT_VERSION} already installed."
  else
    echo "[WARN] Installed version: ${INSTALLED:-unknown} — updating to ${VAGRANT_VERSION}..."
    case "$PACKAGE_MANAGER" in
      apt)
        ARCH="$(detect_architecture)"
        DEB_URL="$(build_vagrant_deb_url "$ARCH")"
        DEB_FILE="/tmp/vagrant_${VAGRANT_VERSION}_${ARCH}.deb"
        wget -q "$DEB_URL" -O "$DEB_FILE"
        sudo apt-get install -y "$DEB_FILE"
        rm -f "$DEB_FILE"
        ;;
      *)
        ARCH="$(detect_architecture)"
        RPM_URL="$(build_vagrant_rpm_url "$ARCH")"
        RPM_FILE="/tmp/vagrant-${VAGRANT_VERSION}-1.${ARCH}.rpm"
        wget -q "$RPM_URL" -O "$RPM_FILE"
        sudo dnf install -y "$RPM_FILE" 2>/dev/null || sudo yum install -y "$RPM_FILE"
        rm -f "$RPM_FILE"
        ;;
    esac
  fi
else
  echo "[INFO] Downloading Vagrant ${VAGRANT_VERSION}; please wait..."
  case "$PACKAGE_MANAGER" in
    apt)
      ARCH="$(detect_architecture)"
      DEB_URL="$(build_vagrant_deb_url "$ARCH")"
      DEB_FILE="/tmp/vagrant_${VAGRANT_VERSION}_${ARCH}.deb"
      wget -q "$DEB_URL" -O "$DEB_FILE"
      sudo apt-get install -y "$DEB_FILE"
      rm -f "$DEB_FILE"
      ;;
    *)
      ARCH="$(detect_architecture)"
      RPM_URL="$(build_vagrant_rpm_url "$ARCH")"
      RPM_FILE="/tmp/vagrant-${VAGRANT_VERSION}-1.${ARCH}.rpm"
      wget -q "$RPM_URL" -O "$RPM_FILE"
      sudo dnf install -y "$RPM_FILE" 2>/dev/null || sudo yum install -y "$RPM_FILE"
      rm -f "$RPM_FILE"
      ;;
  esac
fi

# 4. Build dependencies for vagrant-libvirt
echo ""
echo "[4/5] Build dependencies..."
install_packages "$PACKAGE_MANAGER" gcc make libvirt-devel libxml2-devel ruby-devel libguestfs-tools

# 5. vagrant-libvirt plugin
echo ""
echo "[5/5] vagrant-libvirt plugin..."
if vagrant plugin list 2>/dev/null | grep -q 'vagrant-libvirt'; then
  echo "[INFO] vagrant-libvirt plugin already installed."
else
  vagrant plugin install vagrant-libvirt
fi

# Final verification
echo ""
echo "========================================"
echo "          Final Verifications ..."
echo "========================================"
if command -v vagrant >/dev/null 2>&1; then
  echo "Vagrant      : $(vagrant --version)"
fi
if command -v packer >/dev/null 2>&1; then
  echo "Packer       : $(packer version)"
fi
if systemctl list-unit-files libvirtd.service >/dev/null 2>&1; then
  echo "Libvirt      : $(systemctl is-active libvirtd)"
fi
if command -v vagrant >/dev/null 2>&1; then
  echo "Plugins      : $(vagrant plugin list 2>/dev/null | grep libvirt || echo 'NOT INSTALLED')"
fi
echo ""
echo "[!] Reconnect to apply the libvirt/kvm group changes."
echo "[!] Source ~/.bashrc or restart the shell to use LIBVIRT_DEFAULT_URI."