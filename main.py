from tkinter import TOP, filedialog
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk

# Création de la classe principale en héritant de ctk.CTk et TkinterDnD.DnDWrapper
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# Configuration de l'apparence de l'interface
ctk.set_appearance_mode("dark")

# Fonction pour récupérer le chemin déposé
def get_path(event):
    pathLabel.configure(text=event.data)

# Fonction pour choisir un dossier manuellement
def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        pathLabel.configure(text=folder_selected)

# Création de la fenêtre principale
root = Tk()
root.geometry("800x200")
root.title("Get file path")

# Création d'une frame qui servira de zone de dépôt
drop_frame = ctk.CTkFrame(root, width=300, height=150, border_color="white", border_width=2, corner_radius=10)
drop_frame.pack(side=TOP, padx=10, pady=10, fill="both", expand=True)

# Création d'un label à l'intérieur de la frame pour afficher le chemin déposé
pathLabel = ctk.CTkLabel(drop_frame, text="Déposez le Dossier ici\n\n\nOu")
pathLabel.pack(expand=True)

# Création d'un bouton pour choisir un dossier manuellement
select_button = ctk.CTkButton(drop_frame, text="Selectionner le Dossier", command=select_directory,height=50,width=200, fg_color="Black",border_width=2)
select_button.pack(expand=True)

# Configuration de la zone de dépôt pour accepter le drag-and-drop
drop_frame.drop_target_register(DND_ALL)
drop_frame.dnd_bind("<<Drop>>", get_path)

# Lancement de la boucle principale de l'application
root.mainloop()
