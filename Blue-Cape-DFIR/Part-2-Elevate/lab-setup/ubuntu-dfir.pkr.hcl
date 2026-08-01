packer {
  required_plugins {
    libvirt = {
      version = ">= 0.5.0"
      source  = "github.com/hashicorp/libvirt"
    }
  }
}

variable "ubuntu_version" {
  type    = string
  default = "24.04.1"
}

source "libvirt-iso" "ubuntu-dfir-base" {
  iso_url      = "https://releases.ubuntu.com/${var.ubuntu_version}/ubuntu-${var.ubuntu_version}-live-server-amd64.iso"
  iso_checksum = "sha256:YOUR_OFFICIAL_SHA256_HERE"
  disk_size    = 15360
  memory       = 2048
  cpus         = 2
  headless     = true
  ssh_username = "vagrant"
  ssh_password = "vagrant"
  ssh_timeout  = "20m"
  shutdown_command = "echo 'packer' | sudo -S shutdown -P now"
  libvirt_uri  = "qemu:///system"
  format       = "qcow2"
  boot_command = [
    "<wait><esc><wait>"
  ]
}

build {
  sources = ["source.libvirt-iso.ubuntu-dfir-base"]

  provisioner "shell" {
    inline = [
      "set -e",
      "export DEBIAN_FRONTEND=noninteractive",
      "sudo apt-get update",
      "sudo apt-get install -y openssh-server qemu-guest-agent cloud-init",
      "sudo systemctl enable qemu-guest-agent",
      "sudo useradd -m -s /bin/bash vagrant || true",
      "echo 'vagrant:vagrant' | sudo chpasswd",
      "sudo mkdir -p /home/vagrant/.ssh",
      "sudo curl -fsSL -o /home/vagrant/.ssh/authorized_keys https://raw.githubusercontent.com/hashicorp/vagrant/main/keys/vagrant.pub",
      "sudo chmod 700 /home/vagrant/.ssh",
      "sudo chmod 600 /home/vagrant/.ssh/authorized_keys",
      "sudo chown -R vagrant:vagrant /home/vagrant/.ssh",
      "echo 'vagrant ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/vagrant >/dev/null",
      "sudo chmod 0440 /etc/sudoers.d/vagrant"
    ]
  }
}
   