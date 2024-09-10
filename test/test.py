import customtkinter as ctk
from tkinter import filedialog
import os
import logging
import re

# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Définition des patterns pour ignorer les fichiers .dxf
patterns = [
    re.compile(r".+_.+_qte-\d+\.dxf", re.IGNORECASE),  # Premier motif
    re.compile(r".+_.+_qte-\d+\.dxf", re.IGNORECASE)   # Deuxième motif (identique pour exemple)
]

# Initialisation de l'application
ctk.set_appearance_mode("dark")  # Définit le mode sombre
ctk.set_default_color_theme("dark-blue")  # Thème par défaut

class FolderSelectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("Sélectionnez un Dossier")
        self.geometry("800x600")
        
        # Bouton pour sélectionner un dossier
        self.select_button = ctk.CTkButton(self, text="Sélectionnez un dossier", command=self.select_folder)
        self.select_button.pack(pady=20)
        
        # Label pour afficher le chemin du dossier sélectionné
        self.folder_label = ctk.CTkLabel(self, text="")
        self.folder_label.pack(pady=10)
        
        # Frame pour contenir les sous-dossiers et leurs fichiers avec scrollbar (initialement cachée)
        self.subfolders_scroll_frame = ctk.CTkScrollableFrame(self)
        # Ne pas pack ici pour ne pas l'afficher immédiatement
        
        # Dictionnaire pour garder une trace des sous-dossiers et de leurs frames
        self.subfolder_frames = {}
        
        # Dictionnaire pour stocker les quantités saisies par l'utilisateur
        self.quantities = {}

    def select_folder(self):
        # Ouvre une fenêtre de dialogue pour sélectionner un dossier
        folder_path = filedialog.askdirectory()
        if folder_path:
            logging.debug(f"Dossier sélectionné : {folder_path}")
            # Met à jour le label avec le chemin du dossier sélectionné
            self.folder_label.configure(text=folder_path)
            
            # Afficher la subfolders_scroll_frame seulement après la sélection d'un dossier
            self.subfolders_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Afficher les sous-dossiers
            self.display_subfolders(folder_path)
        else:
            logging.debug("Aucun dossier sélectionné.")
    
    def display_subfolders(self, folder_path):
        # Efface le contenu précédent de la frame scrollable
        for widget in self.subfolders_scroll_frame.winfo_children():
            widget.destroy()
        
        # Liste tous les sous-dossiers dans le dossier sélectionné
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        logging.debug(f"Nombre de sous-dossiers trouvés : {len(subfolders)}")
        
        # Mise à jour du dictionnaire de frames
        self.subfolder_frames = {}
        
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)
            logging.debug(f"Affichage du sous-dossier : {subfolder}")
            
            # Crée une frame pour chaque sous-dossier avec un "contour"
            subfolder_frame = ctk.CTkFrame(self.subfolders_scroll_frame, fg_color="gray20")  # Contour de couleur
            subfolder_frame.pack(fill="x", padx=5, pady=5)
            
            # Ajoute une bordure intérieure pour simuler un contour
            inner_frame = ctk.CTkFrame(subfolder_frame, fg_color="gray30", corner_radius=5)
            inner_frame.pack(fill="both", padx=2, pady=2, expand=True)
            
            # Affiche le nom du sous-dossier
            subfolder_label = ctk.CTkLabel(inner_frame, text=subfolder)
            subfolder_label.pack(padx=10, pady=5)
            
            # Bouton pour supprimer uniquement la frame (sous le label)
            delete_folder_frame_button = ctk.CTkButton(
                inner_frame, 
                text="Supprimer ce Dossier", 
                command=lambda sf_frame=subfolder_frame: self.delete_subfolder_frame(sf_frame),
                fg_color="red"
            )
            delete_folder_frame_button.pack(padx=10, pady=5)  # Positionné en dessous du label
            
            # Ajoute le sous-dossier à la liste des frames pour le suivi
            self.subfolder_frames[subfolder] = subfolder_frame
            
            # Affiche les fichiers .dxf dans chaque sous-dossier
            self.display_dxf_files(subfolder_path, inner_frame)
    
    def display_dxf_files(self, subfolder_path, parent_frame):
        # Liste tous les fichiers .dxf dans le sous-dossier
        dxf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.dxf')]
        logging.debug(f"Fichiers .dxf trouvés dans {subfolder_path} : {dxf_files}")
        
        # Filtre les fichiers à ignorer selon les patterns
        filtered_dxf_files = [f for f in dxf_files if not any(p.search(f) for p in patterns)]
        logging.debug(f"Fichiers .dxf affichés (non ignorés) dans {subfolder_path} : {filtered_dxf_files}")
        
        for dxf_file in filtered_dxf_files:
            # Crée une frame pour chaque fichier .dxf
            dxf_frame = ctk.CTkFrame(parent_frame)
            dxf_frame.pack(fill="x", padx=10, pady=2)
            
            # Affiche le nom du fichier .dxf
            dxf_label = ctk.CTkLabel(dxf_frame, text=dxf_file)
            dxf_label.pack(side="left", padx=10, pady=5)

            # Champ d'entrée pour la quantité
            quantity_entry = ctk.CTkEntry(dxf_frame, placeholder_text="Quantité", width=80)
            quantity_entry.pack(side="left", padx=5)
            
            # Stocker la quantité lorsque l'entrée change
            quantity_entry.bind("<FocusOut>", lambda event, key=dxf_file: self.store_quantity(key, event.widget.get()))

            # Bouton pour ignorer le fichier .dxf
            ignore_button = ctk.CTkButton(
                dxf_frame, 
                text="Ignorer", 
                command=lambda lbl=dxf_frame: self.ignore_dxf_file(lbl),
                fg_color="red"
            )
            ignore_button.pack(side="right", padx=10, pady=5)

    def store_quantity(self, key, value):
        """Stocke la quantité saisie pour chaque fichier .dxf."""
        try:
            self.quantities[key] = int(value) if value.isdigit() else 0
            logging.debug(f"Quantité pour {key} mise à jour : {self.quantities[key]}")
        except ValueError:
            logging.error(f"Erreur lors de la saisie de la quantité pour {key}")

    def ignore_dxf_file(self, dxf_frame):
        """Supprime uniquement le label du fichier .dxf sans affecter le fichier physique."""
        try:
            # Supprime la frame de l'interface
            dxf_frame.destroy()
            logging.debug("Fichier .dxf ignoré et retiré de l'affichage.")
        except Exception as e:
            logging.error(f"Erreur lors de l'ignorance du fichier .dxf : {e}")

    def delete_subfolder_frame(self, subfolder_frame):
        """Supprime uniquement la frame du sous-dossier sans affecter le dossier physique."""
        try:
            # Supprime la frame de l'interface
            subfolder_frame.destroy()
            logging.debug("Frame du sous-dossier supprimée.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la frame du sous-dossier : {e}")

# Lancement de l'application
if __name__ == "__main__":
    logging.debug("Lancement de l'application.")
    app = FolderSelectorApp()
    app.mainloop()
    logging.debug("Application fermée.")
