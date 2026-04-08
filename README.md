Dotfiles

This repository contains my personal system configurations. The structure is organized strictly by the init system rather than the specific distribution.
Software Stack

    Window Manager: i3wm

    Shell: Zsh

    Terminal: Alacritty

    Editor: Neovim

    File Manager: Yazi

Structure

    systemd/ - Configurations, services, and modules for systemd-based setups (NixOS).

    openrc/ - Scripts and configurations for OpenRC-based setups (Artix/Gentoo).

    common/ - Init-agnostic application configurations (dotfiles for ~/.config/).

    scripts/ - Custom automation and utility scripts.

Installation:
Systemd (NixOS)


sudo nixos-rebuild switch --flake .#hostname

OpenRC / General
Bash

git clone https://github.com/user/dotfiles.git
cd dotfiles
cp -r common/* ~/.config/
# Apply init-specific services from openrc/ as needed

License

GPL 2.0
