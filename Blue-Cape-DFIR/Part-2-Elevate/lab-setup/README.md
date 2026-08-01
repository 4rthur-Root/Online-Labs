# Lab Setup for the DFIR Workstation

This folder contains a small, self-contained workflow to build and run an Ubuntu-based DFIR workstation with Vagrant and libvirt.

## What this setup does

The workflow helps you:

- install the host dependencies needed for Vagrant/libvirt on Fedora
- build a custom Ubuntu base box with Packer
- register that box with Vagrant
- start a VM defined by the included Vagrant configuration

It is intended for the local lab environment for the hands on part of the certification.

## Files in this folder

- `install_tools.sh` – installs Vagrant, Packer, libvirt, and related packages on the host
- `box.sh` – builds the Ubuntu box with Packer and adds it to Vagrant if needed
- `ubuntu-dfir.pkr.hcl` – the Packer template used to build the base box
- `Vagrantfile` – the Vagrant machine definition for the lab VM
- `Makefile` – convenience targets for the full workflow

## Prerequisites

Before starting, make sure your host machine satisfies the following:

- A Fedora/RHEL, Debian/Ubuntu, or other Linux host is assumed
- CPU virtualization support must be available and enabled in BIOS/UEFI
- You must have sudo privileges
- You should have enough free disk space for the VM image and packages
- A working libvirt/KVM setup is required

### Recommended host requirements

- 8+ GB RAM recommended
- 4+ CPU cores recommended
- At least 50+ GB free disk space

## Important considerations before you start

1. Virtualization must be enabled
   - If your VM is not able to start guests, check that VT-x/AMD-V is enabled in BIOS/UEFI.

2. The Packer ISO checksum must be updated
   - The template currently contains a placeholder checksum.
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

Before building, edit `ubuntu-dfir.pkr.hcl` and replace the placeholder ISO checksum.

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

### 3. Start the Vagrant VM

Once the box exists, start the lab VM with:

```bash
make up
```

This uses the Vagrantfile and starts the machine with the libvirt provider.

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

## Quick reference

Use these commands most often:

```bash
make help
make install-tools
make build-ubuntu-box
make up
make down
make destroy
make clean
```

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

### Box already exists

The box script is designed to skip re-adding a box that is already present in Vagrant.

## Notes

This setup is intentionally simple and focused on getting a functional local lab environment running quickly. It is a good starting point, but production or long-term lab deployments may need stricter automation, better provisioning, and more hardened VM settings.
