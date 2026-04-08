#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import logging
from datetime import datetime


logging.basicConfig(
    filename='install.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

CONFIG_FILE = "user_selection.json"

def run_dialog(cmd):
    try:
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        return result.stderr.strip()
    except FileNotFoundError:
        logging.error("Narzędzie 'dialog' nie jest zainstalowane.")
        sys.exit(1)

def load_config():
    """Wczytuje poprzednie wybory z pliku JSON, jeśli istnieje."""
    default_config = {
        "packages": ["thunar", "btop", "fastfetch"], # domyślne
        "shell": "bash",
        "ui_features": ["i3-wm", "polybar", "picom"],
        "gpu": "none"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                logging.info("Wczytano istniejącą konfigurację z pliku.")
                return json.load(f)
        except Exception as e:
            logging.error(f"Błąd wczytywania configu: {e}")
    return default_config

def save_config(config_data):
    """Zapisuje aktualne wybory do JSON."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        logging.info("Zapisano wybory do pliku JSON.")
    except Exception as e:
        logging.error(f"Błąd zapisu: {e}")

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
            "--menu", "Twoje wybory są automatycznie zapamiętywane:", "18", "60", "6",
            "1", "Pakiety systemowe",
            "2", "Wybór powłoki (Shell)",
            "3", "GPU Profile (AMD/Nvidia)",
            "4", "Wygląd (i3, Polybar, Picom)",
            "5", ">>> ROZPOCZNIJ INSTALACJĘ <<<",
            "6", "Wyjście"
        ])

        if main_choice == "1":
            pkgs = ["thunar", "firefox", "btop", "fastfetch"]
            cmd = ["dialog", "--separate-output", "--checklist", " Wybierz pakiety: ", "15", "60", "5"]
            for p in pkgs:
                status = "on" if p in config["packages"] else "off"
                cmd.extend([p, "", status])
            
            config["packages"] = run_dialog(cmd).splitlines()
            save_config(config) # Zapisz od razu po zmianie

        elif main_choice == "2":
            config["shell"] = run_dialog([
                "dialog", "--menu", " Wybierz Shell: ", "12", "40", "3",
                "zsh", "Z-Shell",
                "bash", "Standardowy Bash",
                "fish", "Friendly Shell"
            ])
            save_config(config)

        elif main_choice == "3":
            config["gpu"] = run_dialog([
                "dialog", "--menu", " Profil GPU: ", "12", "40", "2",
                "AMD", "Mesa",
                "Nvidia", "Proprietary"
            ])
            save_config(config)

        elif main_choice == "4":
            features = ["i3-wm", "polybar", "picom"]
            cmd = ["dialog", "--separate-output", "--checklist", " UI Setup: ", "15", "60", "3"]
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
            input("\nInstalacja gotowa. Enter, by wrócić...")

        elif main_choice == "6" or not main_choice:
            os.system("clear")
            break

if __name__ == "__main__":
    main()
