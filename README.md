# i3wm configs

![License](https://img.shields.io/badge/license-GPL--2.0-blue.svg)
![Init](https://img.shields.io/badge/init-OpenRC-orange)
![WM](https://img.shields.io/badge/WM-i3wm-green)

Personal dotfiles and system configurations. This repository is organized strictly by the **init system** rather than the specific distribution, ensuring better portability for Artix and Gentoo users.

---

## 🛠️ Software Stack

* **Distro:** Artix Linux (OpenRC)
* **Window Manager:** i3wm
* **Shell:** Zsh (with custom aliases & fastfetch)
* **Terminal:** Alacritty
* **Editor:** Neovim
* **File Manager:** Yazi
* **Visual Style:** Inspired by Frutiger Aero (Glass Blur / Liquid Gloss)

---

## 📂 Structure

The repository separates core application configs from system-level service management:

* `openrc/` – Scripts and service configurations for OpenRC-based setups.
* `common/` – Init-agnostic application configurations (maps to `~/.config/`).
* `scripts/` – Custom automation, including a Python-based interactive installer.

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone [https://github.com/LubieBudyn699/i3wm-configs.git](https://github.com/TWOJA_NAZWA/i3wm-configs.git)
cd i3wm-configs

2. Run the Installer

I have developed a custom Python installer using dialog to handle package selection and symlinking:
Bash

python3 scripts/install.py

Note: If you prefer manual installation, you can copy the contents of common/ to your ~/.config/ directory.
⚙️ GPU & Performance

The installer includes profiles for AMD and Nvidia. Make sure to select the appropriate one to ensure transparency and blur effects (Picom) work correctly with your hardware.
⚖️ License

This project is licensed under GPL 2.0. Feel free to fork and modify!

Maintained by LubieBudyn699
