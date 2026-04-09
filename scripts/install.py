#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import logging
import stat

logging.basicConfig(
    filename='install.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

CONFIG_FILE = "user_selection.json"

 (~/.config/)
DOTFILES_MAP = {
    "i3": "~/.config/i3",
    "alacritty": "~/.config/alacritty",
    "polybar": "~/.config/polybar",
    "nvim": "~/.config/nvim",
    "zsh": "~/.config/zsh"
}

def run_dialog(cmd):
    try:
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        return result.stderr.strip()
    except FileNotFoundError:
        logging.error("Narzędzie 'dialog' nie jest zainstalowane.")
        sys.exit(1)

def load_config():
    default_config = {
        "packages": ["thunar", "btop", "fastfetch", "alacritty", "rofi"],
        "shell": "zsh",
        "ui_features": ["i3-wm", "polybar", "picom", "ttf-jetbrains-mono-nerd"],
        "gpu": "AMD"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Błąd wczytywania configu: {e}")
    return default_config

def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        logging.error(f"Błąd zapisu: {e}")

def make_executable(path):

    if os.path.exists(path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        logging.info(f"Nadano uprawnienia +x: {path}")

def setup_dotfiles():

    print("\n--- Deploying Dotfiles (Frutiger Aero Setup) ---")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    common_dir = os.path.join(base_dir, "common")

    for src_name, dest_path in DOTFILES_MAP.items():
        src = os.path.join(common_dir, src_name)
        dest = os.path.expanduser(dest_path)


        os.makedirs(os.path.dirname(dest), exist_ok=True)

        if os.path.exists(src):
            if os.path.exists(dest) or os.path.islink(dest):
                print(f"⚠️  Target {dest} exists. Skipping link.")
            else:
                os.symlink(src, dest)
                print(f"✅ Linked: {src_name} -> {dest}")
                logging.info(f"Utworzono symlink: {src} -> {dest}")
        else:
            print(f"❌ Source {src} not found in common/ folder.")


    polybar_launch = os.path.expanduser("~/.config/polybar/launch.sh")
    make_executable(polybar_launch)

def install_packages(packages):
    if not packages:
        return
    print(f"\n--- Instalowanie: {', '.join(packages)} ---")

    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "--needed"] + packages)

def main():
    config = load_config()

    while True:
        main_choice = run_dialog([
            "dialog", "--clear", "--title", " INSTALACJA DOTFILES ",
            "--menu", "Wybory są zapamiętywane w JSON:", "18", "60", "6",
            "1", "Pakiety systemowe (Apps)",
            "2", "Wybór powłoki (Shell/ZSH)",
            "3", "GPU Profile (RX 9070XT / Nvidia)",
            "4", "Wygląd (i3, Polybar, Picom)",
            "5", ">>> ROZPOCZNIJ INSTALACJĘ I LINKOWANIE <<<",
            "6", "Wyjście"
        ])

        if main_choice == "1":
            pkgs = ["thunar", "firefox", "btop", "fastfetch", "alacritty", "rofi", "feh"]
            cmd = ["dialog", "--separate-output", "--checklist", " Wybierz pakiety: ", "15", "60", "7"]
            for p in pkgs:
                status = "on" if p in config["packages"] else "off"
                cmd.extend([p, "", status])
            config["packages"] = run_dialog(cmd).splitlines()
            save_config(config)

        elif main_choice == "2":
            config["shell"] = run_dialog([
                "dialog", "--menu", " Wybierz Shell: ", "12", "40", "3",
                "zsh", "Z-Shell (Recommended)",
                "bash", "Standardowy Bash",
                "fish", "Friendly Shell"
            ])
            save_config(config)

        elif main_choice == "3":
            config["gpu"] = run_dialog([
                "dialog", "--menu", " Profil GPU: ", "12", "40", "2",
                "AMD", "Mesa",
                "Nvidia", "Proprietary Drivers"
            ])
            save_config(config)

        elif main_choice == "4":
            features = ["i3-wm", "polybar", "picom", "ttf-jetbrains-mono-nerd"]
            cmd = ["dialog", "--separate-output", "--checklist", " UI Setup: ", "15", "60", "4"]
            for f in features:
                status = "on" if f in config["ui_features"] else "off"
                cmd.extend([f, "", status])
            config["ui_features"] = run_dialog(cmd).splitlines()
            save_config(config)

        elif main_choice == "5":
            os.system("clear")
            all_to_install = config["packages"] + config["ui_features"]
            if config["shell"] != "bash":
                all_to_install.append(config["shell"])
            install_packages(all_to_install)


            setup_dotfiles()





            input("\n✅ Wszystko gotowe! Enter, by wrócić...")

        elif main_choice == "6" or not main_choice:
            os.system("clear")
            break

if __name__ == "__main__":
    main()
