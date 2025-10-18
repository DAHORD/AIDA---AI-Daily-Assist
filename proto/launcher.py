import subprocess
import sys
import os
import json

# --- Configuration ---
SCRIPT_FR = "assistant_cmd_fr.py"
SCRIPT_EN = "assistant_cmd_en.py"
PYTHON_EXECUTABLE = "python" # On se base sur le PATH

# --- Logique de gestion des paramètres ---

APP_DATA_FOLDER_NAME = "AI Daily Assist" 

def get_app_data_path(filename=""):
    """
    Trouve le dossier AppData\Roaming\AI Daily Assist et retourne le chemin d'un fichier.
    C'est le même dossier que l'assistant utilise pour config.ini et todolist.json.
    """
    try:
        app_data_root = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
        app_folder = os.path.join(app_data_root, APP_DATA_FOLDER_NAME)
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)
        return os.path.join(app_folder, filename)
    except Exception as e:
        print(f"Erreur critique: Impossible d'accéder au dossier AppData : {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

SETTINGS_FILE = get_app_data_path("settings.json")

def load_settings():
    """Charge la langue depuis settings.json. Retourne None si le fichier n'existe pas."""
    if not os.path.exists(SETTINGS_FILE):
        return None
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('language') # Retourne 'fr', 'en', ou None
    except Exception:
        return None # Fichier corrompu ou illisible

def save_settings(lang):
    """Sauvegarde le choix de langue."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'language': lang}, f, indent=4)
    except Exception as e:
        print(f"Erreur: Impossible d'enregistrer les paramètres : {e}")
        input("Appuyez sur Entrée pour quitter...")

def first_run_setup():
    """Pose la question à l'utilisateur pour le premier lancement."""
    print("--- Bienvenue / Welcome to AI Daily Assist ---")
    choix = ""
    while choix not in ['fr', 'en']:
        choix = input("Veuillez choisir votre langue (fr / en): ").lower().strip()
    
    save_settings(choix)
    return choix

def launch_assistant(lang):
    """Lance le script assistant correspondant."""
    script_to_run = SCRIPT_FR if lang == 'fr' else SCRIPT_EN
    command = [PYTHON_EXECUTABLE, script_to_run]
    
    try:
        # Popen lance le script dans un nouveau processus et le launcher se ferme
        subprocess.Popen(command)
        sys.exit(0)
    except FileNotFoundError:
        print(f"Erreur: Impossible de trouver '{PYTHON_EXECUTABLE}' ou '{script_to_run}'.")
        print("Assurez-vous que Python est dans votre PATH.")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur au lancement: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    langue = load_settings()
    
    if langue is None:
        langue = first_run_setup()
    
    launch_assistant(langue)