import subprocess
import os

def run_install():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    if os.path.exists(script_path):
        print(f"Exécution de {script_path}...")
        subprocess.run(["bash", script_path], check=True)
    else:
        print("install.sh introuvable dans le package.")
