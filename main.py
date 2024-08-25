from tkinter import TOP, filedialog
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
import src  # Importation du fichier src.py

# Création de la classe principale en héritant de ctk.CTk et TkinterDnD.DnDWrapper
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# Configuration de l'apparence de l'interface
ctk.set_appearance_mode("dark")

# Fonction pour récupérer le chemin déposé
def get_path(event):
    paths = src.get_dropped_paths(event)
    pathLabel.configure(text="\n".join(paths))
    show_canvas()
    src.display_dxf_files(paths, canvas)

# Fonction pour choisir un dossier manuellement
def select_directory():
    folder_selected = src.select_directory_manually(filedialog)
    if folder_selected:
        pathLabel.configure(text=folder_selected)
        show_canvas()
        src.display_dxf_files([folder_selected], canvas)

# Fonction pour afficher le canvas uniquement si un dossier est sélectionné
def show_canvas():
    if not canvas.winfo_ismapped():  # Vérifie si le canvas n'est pas déjà affiché
        canvas.pack(side=TOP, padx=10, pady=10, fill="both", expand=True)

# Création de la fenêtre principale
root = Tk()
root.geometry("800x400")
root.title("Gestion des fichiers DXF")

# Création d'une frame qui servira de zone de dépôt
drop_frame = ctk.CTkFrame(root, width=300, height=150, border_color="white", border_width=2, corner_radius=10)
drop_frame.pack(side=TOP, padx=10, pady=10, fill="both", expand=True)

# Création d'un label à l'intérieur de la frame pour afficher le chemin déposé
pathLabel = ctk.CTkLabel(drop_frame, text="Déposez le Dossier ici\n\n\nOu")
pathLabel.pack(expand=True)

# Création d'un bouton pour choisir un dossier manuellement
select_button = ctk.CTkButton(drop_frame, text="Sélectionner le Dossier", command=select_directory, height=50, width=200, fg_color="Black", border_width=2)
select_button.pack(expand=True)

# Création du canvas, mais on ne l'affiche pas encore (pas de pack/place/grid)
canvas = ctk.CTkCanvas(root, width=780, height=200, bg="black")

# Configuration de la zone de dépôt pour accepter le drag-and-drop
drop_frame.drop_target_register(DND_ALL)
drop_frame.dnd_bind("<<Drop>>", get_path)

# Lancement de la boucle principale de l'application
root.mainloop()
