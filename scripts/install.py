#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import logging
import stat

# --- LOGGING SETUP ---
logging.basicConfig(
    filename='install.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

CONFIG_FILE = "user_selection.json"

# --- CONFIGURATION MAP ---
# Removed zsh and nvim as requested. Only existing folders here.
DOTFILES_MAP = {
    "i3": "~/.config/i3",
    "alacritty": "~/.config/alacritty",
    "polybar": "~/.config/polybar"
}

def run_dialog(cmd):
    """Run dialog and return user input."""
    try:
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        return result.stderr.strip()
    except FileNotFoundError:
        print("Error: 'dialog' is not installed. Install it with: sudo pacman -S dialog")
        sys.exit(1)

def load_config():
    """Load configuration or return default selections."""
    default_config = {
        "packages": ["thunar", "btop", "fastfetch", "alacritty", "rofi", "feh", "firefox", "steam", "git"],
        "ui_features": [
            "i3-wm", "polybar", "picom", "ttf-jetbrains-mono-nerd", 
            "nwg-look", "catppuccin-gtk-theme-mocha", "catppuccin-cursors-mocha", "papirus-icon-theme"
        ],
        "gpu": "AMD"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Load error: {e}")
    return default_config

def save_config(config_data):
    """Save selections to JSON."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        logging.error(f"Save error: {e}")

def make_executable(path):
    """Set +x permission on a file."""
    if os.path.exists(path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def setup_dotfiles():
    """Create symlinks for the existing config folders."""
    print("\n--- Deploying Dotfiles ---")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    common_dir = os.path.join(base_dir, "common")

    for src_name, dest_path in DOTFILES_MAP.items():
        src = os.path.join(common_dir, src_name)
        dest = os.path.expanduser(dest_path)

        os.makedirs(os.path.dirname(dest), exist_ok=True)

        if os.path.exists(src):
            if os.path.exists(dest) or os.path.islink(dest):
                subprocess.run(["rm", "-rf", dest])
            os.symlink(src, dest)
            print(f"✅ Linked: {src_name} -> {dest}")
        else:
            print(f"❌ Error: {src} folder not found in repo.")

    # Fix Polybar script
    polybar_launch = os.path.expanduser("~/.config/polybar/launch.sh")
    make_executable(polybar_launch)

def install_packages(packages):
    """Run pacman installation."""
    if not packages:
        return
    print(f"\n--- Installing Packages ---")
    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "--needed"] + packages)

def main():
    config = load_config()

    while True:
        choice = run_dialog([
            "dialog", "--clear", "--title", " DOTFILES INSTALLER ",
            "--menu", "Adjust your setup selections:", "18", "60", "6",
            "1", "Apps & Steam",
            "2", "UI & Catppuccin Themes",
            "3", "GPU Profile",
            "4", ">>> START INSTALLATION <<<",
            "5", "Exit"
        ])

        if choice == "1":
            apps = ["thunar", "firefox", "btop", "fastfetch", "alacritty", "rofi", "feh", "steam", "git"]
            cmd = ["dialog", "--separate-output", "--checklist", " Select Apps: ", "15", "60", "9"]
            for a in apps:
                status = "on" if a in config["packages"] else "off"
                cmd.extend([a, "", status])
            config["packages"] = run_dialog(cmd).splitlines()
            save_config(config)

        elif choice == "2":
            ui = [
                "i3-wm", "polybar", "picom", "ttf-jetbrains-mono-nerd", 
                "nwg-look", "catppuccin-gtk-theme-mocha", "catppuccin-cursors-mocha", "papirus-icon-theme"
            ]
            cmd = ["dialog", "--separate-output", "--checklist", " Themes & UI: ", "15", "60", "8"]
            for item in ui:
                status = "on" if item in config["ui_features"] else "off"
                cmd.extend([item, "", status])
            config["ui_features"] = run_dialog(cmd).splitlines()
            save_config(config)

        elif choice == "3":
            config["gpu"] = run_dialog([
                "dialog", "--menu", " GPU Driver: ", "12", "40", "2",
                "AMD", "Mesa",
                "Nvidia", "Proprietary"
            ])
            save_config(config)

        elif choice == "4":
            os.system("clear")
            
            # Combine all packages for installation
            to_install = config["packages"] + config["ui_features"]
            if config["gpu"] == "Nvidia":
                to_install.extend(["nvidia-dkms", "nvidia-utils"])

            install_packages(to_install)
            setup_dotfiles()

            print("\n✨ Done. System ready for Catppuccin Mocha.")
            input("\nPress Enter to return...")

        elif choice == "5" or not choice:
            os.system("clear")
            break

if __name__ == "__main__":
    main()
