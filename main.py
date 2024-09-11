import customtkinter as ctk
from tkinter import filedialog, messagebox
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
        
        # Dictionnaire pour garder une trace des sous-dossiers et de leurs frames
        self.subfolder_frames = {}
        
        # Dictionnaire pour stocker les quantités saisies par l'utilisateur
        self.quantities = {}

        # Liste des entries de quantités pour validation
        self.quantity_entries = []

        # Bouton valider (caché initialement)
        self.validate_button = ctk.CTkButton(self, text="Valider", command=self.on_validate)
        
    def select_folder(self):
        # Ouvre une fenêtre de dialogue pour sélectionner un dossier
        folder_path = filedialog.askdirectory()
        if folder_path:
            logging.debug(f"Dossier sélectionné : {folder_path}")
            self.folder_label.configure(text=folder_path)
            self.subfolders_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            self.display_subfolders(folder_path)
        else:
            logging.debug("Aucun dossier sélectionné.")
    
    def display_subfolders(self, folder_path):
        for widget in self.subfolders_scroll_frame.winfo_children():
            widget.destroy()
        
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        logging.debug(f"Nombre de sous-dossiers trouvés : {len(subfolders)}")
        
        self.subfolder_frames = {}
        self.quantity_entries = []
        has_dxf_files = False
        
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)
            logging.debug(f"Affichage du sous-dossier : {subfolder}")
            
            subfolder_frame = ctk.CTkFrame(self.subfolders_scroll_frame, fg_color="gray20")
            subfolder_frame.pack(fill="x", padx=5, pady=5)
            
            inner_frame = ctk.CTkFrame(subfolder_frame, fg_color="gray30", corner_radius=5)
            inner_frame.pack(fill="both", padx=2, pady=2, expand=True)
            
            subfolder_label = ctk.CTkLabel(inner_frame, text=subfolder)
            subfolder_label.pack(padx=10, pady=5)
            
            delete_folder_frame_button = ctk.CTkButton(
                inner_frame, 
                text="Supprimer ce Dossier", 
                command=lambda sf_frame=subfolder_frame: self.delete_subfolder_frame(sf_frame),
                fg_color="red"
            )
            delete_folder_frame_button.pack(padx=10, pady=5)
            
            self.subfolder_frames[subfolder] = subfolder_frame
            
            if self.display_dxf_files(subfolder_path, inner_frame, subfolder):
                has_dxf_files = True
        
        if has_dxf_files:
            self.validate_button.pack(side="bottom", fill="x", padx=10, pady=10)

    def display_dxf_files(self, subfolder_path, parent_frame, subfolder_name):
        dxf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.dxf')]
        logging.debug(f"Fichiers .dxf trouvés dans {subfolder_path} : {dxf_files}")
        
        filtered_dxf_files = [f for f in dxf_files if not any(p.search(f) for p in patterns)]
        logging.debug(f"Fichiers .dxf affichés (non ignorés) dans {subfolder_path} : {filtered_dxf_files}")
        
        has_files = bool(filtered_dxf_files)

        for dxf_file in filtered_dxf_files:
            dxf_frame = ctk.CTkFrame(parent_frame)
            dxf_frame.pack(fill="x", padx=10, pady=2)
            
            dxf_label = ctk.CTkLabel(dxf_frame, text=dxf_file)
            dxf_label.pack(side="left", padx=10, pady=5)

            quantity_entry = ctk.CTkEntry(dxf_frame, placeholder_text="Quantité", width=80)
            quantity_entry.pack(side="left", padx=5)
            
            # Stocker chaque entry avec le nom du fichier et du dossier
            self.quantity_entries.append(((subfolder_name, dxf_file, subfolder_path), quantity_entry))

            ignore_button = ctk.CTkButton(
                dxf_frame, 
                text="Ignorer", 
                command=lambda lbl=dxf_frame, key=(subfolder_name, dxf_file, subfolder_path): self.ignore_dxf_file(lbl, key),
                fg_color="red"
            )
            ignore_button.pack(side="right", padx=10, pady=5)
        
        return has_files

    def store_quantity(self, key, value):
        """Stocke la quantité saisie pour chaque fichier .dxf."""
        try:
            self.quantities[key] = int(value) if value.isdigit() else 0
            logging.debug(f"Quantité pour {key} mise à jour : {self.quantities[key]}")
        except ValueError:
            logging.error(f"Erreur lors de la saisie de la quantité pour {key}")

    def ignore_dxf_file(self, dxf_frame, key):
        """Ignore un fichier .dxf en le retirant de l'affichage et des validations."""
        try:
            # Supprime la frame de l'interface
            dxf_frame.destroy()
            # Supprime l'entrée et la quantité associée au fichier ignoré
            self.quantity_entries = [(k, e) for k, e in self.quantity_entries if k != key]
            if key in self.quantities:
                del self.quantities[key]
            logging.debug(f"Fichier {key} ignoré et retiré de l'affichage.")
        except Exception as e:
            logging.error(f"Erreur lors de l'ignorance du fichier .dxf : {e}")

    def delete_subfolder_frame(self, subfolder_frame):
        """Supprime uniquement la frame du sous-dossier sans affecter le dossier physique."""
        try:
            subfolder_frame.destroy()
            logging.debug("Frame du sous-dossier supprimée.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la frame du sous-dossier : {e}")

    def on_validate(self):
        """Vérifie que toutes les quantités ont été remplies correctement avant de valider et renomme les fichiers."""
        for (folder_name, filename, folder_path), entry in self.quantity_entries:
            # Lire explicitement les valeurs de chaque entrée
            value = entry.get()
            if value.isdigit() and int(value) > 0:
                self.quantities[(folder_name, filename, folder_path)] = int(value)  # Clé à trois éléments
            else:
                messagebox.showerror("Erreur", f"Veuillez entrer un nombre valide pour {filename} dans {folder_name}.")
                return
        
        # Renommer les fichiers avec le nouveau format
        for (folder_name, filename, folder_path), quantity in self.quantities.items():
            old_file_path = os.path.join(folder_path, filename)
            new_filename = f'{os.path.splitext(filename)[0]}_{folder_name}_qte-{quantity}.dxf'
            new_file_path = os.path.join(folder_path, new_filename)
            try:
                os.rename(old_file_path, new_file_path)
                print(f'Fichier renommé : {old_file_path} -> {new_file_path}')
            except Exception as e:
                logging.error(f"Erreur lors du renommage du fichier {filename} : {e}")
                messagebox.showerror("Erreur", f"Impossible de renommer le fichier {filename}.")

# Lancement de l'application
if __name__ == "__main__":
    logging.debug("Lancement de l'application.")
    app = FolderSelectorApp()
    app.mainloop()
    logging.debug("Application fermée.")
