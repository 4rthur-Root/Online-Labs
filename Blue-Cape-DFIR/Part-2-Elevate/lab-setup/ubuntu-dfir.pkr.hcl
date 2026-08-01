packer {
  required_plugins {
    qemu = {
      source  = "github.com/hashicorp/qemu"
      version = "~> 1.0"
    }
    vagrant = {
      source  = "github.com/hashicorp/vagrant"
      version = "~> 1.0"
    }
  }
}

variable "iso_url" {
  default = "/home/adrien/Downloads/ISO/Ubuntu-Server.iso"
}

variable "iso_checksum" {
  default = "sha256:e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433"
}

source "qemu" "ubuntu-dfir" {
  iso_url           = var.iso_url
  iso_checksum      = var.iso_checksum
  output_directory  = "output-ubuntu-server"
  vm_name           = "ubuntu-dfir"
  disk_size         = "20G" 
  format            = "qcow2"
  headless          = false # For debugging, set to true for headless operation
  accelerator       = "kvm"
  memory            = 2048
  cpu_model         = "host"
  cores             = 2
  net_device        = "virtio-net"
  disk_interface    = "virtio"
  boot_wait         = "30s"
  boot_key_interval = "250ms"
  boot_keygroup_interval = "500ms"
  
  # Boot command to automate the installation process using cloud-init
  # The boot command sequence is designed to navigate the boot menu and initiate the autoinstallation process.
  boot_command = [
    "<esc><wait10>",
    "<esc><wait10>",
    "e<wait10>",
    "<end><wait10>",
    " autoinstall ds=nocloud-net;s=cdrom:/<enter><wait20>",
    "<f10><wait20>"
  ]
  
  cd_files = ["user-data", "meta-data"]
  cd_label = "cidata"
  ssh_username   = "vagrant"
  ssh_password   = "vagrant"
  ssh_timeout    = "60m"
  shutdown_command = "echo 'vagrant' | sudo -S shutdown -P now"
}

build {
  sources = ["source.qemu.ubuntu-dfir"]

  # Provisioning post-installation to finalize the configuration and clean up the image
  provisioner "shell" {
    inline = [
      "set -e",
      "echo 'Finalizing configuration...'",
      "sudo apt-get update",
      "sudo apt-get install -y qemu-guest-agent cloud-init",
      "sudo systemctl enable qemu-guest-agent",
      "sudo apt-get clean",
      "sudo apt-get autoremove --purge -y",
      "sudo rm -rf /var/cache/apt/archives/*",
      "sudo rm -rf /tmp/*",
      "sudo rm -rf /var/log/*.gz",
      "sudo truncate -s 0 /var/log/*log"
    ]
  }

  post-processor "vagrant" {
    output = "dfir-ubuntu-base.box"
    compression_level = 9
  }
}