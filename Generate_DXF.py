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
        
        print(f"Conversion réussie : {dwg_file} -> {dxf_file_path}")
        return dxf_file_path
    except Exception as e:
        print(f"Erreur lors de la conversion DWG en DXF : {e}")
        sys.exit(1)

def determine_target_directory(dwg_file):
    """Détermine le répertoire cible pour enregistrer les blocs extraits."""
    dwg_dir = os.path.dirname(dwg_file)
    existing_dirs = [d.lower() for d in os.listdir(dwg_dir)]
    if "dxf" not in existing_dirs and "laser" not in existing_dirs:
        target_dir = os.path.join(dwg_dir, "DXF")
        os.makedirs(target_dir, exist_ok=True)
    else:
        target_dir = os.path.join(dwg_dir, [d for d in os.listdir(dwg_dir) if d.lower() in {"dxf", "laser"}][0])
    return target_dir

def list_existing_dxf_files(dwg_dir):
    """Liste tous les fichiers DXF dans les sous-dossiers des répertoires DXF et Laser et affiche les détails pour débogage."""
    existing_dxf_files = []
    print("\nRecherche des répertoires existants (DXF, Laser) et des fichiers DXF :")
    for root, dirs, files in os.walk(dwg_dir):
        # Vérifier si le dossier parent ou un sous-dossier appartient à DXF ou Laser
        if any(part.lower() in {"dxf", "laser"} for part in root.split(os.sep)):
            print(f"Dossier trouvé : {root}")
            for file in files:
                if file.lower().endswith('.dxf'):
                    existing_dxf_files.append(os.path.splitext(file)[0])
                    print(f"    Fichier DXF trouvé : {file}")
    return existing_dxf_files

def extract_blocks(input_dxf, target_dir, prefix, suffix, existing_dxf_files):
    """Extrait les blocs d'un fichier DXF qui respectent le préfixe et suffixe spécifiés et vérifie si déjà traités."""
    try:
        doc = ezdxf.readfile(input_dxf)
        msp = doc.modelspace()
        blocks_by_layer = {}
        blocks_already_processed = []

        for entity in msp.query('INSERT'):
            block_name = entity.dxf.name
            layer_name = entity.dxf.layer

            # Vérifier si le nom du bloc commence par le préfixe et finit par le suffixe
            if block_name.startswith(prefix) and block_name.endswith(suffix):
                # Retirer le suffixe du nom du bloc pour la comparaison
                clean_block_name = block_name.removesuffix(suffix)

                # Vérifier si le bloc a déjà été traité
                if any(existing_name.startswith(clean_block_name) for existing_name in existing_dxf_files):
                    print(f"Le bloc '{block_name}' a déjà été traité et ne sera pas extrait.")
                    blocks_already_processed.append(block_name)
                    continue

                # Enregistrer le bloc si non traité
                if layer_name not in blocks_by_layer:
                    blocks_by_layer[layer_name] = []
                blocks_by_layer[layer_name].append(clean_block_name)

                if block_name in doc.blocks:
                    block = doc.blocks.get(block_name)
                    layer_folder = os.path.join(target_dir, layer_name)
                    os.makedirs(layer_folder, exist_ok=True)
                    output_dxf = os.path.join(layer_folder, f"{clean_block_name}.dxf")
                    new_doc = ezdxf.new()
                    new_msp = new_doc.modelspace()
                    new_block = new_doc.blocks.new(name=block_name)

                    try:
                        for e in block:
                            new_block.add_entity(e.copy())
                    except Exception as copy_error:
                        print(f"Erreur lors de la copie des entités du bloc '{block_name}': {copy_error}")
                        continue

                    try:
                        new_msp.add_blockref(block_name, entity.dxf.insert)
                        new_doc.saveas(output_dxf)
                        print(f"Bloc '{clean_block_name}' extrait et enregistré dans {output_dxf}")
                    except Exception as save_error:
                        print(f"Erreur lors de la sauvegarde du bloc '{clean_block_name}': {save_error}")

        print("\nListe des blocs extraits par calque :")
        for layer, blocks in blocks_by_layer.items():
            print(f"Calque '{layer}': {', '.join(blocks)}")

        print("\nBlocs qui n'ont pas besoin d'être traités :")
        for block in blocks_already_processed:
            print(f"  - {block}")

    except Exception as e:
        print(f"Erreur lors du traitement du fichier DXF : {e}")

def clear_directory(directory):
    """Supprime tous les fichiers du dossier spécifié."""
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Tous les fichiers du dossier '{directory}' ont été supprimés.")
    except Exception as e:
        print(f"Erreur lors de la suppression des fichiers dans '{directory}': {e}")

def process_dwg(dwg_file, prefix, suffix):
    """Processus principal pour convertir DWG en DXF, extraire les blocs et nettoyer."""
    dxf_file_path = convert_dwg_to_dxf(dwg_file)
    target_dir = determine_target_directory(dwg_file)
    existing_dxf_files = list_existing_dxf_files(os.path.dirname(dwg_file))
    extract_blocks(dxf_file_path, target_dir, prefix, suffix, existing_dxf_files)
    time.sleep(4)
    clear_directory(os.path.dirname(dxf_file_path))
