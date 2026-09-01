#!/usr/bin/env bash
#
# RegRipper 3.0 Automated Linux Installer
# Configures the latest GitHub build with correct Linux Perl interpreter paths.
# Make it executable: chmod +x install.sh
# And then run it as sudo: sudo ./install.sh


set -e # Exit immediately if any command fails

echo "[*] Ensuring root privileges..."
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script with sudo: sudo ./install_regripper.sh"
  exit 1
fi

echo "[*] Cleaning up any previous failed installations or broken links..."
rm -f /usr/local/bin/rip.pl
rm -rf /opt/regripper

echo "[*] Installing required package dependencies..."
apt-get update && apt-get install -y libparse-win32registry-perl git

echo "[*] Cloning the official RegRipper 3.0 repository..."
git clone https://github.com /opt/regripper

echo "[*] Modifying Windows hardcoded shebang paths for Linux Perl..."
sed -i '1s|.*|#!/usr/bin/env perl|' /opt/regripper/rip.pl

echo "[*] Making the script executable..."
chmod +x /opt/regripper/rip.pl

echo "[*] Creating a global symbolic link inside /usr/local/bin/..."
ln -s /opt/regripper/rip.pl /usr/local/bin/rip.pl

echo -e "\n[+] RegRipper 3.0 installation completed successfully!"
echo "[*] Verifying global access..."
echo "--------------------------------------------------------"
rip.pl -h | head -n 5
echo "--------------------------------------------------------"
echo "[+] Verification passed. You can now use 'rip.pl' anywhere as a standard user."
