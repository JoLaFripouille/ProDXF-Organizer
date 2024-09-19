import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import logging
import json
from Generate_DXF import process_dwg

CONFIG_PATH = "JSON/FormatBlocks.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    else:
        return {"prefix": "TL", "suffix": "_"}
# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration des constantes
config = load_config()
DEFAULT_HEIGHT = 38
DEFAULT_CORNER_RADIUS = DEFAULT_HEIGHT // 2

class Tab2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="black", corner_radius=10)
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Variables pour stocker le chemin du fichier DWG sélectionné
        self.dwg_file = ""

        # Bouton pour sélectionner le fichier DWG
        self.select_dwg_button = ctk.CTkButton(
            self,
            text="Sélectionnez un fichier DWG",
            command=self.select_dwg_file,
            font=("Helvetica", 20),
            corner_radius=DEFAULT_CORNER_RADIUS,
            height=DEFAULT_HEIGHT * 1.5
        )
        self.select_dwg_button.pack(pady=40)

        # Label pour afficher le chemin du fichier DWG sélectionné
        self.dwg_file_label = ctk.CTkLabel(self, text="")
        self.dwg_file_label.pack(pady=10)

        # Bouton pour générer les fichiers .dxf
        self.big_button = ctk.CTkButton(
            self,
            text="Générer les fichiers .dxf",
            command=self.generate_dxf,
            corner_radius=DEFAULT_CORNER_RADIUS,
            width=270,
            height=110,
            fg_color="black",
            border_color="white",
            border_width=2,
            font=("Helvetica", 22)
        )
        self.big_button.pack_forget()  # Masquer le bouton jusqu'à ce qu'un fichier DWG soit sélectionné

        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(self, height=20)
        self.progress_bar.pack_forget()  # Masquer la barre de progression initialement

    def select_dwg_file(self):
        """Ouvre une fenêtre de dialogue pour sélectionner un fichier DWG."""
        file_path = filedialog.askopenfilename(filetypes=[("DWG files", "*.dwg")])
        if file_path:
            logging.debug(f"Fichier DWG sélectionné : {file_path}")
            self.dwg_file = file_path
            self.dwg_file_label.configure(text=file_path)
            self.big_button.pack(pady=20)  # Affiche le bouton quand un fichier est sélectionné
        else:
            logging.debug("Aucun fichier DWG sélectionné.")
            self.big_button.pack_forget()  # Cache le bouton si aucun fichier n'est sélectionné

    def generate_dxf(self):
        """Génère des fichiers DXF à partir du fichier DWG sélectionné."""
        if self.dwg_file:
            logging.debug(f"Génération des fichiers DXF à partir de {self.dwg_file}...")
            self.big_button.pack_forget()  # Cache le bouton pendant le processus
            self.progress_bar.pack(pady=20)  # Affiche la barre de progression
            self.progress_bar.set(0)  # Réinitialise la barre de progression

            try:
                # Appel à la fonction de génération de fichiers DXF
                prefix = config["prefix"]  # Exemple de préfixe à utiliser
                suffix = config["suffix"]  # Exemple de suffixe à utiliser
                process_dwg(self.dwg_file, prefix, suffix)

                # Mise à jour de la barre de progression
                self.progress_bar.set(1.0)  # Met à jour à 100% une fois terminé
                messagebox.showinfo("Succès", "Les fichiers DXF ont été générés avec succès.")
            except Exception as e:
                logging.error(f"Erreur lors de la génération des fichiers DXF : {e}")
                messagebox.showerror("Erreur", f"Erreur lors de la génération des fichiers DXF : {e}")
            finally:
                self.progress_bar.pack_forget()  # Cache la barre de progression après le processus
                self.big_button.pack(pady=20)  # Réaffiche le bouton après le processus
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier DWG avant de générer les fichiers DXF.")
