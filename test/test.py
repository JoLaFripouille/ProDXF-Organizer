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
def obtenir_chemin(event):
    dossiers = event.data.split()  # Séparer les chemins en cas de multiple drops
    nouveaux_chemins = "\n".join(dossiers)  # Convertir les chemins en texte
    label_chemin.configure(text=nouveaux_chemins)  # Remplacer le texte existant par les nouveaux chemins

# Fonction pour choisir un dossier manuellement
def choisir_dossier():
    dossier_selectionne = filedialog.askdirectory()
    if dossier_selectionne:
        label_chemin.configure(text=dossier_selectionne)  # Remplacer le texte existant par le dossier sélectionné

# Création de la fenêtre principale
root = Tk()
root.geometry("800x300")
root.title("Obtenir le chemin du fichier")

# Création d'une frame qui servira de zone de dépôt
zone_depot = ctk.CTkFrame(root, width=300, height=150, border_color="white", border_width=2, corner_radius=10)
zone_depot.pack(side=TOP, padx=10, pady=10, fill="both", expand=True)

# Création d'un label à l'intérieur de la frame pour afficher le chemin déposé
label_chemin = ctk.CTkLabel(zone_depot, text="Déposez les Dossiers ici\n\n\nOu")
label_chemin.pack(expand=True,pady=20)

# Création d'un bouton pour choisir un dossier manuellement
bouton_selection = ctk.CTkButton(zone_depot, text="Sélectionner le Dossier", command=choisir_dossier, height=50, width=200, fg_color="Black", border_width=2)
bouton_selection.pack(expand=True,pady=20)

# Configuration de la zone de dépôt pour accepter le drag-and-drop
zone_depot.drop_target_register(DND_ALL)
zone_depot.dnd_bind("<<Drop>>", obtenir_chemin)

# Ajout d'une nouvelle frame avec un label, une entrée et un bouton
frame_entree = ctk.CTkFrame(root, height=100, border_color="white", border_width=2, corner_radius=10)
frame_entree.pack(side=TOP, padx=10, pady=10, fill="both", expand=True)

label_entree = ctk.CTkLabel(frame_entree, text="Entrez le texte ici :")
label_entree.pack(side="left", padx=5, pady=5)

entree = ctk.CTkEntry(frame_entree)
entree.pack(side="left", padx=5, pady=5, fill="x", expand=True)

bouton_soumettre = ctk.CTkButton(frame_entree, text="Soumettre")
bouton_soumettre.pack(side="right", padx=5, pady=5)

# Lancement de la boucle principale de l'application
root.mainloop()
