import os
import re
import logging

# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Définition des motifs pour ignorer certains fichiers DXF
patterns = [
    re.compile(r".+_.+_qte-\d+\.dxf", re.IGNORECASE),  # Motif pour ignorer les fichiers avec "_qte-<nombre>.dxf"
]

def get_subfolders_with_valid_dxf(folder_path):
    """
    Récupère les sous-dossiers contenant des fichiers DXF valides (non ignorés par les motifs).

    :param folder_path: Chemin du dossier principal à analyser.
    :return: Un dictionnaire contenant les sous-dossiers et leurs fichiers DXF valides avec une quantité initiale de 0.
    """
    subfolders_with_valid_dxf = {}  # Dictionnaire pour stocker les sous-dossiers et leurs fichiers valides

    try:
        # Liste tous les sous-dossiers dans le dossier principal
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        logging.debug(f"Nombre de sous-dossiers trouvés : {len(subfolders)}")

        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)  # Chemin complet du sous-dossier
            dxf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.dxf')]  # Liste des fichiers DXF
            valid_dxf_files = [f for f in dxf_files if not any(p.search(f) for p in patterns)]  # Filtres les fichiers valides

            # Si des fichiers valides sont trouvés, on les ajoute avec une quantité nulle par défaut
            if valid_dxf_files:
                subfolders_with_valid_dxf[subfolder] = {f: 0 for f in valid_dxf_files}
                logging.debug(f"Fichiers .dxf affichés (non ignorés) dans {subfolder_path} : {valid_dxf_files}")

        # Affichage structuré des sous-dossiers et fichiers à traiter
        print("\nListe des sous-dossiers et des fichiers à traiter :")
        for subfolder, files in subfolders_with_valid_dxf.items():
            print(f'    _"{subfolder}":')
            for file in files:
                print(f'        -"{file}"')

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des sous-dossiers et fichiers : {e}")

    return subfolders_with_valid_dxf

def delete_file_or_folder(subfolders_with_valid_dxf, subfolder_name, file_name=None):
    """
    Supprime un fichier spécifique ou un dossier entier du dictionnaire des sous-dossiers avec fichiers DXF valides.

    :param subfolders_with_valid_dxf: Dictionnaire contenant les sous-dossiers et fichiers DXF valides.
    :param subfolder_name: Nom du sous-dossier à traiter.
    :param file_name: Nom du fichier à supprimer. Si None, supprime le sous-dossier entier.
    """
    try:
        # Vérifie si le sous-dossier existe dans le dictionnaire
        if subfolder_name in subfolders_with_valid_dxf:
            if file_name:
                # Supprime un fichier spécifique dans le sous-dossier
                if file_name in subfolders_with_valid_dxf[subfolder_name]:
                    del subfolders_with_valid_dxf[subfolder_name][file_name]
                    logging.debug(f"Fichier '{file_name}' supprimé du sous-dossier '{subfolder_name}'.")

                    # Si le sous-dossier est vide après suppression, on supprime aussi le sous-dossier
                    if not subfolders_with_valid_dxf[subfolder_name]:
                        del subfolders_with_valid_dxf[subfolder_name]
                        logging.debug(f"Le sous-dossier '{subfolder_name}' est vide et a été supprimé.")
            else:
                # Supprime un sous-dossier entier
                del subfolders_with_valid_dxf[subfolder_name]
                logging.debug(f"Le sous-dossier '{subfolder_name}' a été supprimé.")
        else:
            logging.error(f"Le sous-dossier '{subfolder_name}' n'existe pas dans la liste des dossiers à traiter.")
    except Exception as e:
        logging.error(f"Erreur lors de la suppression du fichier ou dossier : {e}")

# Exemple d'utilisation pour tester les fonctions (à commenter ou supprimer en production)
if __name__ == "__main__":
    # Exemple de chemin du dossier principal à analyser
    folder_path = "D:/PROJECT/AUTOCAD/Chantier/EIFFAGE/15183 TOLERIE/DXF"
    
    # Récupère les sous-dossiers avec des fichiers DXF valides
    subfolders_with_valid_dxf = get_subfolders_with_valid_dxf(folder_path)

    # Suppression d'un fichier spécifique dans un sous-dossier
    delete_file_or_folder(subfolders_with_valid_dxf, 'EZ-3', 'TL25.dxf')
    # Suppression d'un sous-dossier entier
    delete_file_or_folder(subfolders_with_valid_dxf, 'ACIER-10')

    # Affiche l'état du dictionnaire après suppression pour vérification
    print("\nÉtat après suppression :")
    for subfolder, files in subfolders_with_valid_dxf.items():
        print(f'    _"{subfolder}":')
        for file in files:
            print(f'        -"{file}"')
