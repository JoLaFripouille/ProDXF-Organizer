import os
import re
import shutil
from tkinter import messagebox

# Fonction pour trouver les fichiers DXF dans un répertoire donné
def find_dxf_files(directory):
    dxf_files = []
    for root_dir, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dxf'):
                dxf_files.append(os.path.join(root_dir, file))
    return dxf_files

# Fonction pour extraire le nom de l'acier et l'épaisseur d'un dossier
def extract_info_from_directory(directory):
    # Suppression des underscores ou des tirets et ajout d'espace
    clean_directory = re.sub(r"[_-]", " ", directory)
    # Extraction des lettres et des chiffres séparément
    match = re.match(r'([a-zA-Z\s]+)([\d.,]+)', clean_directory)
    if match:
        name = match.group(1).strip()
        thickness = match.group(2).replace(',', '.') + "mm"
        return name, thickness
    return "", ""

# Fonction pour renommer les fichiers DXF
def rename_dxf_files(directory, files_entries):
    for old_name, new_name in files_entries.items():
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        try:
            os.rename(old_path, new_path)
            print(f"Fichier renommé : {old_name} -> {new_name}")
        except Exception as e:
            print(f"Erreur lors du renommage de {old_name} : {e}")

# Fonction pour extraire le numéro de commande depuis le dossier
def extract_order_number(directory):
    # Extraction d'un potentiel numéro de commande (personnalisable)
    match = re.search(r'commande\s*(\d+)', directory, re.IGNORECASE)
    return match.group(1) if match else "Inconnu"

# Fonction pour extraire le nom du client depuis le dossier
def extract_client_name(directory):
    # Extraction d'un potentiel nom de client (personnalisable)
    match = re.search(r'client\s*([a-zA-Z\s]+)', directory, re.IGNORECASE)
    return match.group(1).strip() if match else "Inconnu"

# Fonction pour ouvrir Gmail avec le sujet et le corps de l'email pré-remplis
def open_gmail(subject, body):
    import webbrowser
    body = body.replace('\n', '%0D%0A')  # Conversion des sauts de ligne pour URL
    webbrowser.open(f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={subject}&body={body}")
