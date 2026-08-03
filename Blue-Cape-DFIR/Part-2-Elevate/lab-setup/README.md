# Lab Setup for the DFIR Workstation

This folder contains a small, self-contained workflow to build and run an Ubuntu-based DFIR workstation with Vagrant and libvirt.

## What this setup does

The workflow helps you:

- install the host dependencies needed for Vagrant/libvirt on your host system
- build a custom Ubuntu base box with Packer
- register that box with Vagrant
- start a VM defined by the included Vagrant configuration

It is intended for the local lab environment for the hands on part of the certification.

## Files in this folder

- `install_tools.sh` – installs Vagrant, Packer, libvirt, and related packages on the host
- `box.sh` – builds the Ubuntu box with Packer and adds it to Vagrant if needed
- `ubuntu-dfir.pkr.hcl` – the Packer template used to build the base box
- `user-data` and `meta-data` – cloud-init files used by the Packer build for Ubuntu autoinstall
- `Vagrantfile` – the Vagrant machine definition for the lab VM
- `Makefile` – convenience targets for the full workflow

## Prerequisites

Before starting, make sure your host machine satisfies the following:

- A Fedora/RHEL, Debian/Ubuntu, or other Linux host is assumed
- CPU virtualization support must be available and enabled in BIOS/UEFI
- You must have sudo privileges
- You should have enough free disk space for the VM image and packages ~ 200 Gb free (and SSD)
- You should also have already installed the ubuntu iso as this script does not do it and consider change iso_url variable in [Ubuntu-ISO-URL](./ubuntu-dfir.pkr.hcl) (line 16)

### Recommended host requirements

- 16+ GB RAM recommended
- 4+ CPU cores recommended
- At least 250+ GB free disk space

## Important considerations before you start

1. Virtualization must be enabled
   - If your VM is not able to start guests, check that VT-x/AMD-V is enabled in BIOS/UEFI.

2. The Packer ISO checksum must be updated
   - The actual one is for my ubuntu 24 , it should not be different but to be sure run `sha256 iso_name` and replace the result in [ISO-CHECKSUM](./ubuntu-dfir.pkr.hcl) (line 17)
   - You must replace it with the official SHA-256 for the Ubuntu ISO before building.

3. You may need to reboot after installing libvirt-related packages
   - The script adds your user to the `libvirt` and `kvm` groups.
   - A new login or reboot is often required for those group changes to take effect.

4. Network and libvirt permissions
   - If libvirt fails to start or create VMs, verify that the `libvirtd` service is active.
   - Confirm that your user can access the system libvirt connection.

## Step-by-step setup

### 1. Install the required tools

From this folder, run:

```bash
make install-tools
```

This runs `install_tools.sh`, which auto-detects the available package manager and installs:

- libvirt
- qemu/KVM components
- Packer
- Vagrant
- the Vagrant libvirt plugin dependencies

The script supports common package managers such as `dnf`, `yum`, `apt`, `zypper`, and `pacman`. On Debian/Ubuntu-based systems it also prepares the necessary package sources for HashiCorp tools.

If the script asks you to reconnect or restart your shell, do that before continuing.

### 2. Build the Ubuntu base box

Before building, verify `ubuntu-dfir.pkr.hcl` has the correct `iso_url` and `iso_checksum` for your Ubuntu 24.04 ISO. The file also uses the local `user-data` and `meta-data` cloud-init files for unattended install.

Then run:

```bash
make build-ubuntu-box
```

This runs `box.sh`, which:

- initializes Packer
- builds the box with Packer
- checks that the `.box` artifact exists
- registers the box with Vagrant if it is not already present

If you prefer, you can also run:

```bash
bash box.sh
```
It should take around 25 minutes to complete.

### 3. Start the Vagrant VM

Once the box exists, start the lab VM with:

```bash
make up
```

This uses the Vagrantfile and starts the machine with the libvirt provider. It also installs these tools on the VM.

- xfce for desktop support
- wireshark
- tshark
- python3
- python3-pip
- python3-venv
- git
- curl
- unzip 
- p7zip-full
- sleuthkit
- autopsy

The other tools will be installed later and are documented further in this README file.

### 4. Optional: provision the machine

If you want to rerun provisioning manually, run:

```bash
make provision
```

### 5. Stop or destroy the environment

To stop the machine:

```bash
make down
```

To remove it completely:

```bash
make destroy
```

To remove the locally registered box:

```bash
make clean
```

## Reference
Run 
```bash
make help
```
To have all the options.

## Troubleshooting

### Packer build fails

Common causes include:

