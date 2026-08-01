.PHONY: help install-tools box build-ubuntu-box up provision down destroy clean

SHELL := /bin/bash
VAGRANT ?= vagrant
PACKER ?= packer

BOX_NAME ?= dfir-ubuntu-base
BOX_PATH ?= output-vagrant/package.box

.DEFAULT_GOAL := help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install-tools      Install Vagrant, Libvirt and related dependencies"
	@echo "  box                Build the Ubuntu DFIR box and register it with Vagrant"
	@echo "  build-ubuntu-box   Build the Ubuntu DFIR box with Packer"
	@echo "  up                 Start the Vagrant environment"
	@echo "  provision          Run Vagrant provisioning"
	@echo "  down               Stop the Vagrant environment"
	@echo "  destroy            Destroy the Vagrant environment"
	@echo "  clean              Remove the local Vagrant box if present"

install-tools:
	@echo "=> Installing dependencies and tools..."
	@bash ./install_tools.sh

build-ubuntu-box:
	@echo "=> Building the Ubuntu DFIR box with Packer..."
	@bash ./box.sh

box: build-ubuntu-box

up:
	@echo "=> Starting the Vagrant environment..."
	@$(VAGRANT) up --provider=libvirt

provision:
	@echo "=> Running Vagrant provisioning..."
	@$(VAGRANT) provision

down:
	@echo "=> Stopping the Vagrant environment..."
	@$(VAGRANT) halt

destroy:
	@echo "=> Destroying the Vagrant environment..."
	@$(VAGRANT) destroy -f

clean:
	@echo "=> Cleaning up the local Vagrant box..."
	@$(VAGRANT) box remove $(BOX_NAME) --provider libvirt 2>/dev/null || true