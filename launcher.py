import subprocess
import sys
import os

# --- Configuration ---
# 1. Le nom du script Python à exécuter
SCRIPT_TO_RUN = "assistant_cmd.py"

# 2. Le chemin de l'interpréteur Python
#    Puisque vous ne voulez pas relancer le launcher.exe, nous allons
#    chercher l'interpréteur Python 'standard' sur le système.
#    Attention: Ceci fonctionne si l'utilisateur a Python installé ET accessible via PATH.
PYTHON_EXECUTABLE = "python" # On se base sur le PATH, ou utilisez un chemin absolu si connu (ex: r"C:\Python310\python.exe")

def launch_script():
    """Tente de lancer le script assistant_cmd.py en utilisant l'interpréteur Python."""
    
    # 3. Construire la commande
    # [Interpréteur Python, Script à lancer, Arguments optionnels]
    command = [PYTHON_EXECUTABLE, SCRIPT_TO_RUN]
    
    try:
        # Lancement du script. 
        # Utilisez 'Popen' pour que le launcher puisse se fermer immédiatement.
        print(f"Lancement de {SCRIPT_TO_RUN} avec l'interpréteur : {PYTHON_EXECUTABLE}")
        subprocess.Popen(command)
        
        # 4. Le launcher se ferme. L'application principale tourne en arrière-plan.
        sys.exit(0) 

    except FileNotFoundError:
        # Cette erreur peut signifier que 'python' n'est pas dans le PATH ou que le script est absent.
        print(f"Erreur: Impossible de trouver l'interpréteur '{PYTHON_EXECUTABLE}' ou le script '{SCRIPT_TO_RUN}'.")
        print("Assurez-vous que Python est installé et que le script est au bon endroit.")
        # Empêche la console de se fermer immédiatement pour que l'utilisateur lise l'erreur
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    # Vérification que le script est bien présent à côté du launcher
    if not os.path.exists(SCRIPT_TO_RUN):
        print(f"Erreur: Le script principal '{SCRIPT_TO_RUN}' est introuvable.")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
        
    launch_script()