- missing or incorrect ISO checksum
- libvirt not running
- missing Packer plugin or package
- insufficient disk space or memory

### Vagrant fails to start the VM

Common causes include:

- libvirt service not active
- missing libvirt permissions for the current user
- the box was not registered correctly
- the machine image path is missing or invalid

### The Xfce desktop (GUI) does not appear

- **Symptom:** the VM boots to a text console, there is no graphical login, and `sudo systemctl status lightdm` shows lightdm as `failed`.
- **Most likely cause:** the X server is missing. The lightdm log at `/var/log/lightdm/lightdm.log` shows `XServer 0: Can't launch X server X -core, not found in path`. A bare `xfce4` install does not pull in `xserver-xorg`. A second, equally common cause is a missing greeter: lightdm was installed with `--no-install-recommends`, so `lightdm-gtk-greeter` was never installed.
- **Applying the fix on a running VM (no rebuild):**

  ```bash
  vagrant ssh -c "sudo apt-get update -qq \
    && sudo apt-get install -y xserver-xorg xserver-xorg-video-qxl lightdm-gtk-greeter \
    && sudo mkdir -p /etc/lightdm/lightdm.conf.d \
    && printf '[Seat:*]\nautologin-user=vagrant\nautologin-user-timeout=0\n' \
       | sudo tee /etc/lightdm/lightdm.conf.d/50-autologin.conf \
    && sudo systemctl set-default graphical.target \
    && sudo systemctl enable --now lightdm"
  ```

  Then open the VM's graphical console via SPICE (virt-manager -> Open), not SSH: the Xfce desktop should appear automatically after auto-login.
- **Note:** the Vagrantfile already provisions all of the above, so freshly created VMs (`vagrant up --provision`) get a working auto-login desktop directly.

### The VM hostname

- The VM hostname is controlled by `config.vm.hostname` in the `Vagrantfile`. To rename the machine on a running VM:

  ```bash
  sudo hostnamectl set-hostname "Ubuntu-dfir" && sudo sed -i "s/ubuntu-dfir/Ubuntu-dfir/" /etc/hosts
  ```

### The disk reports far less than the ~150 GB virtual size

- **Symptom:** `make up` succeeds, but `df -h /` shows a root of only ~10 GB even though `lv.machine_virtual_size = 150` is set. `lsblk` shows `vda` = 150G but `vda3` (and the LVM `ubuntu-lv`) are still ~18 GB / ~10 GB.
- **Why:** `machine_virtual_size` only inflates the **raw virtual disk** capacity to 150 GB. It does **not** resize the guest's partition table, LVM, or filesystem. The extra ~131 GB is simply unpartitioned/unallocated space.
- **What the Vagrantfile already does:** it auto-grows everything at provision time (`growpart` + `pvresize` + `lvextend` + `resize2fs`, see the `Vagrantfile`). Fresh VMs provisioned with `vagrant up --provision` get the full disk automatically.
- **Manual fix on a running VM** (partition is in use, done online):

  ```bash
  sudo apt-get install -y cloud-guest-utils        # provides growpart
  sudo growpart /dev/vda 3                          # grow partition 3 to the 150G disk
  sudo partx -u /dev/vda                            # reload the partition table in the kernel
  sudo pvresize /dev/vda3                           # extend the LVM physical volume
  sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv   # extend the root LV to the whole VG
  sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv      # grow the ext4 filesystem
  df -h /                                           # should now show ~150G
  ```
  Note the device-mapper path uses double hyphens: `/dev/mapper/ubuntu--vg-ubuntu--lv`, not a single one. If `resize2fs` returns "No such file or directory", that is the cause.

### Box already exists

The box script is designed to skip re-adding a box that is already present in Vagrant.

## Notes
### Autoinstall prompt

- **Symptom:** during the unattended install you may see a prompt asking "Continue autoinstall?" which requires typing `yes` to proceed.

- **Why:** some installer behaviors (refresh checks or interactive sections) can trigger a confirmation prompt in the installer UI.

- **What we changed:** the included `user-data` now sets `interactive-sections: []`, disables `refresh-installer` updates, and sets `reporting.builtin.type: none` to avoid interactive prompts.

- **If you still see a prompt:** open `user-data` and remove any `interactive-sections` entries or set `refresh-installer.update: false` as needed. Re-run `make build-ubuntu-box`. (line 4-9)

This change keeps the install fully unattended by default.
This setup is intentionally simple and focused on getting a functional local lab environment running quickly. It is a good starting point, but production or long-term lab deployments may need stricter automation, better provisioning, and more hardened VM settings.
