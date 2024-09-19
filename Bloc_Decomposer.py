import os
import sys
import ezdxf


def decompose_blocks_in_dxf(dxf_file):
    """Décompose tous les blocs dans un fichier DXF et remplace le fichier d'origine."""
    try:
        # Vérification que le fichier DXF existe
        if not os.path.isfile(dxf_file):
            raise FileNotFoundError(f"Le fichier DXF '{dxf_file}' n'a pas été trouvé.")

        # Charger le fichier DXF
        doc = ezdxf.readfile(dxf_file)

        # Créer un nouveau document DXF pour les entités décomposées
        new_doc = ezdxf.new(dxfversion=doc.dxfversion)
        new_msp = new_doc.modelspace()

        # Décomposer les blocs insérés dans le modèle (Modelspace)
        msp = doc.modelspace()

        for entity in msp.query("INSERT"):
            block_name = entity.dxf.name
            block = doc.blocks.get(block_name)

            # Parcourir les entités du bloc et les ajouter au nouveau modelspace
            for block_entity in block:
                # Ajouter chaque entité du bloc au nouveau fichier DXF
                new_msp.add_entity(block_entity.copy())

        # Enregistrer le fichier DXF décomposé au même emplacement que l'original
        new_doc.saveas(dxf_file)
        print(f"Fichier décomposé enregistré et remplacé : {dxf_file}")

    except Exception as e:
        print(f"Erreur lors de la décomposition des blocs : {str(e)}")
