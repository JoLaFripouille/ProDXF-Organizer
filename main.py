import os
import re
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
from tkinter import filedialog
from src import find_dxf_files, rename_dxf_files

# Création de la classe principale en héritant de ctk.CTk et TkinterDnD.DnDWrapper
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        self.setup_ui()

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        self.geometry("800x600")
        self.title("Gestionnaire de Fichiers DXF")

        # Création d'une frame qui servira de zone de dépôt
        self.drop_frame = ctk.CTkFrame(self, width=300, height=150, border_color="white", border_width=2, corner_radius=10)
        self.drop_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Création d'un label à l'intérieur de la frame pour afficher le chemin déposé
        self.pathLabel = ctk.CTkLabel(self.drop_frame, text="Déposez le Dossier ici\n\n\nOu")
        self.pathLabel.pack(expand=True)

        # Création d'un bouton pour choisir un dossier manuellement
        select_button = ctk.CTkButton(self.drop_frame, text="Sélectionner le Dossier", command=self.select_directory, height=50, width=200, fg_color="black", border_width=2)
        select_button.pack(expand=True)

        # Configuration de la zone de dépôt pour accepter le drag-and-drop
        self.drop_frame.drop_target_register(DND_ALL)
        self.drop_frame.dnd_bind("<<Drop>>", self.get_path)

        # Création d'un canvas pour afficher les fichiers DXF trouvés
        self.canvas = ctk.CTkCanvas(self, height=300, bg="black")
        self.canvas.pack(padx=10, pady=10, fill="both", expand=True)
        self.canvas.pack_forget()  # Masquer le canvas au départ

    def get_path(self, event):
        paths = event.data.replace("{", "").replace("}", "").split()
        self.display_dxf_files(paths)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.display_dxf_files([directory])

    def display_dxf_files(self, paths):
        dxf_files = []
        for path in paths:
            dxf_files.extend(find_dxf_files(path))

        # Afficher les fichiers dans le canvas seulement s'il y a des fichiers DXF
        if dxf_files:
            self.canvas.pack()  # Afficher le canvas
            self.canvas.delete("all")  # Effacer le contenu précédent du canvas
            y_position = 10

            ignore_pattern = re.compile(r'.+_.+_qte-\d+\.dxf$', re.IGNORECASE)
            for file_path in dxf_files:
                if not ignore_pattern.match(os.path.basename(file_path)):
                    self.canvas.create_text(10, y_position, anchor="nw", text=f"{os.path.basename(file_path)}", fill="white", font=("Arial", 10))
                    y_position += 20
        else:
            self.canvas.pack_forget()  # Masquer le canvas s'il n'y a pas de fichiers DXF


# Création de la fenêtre principale
if __name__ == "__main__":
    app = Tk()
    app.mainloop()
