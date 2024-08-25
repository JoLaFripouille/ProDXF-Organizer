import os

def process_paths(paths):
    """
    Fonction pour traiter les chemins des dossiers déposés ou sélectionnés.
    Vérifie si les dossiers contiennent des fichiers .dxf.
    """
    for path in paths:
        if os.path.isdir(path):
            print(f"Dossier trouvé : {path}")
            # Rechercher des fichiers .dxf dans le dossier
            dxf_files = [f for f in os.listdir(path) if f.lower().endswith('.dxf')]
            if dxf_files:
                print(f"Fichiers DXF trouvés dans {path} : {dxf_files}")
            else:
                print(f"Aucun fichier DXF trouvé dans {path}.")
        else:
            print(f"Chemin non valide : {path}")

def find_chrome_executable():
    """
    Fonction pour trouver le chemin de 'chrome.exe'.
    """
    for root, dirs, files in os.walk("C:\\"):
        if 'chrome.exe' in files:
            return os.path.join(root, 'chrome.exe')
    return "chrome.exe non trouvé"
