import subprocess
import sys
import os
from setuptools import setup, find_packages

# Ajout de plus de messages de débogage
print("Vérification de la plateforme...")
if sys.platform.startswith("linux"):
    print("Plateforme Linux détectée.")
    if os.path.exists("install.sh"):
        print("Fichier install.sh trouvé.")
        try:
            subprocess.check_call(["bash", "install.sh"])
            print("install.sh exécuté avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de install.sh: {e}")
    else:
        print("install.sh n'est pas trouvé.")
else:
    print("La plateforme n'est pas Linux, le script install.sh ne sera pas exécuté.")

setup(
    name="LCD_16x2",
    version="0.1.0-alpha6",
    packages=["lcd_16x2",
              "lcd_16x2.drivers",
              "lcd_16x2.emulators",
              "demo"],
    install_requires=['requests~=2.32.3',
                      'beautifulsoup4~=4.13.3',
                      'setuptools~=78.1.0'],
    author="Matthew Timmons-Brown (the-raspberry-pi-guy)",
    maintainer="https://github.com/the-raspberry-pi-guy/lcd/contributors",
    description="Python package for interfacing with a 16x2 character I2C liquid-crystal display (LCD).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/the-raspberry-pi-guy/lcd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
)
