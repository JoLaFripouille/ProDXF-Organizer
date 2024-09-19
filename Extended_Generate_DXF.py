
import os
import sys
import ezdxf
import Dwg_To_Dxf
import time

def convert_dwg_to_dxf(dwg_file):
    """Convertit un fichier DWG en DXF et enregistre le résultat dans 'OutputDXF'."""
    try:
        # Création du répertoire "OutputDXF" si nécessaire
        output_dir = os.path.abspath("OutputDXF")
        os.makedirs(output_dir, exist_ok=True)

        # Détermination du chemin du fichier DXF à sauvegarder dans "OutputDXF"
        dxf_file_path = os.path.join(output_dir, os.path.basename(dwg_file).replace('.dwg', '.dxf'))

        # Log pour vérifier le chemin du fichier DXF
        print(f"Le fichier DXF sera sauvegardé dans : {dxf_file_path}")

        # Appel de la conversion DWG -> DXF
        Dwg_To_Dxf.convert(dwg_file, dxf_file_path)

        # Vérification que le fichier DXF a bien été créé
        if not os.path.isfile(dxf_file_path):
            raise FileNotFoundError(f"Le fichier DXF '{dxf_file_path}' n'a pas été créé.")

        # Après la conversion, extraire les blocs
        extract_blocks_from_dxf(dxf_file_path, output_dir)

    except Exception as e:
        print(f"Erreur lors de la conversion du fichier DWG : {str(e)}")


def extract_blocks_from_dxf(dxf_file, output_dir):
    """Extrait les blocs d'un fichier DXF et les enregistre dans des fichiers DXF distincts."""
    try:
        # Charger le fichier DXF
        doc = ezdxf.readfile(dxf_file)
        
        # Accéder à la section des blocs
        blocks = doc.blocks

        # Parcourir tous les blocs
        for block_name in blocks.names():
            block = blocks.get(block_name)

            # Créer un nouveau document DXF
            new_doc = ezdxf.new(dxfversion=doc.dxfversion)

            # Créer un nouveau modelspace dans le nouveau document
            new_msp = new_doc.modelspace()

            # Ajouter les entités du bloc au nouveau document
            for entity in block:
                new_msp.add_entity(entity.copy())

            # Enregistrer le fichier DXF extrait
            block_dxf_path = os.path.join(output_dir, f"{block_name}_extracted.dxf")
            new_doc.saveas(block_dxf_path)
            print(f"Bloc '{block_name}' extrait et enregistré dans '{block_dxf_path}'")

    except Exception as e:
        print(f"Erreur lors de l'extraction des blocs : {str(e)}")


# Exemple d'appel de la fonction
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Generate_DXF.py <chemin_du_fichier_DWG>")
    else:
        dwg_file = sys.argv[1]
        convert_dwg_to_dxf(r"D:\PROJECT\AUTOCAD\Chantier\EIFFAGE\Nouveau dossier\454-0_prepa.dwg")
