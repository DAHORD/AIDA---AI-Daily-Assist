import subprocess
import sys
import os

# --- Configuration ---
SCRIPT_TO_RUN = "assistant_cmd.py" # IMPORTANT: Make sure this matches the English script name
PYTHON_EXECUTABLE = "python"

def launch_script():
    """Attempts to launch the assistant_cmd.py script using the Python interpreter."""

    command = [PYTHON_EXECUTABLE, SCRIPT_TO_RUN]
    
    try:
        print(f"Launching {SCRIPT_TO_RUN} with interpreter: {PYTHON_EXECUTABLE}")
        subprocess.Popen(command)
        sys.exit(0) 

    except FileNotFoundError:
        print(f"Error: Could not find the interpreter '{PYTHON_EXECUTABLE}' or the script '{SCRIPT_TO_RUN}'.")
        print("Please ensure Python is installed and accessible via PATH, and that the script is in the correct location.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    # Verify that the main script exists alongside the launcher
    if not os.path.exists(SCRIPT_TO_RUN):
        print(f"Error: Main script '{SCRIPT_TO_RUN}' not found.")
        input("Press Enter to exit...")
        sys.exit(1)
        
    launch_script()