Dotfiles

This repository contains my personal system configurations. The structure is organized strictly by the init system rather than the specific distribution.
Software Stack

    Distro: Artix

    Window Manager: i3wm

    Shell: Zsh

    Terminal: Alacritty

    Editor: Neovim

    File Manager: Yazi

Structure

    openrc/ - Scripts and configurations for OpenRC-based setups (Artix/Gentoo).

    common/ - Init-agnostic application configurations (dotfiles for ~/.config/).

    scripts/ - Custom automation and utility scripts.

Installation:

OpenRC / General
Bash

git clone https://github.com/user/dotfiles.git
cd dotfiles
cp -r common/* ~/.config/
# Apply init-specific services from openrc/ as needed

Other things:
If you are using a system other than Arch/Artix, ensure that the package names match those used by your specific package manager.

Make sure to select the configurations appropriate for your graphics card in the installer.

License

GPL 2.0
