import os
import re

# Fonction pour récupérer les chemins des dossiers déposés
def get_dropped_paths(event):
    return event.data.replace("{", "").replace("}", "").split()

# Fonction pour choisir un dossier manuellement
def select_directory_manually(filedialog):
    folder_selected = filedialog.askdirectory()
    return folder_selected if folder_selected else None

# Fonction pour afficher les fichiers .dxf dans le canvas
def display_dxf_files(paths, canvas):
    canvas.delete("all")  # Effacer le contenu précédent du canvas
    y_position = 10

    # Motif à ignorer
    ignore_pattern = re.compile(r'.+_.+mm_qte-\d+\.dxf$', re.IGNORECASE)

    for path in paths:
        for root_dir, dirs, files in os.walk(path):
            # Filtrer les fichiers .dxf qui ne correspondent pas au motif à ignorer
            dxf_files = [f for f in files if f.lower().endswith('.dxf') and not ignore_pattern.match(f)]
            if dxf_files:
                canvas.create_text(10, y_position, anchor="nw", text=f"Dossier: {os.path.basename(root_dir)}", fill="white", font=("Arial", 12, "bold"))
                y_position += 20
                for file in dxf_files:
                    canvas.create_text(20, y_position, anchor="nw", text=f"- {file}", fill="white", font=("Arial", 10))
                    y_position += 20
            else:
                canvas.create_text(10, y_position, anchor="nw", text=f"Dossier: {os.path.basename(root_dir)} (Aucun fichier DXF)", fill="white", font=("Arial", 12, "bold"))
                y_position += 40
