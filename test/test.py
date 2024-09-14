import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import logging
import re
import webbrowser
import win32com.client  # Bibliothèque pour contrôler Outlook via COM
import Generate_DXF

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
        self.title("ProDXF Organizer")
        self.geometry("1000x600")

        # Configuration de la grille principale
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame latérale pour les boutons d'onglets
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Boutons pour simuler des onglets dans la sidebar avec largeur augmentée
        self.button_onglet1 = ctk.CTkButton(self.sidebar_frame, text="Onglet 1", command=self.show_frame1, corner_radius=10, fg_color="black", text_color="white", border_color="white", border_width=2, width=220, height=40)
        self.button_onglet1.pack(padx=10, pady=10)

        self.button_onglet2 = ctk.CTkButton(self.sidebar_frame, text="Onglet 2", command=self.show_frame2, corner_radius=10, fg_color="#1a1a1a", text_color="white", width=220, height=40)
        self.button_onglet2.pack(padx=10, pady=10)

        self.button_onglet3 = ctk.CTkButton(self.sidebar_frame, text="Onglet 3", command=self.show_frame3, corner_radius=10, fg_color="#1a1a1a", text_color="white", width=220, height=40)
        self.button_onglet3.pack(padx=10, pady=10)
        
        # Frames pour chaque "onglet"
        self.frame1 = ctk.CTkFrame(self, fg_color="black", corner_radius=10)
        self.frame2 = ctk.CTkFrame(self, fg_color="black", corner_radius=10)
        self.frame3 = ctk.CTkFrame(self, fg_color="black", corner_radius=10)
        
        self.frame1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame3.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Affichage initial du premier onglet
        self.show_frame1()

        # Contenu de la première frame (Onglet 1)
        self.select_button = ctk.CTkButton(self.frame1, text="Sélectionnez un dossier", command=self.select_folder, corner_radius=10)
        self.select_button.pack(pady=20)

        self.folder_label = ctk.CTkLabel(self.frame1, text="")
        self.folder_label.pack(pady=10)

        self.subfolders_scroll_frame = ctk.CTkScrollableFrame(self.frame1, corner_radius=10)
        
        self.email_client_button = ctk.CTkButton(
            self.frame1,
            text="Gmail",
            fg_color="red",
            command=self.toggle_email_client,
            corner_radius=10
        )
        self.email_client_button.pack(anchor="ne", padx=10, pady=10)

        self.validate_button = ctk.CTkButton(self.frame1, text="Valider", command=self.on_validate, corner_radius=10)
        
        # Contenu de la deuxième frame (Onglet 2)
        self.select_button2 = ctk.CTkButton(self.frame2, text="Sélectionnez un dossier", command=self.select_folder, corner_radius=10)
        self.select_button2.pack(pady=20)

        self.folder_label2 = ctk.CTkLabel(self.frame2, text="")
        self.folder_label2.pack(pady=10)

        # Ajout du nouveau bouton dans l'onglet 2 avec les dimensions spécifiées et le style
        self.big_button = ctk.CTkButton(
            self.frame2, 
            text="Générer DXF", 
            corner_radius=20, 
            width=270, 
            height=150, 
            fg_color="black", 
            border_color="white", 
            border_width=2,
            font=("Helvetica", 16),  # Utilisation du paramètre correct pour la police
            command=self.generate_dxf
        )
        self.big_button.pack(pady=20)

        # Variables pour les informations extraites du chemin
        self.subfolder_frames = {}
        self.quantities = {}
        self.quantity_entries = []
        self.client_name = ""
        self.project_number = ""
        self.project_name = ""
        self.email_client = "Gmail"  # Par défaut, Gmail est sélectionné

    def show_frame1(self):
        """Affiche la première frame et cache les autres."""
        self.frame1.tkraise()
        self.button_onglet1.configure(fg_color="black", text_color="white", border_color="white", border_width=2)
        self.button_onglet2.configure(fg_color="#1a1a1a", text_color="white", border_width=0)
        self.button_onglet3.configure(fg_color="#1a1a1a", text_color="white", border_width=0)

    def show_frame2(self):
        """Affiche la seconde frame et cache les autres."""
        self.frame2.tkraise()
        self.button_onglet2.configure(fg_color="black", text_color="white", border_color="white", border_width=2)
        self.button_onglet1.configure(fg_color="#1a1a1a", text_color="white", border_width=0)
        self.button_onglet3.configure(fg_color="#1a1a1a", text_color="white", border_width=0)

    def show_frame3(self):
        """Affiche la troisième frame et cache les autres."""
        self.frame3.tkraise()
        self.button_onglet3.configure(fg_color="black", text_color="white", border_color="white", border_width=2)
        self.button_onglet1.configure(fg_color="#1a1a1a", text_color="white", border_width=0)
        self.button_onglet2.configure(fg_color="#1a1a1a", text_color="white", border_width=0)

    def toggle_email_client(self):
        """Change le client de messagerie entre Gmail et Outlook."""
        if self.email_client == "Gmail":
            self.email_client = "Outlook"
            self.email_client_button.configure(text="Outlook", fg_color="blue")
        else:
            self.email_client = "Gmail"
            self.email_client_button.configure(text="Gmail", fg_color="red")

    def select_folder(self):
        # Ouvre une fenêtre de dialogue pour sélectionner un dossier
        folder_path = filedialog.askdirectory()
        if folder_path:
            logging.debug(f"Dossier sélectionné : {folder_path}")
            self.folder_label.configure(text=folder_path)
            self.folder_label2.configure(text=folder_path)  # Mise à jour du label dans le deuxième onglet aussi
            self.extract_project_info(folder_path)  # Extraction des informations du projet
            self.subfolders_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            self.display_subfolders(folder_path)
        else:
            logging.debug("Aucun dossier sélectionné.")
    
    def extract_project_info(self, folder_path):
        """Extrait le nom du client, le numéro d'affaire et le nom du projet depuis le chemin du dossier."""
        path_parts = folder_path.split(os.sep)
        try:
            # Rechercher les informations dans le chemin
            chantier_index = path_parts.index('Chantier')
            self.client_name = path_parts[chantier_index + 1]
            project_info = path_parts[chantier_index + 2]
            
            # Extraction du numéro d'affaire (5 chiffres) et du nom du projet
            self.project_number = re.search(r'\d{5}', project_info).group()
            self.project_name = project_info.split(self.project_number)[1].strip()

            logging.debug(f"Client : {self.client_name}, Numéro d'affaire : {self.project_number}, Projet : {self.project_name}")
        except (ValueError, IndexError, AttributeError) as e:
            logging.error(f"Erreur lors de l'extraction des informations du projet : {e}")
            self.client_name = ""
            self.project_number = ""
            self.project_name = ""

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
            
            subfolder_frame = ctk.CTkFrame(self.subfolders_scroll_frame, fg_color="gray20", corner_radius=10)
            subfolder_frame.pack(fill="x", padx=5, pady=5)
            
            inner_frame = ctk.CTkFrame(subfolder_frame, fg_color="gray30", corner_radius=10)
            inner_frame.pack(fill="both", padx=2, pady=2, expand=True)
            
            subfolder_label = ctk.CTkLabel(inner_frame, text=subfolder)
            subfolder_label.pack(padx=10, pady=5)
            
            delete_folder_frame_button = ctk.CTkButton(
                inner_frame, 
                text="Supprimer ce Dossier", 
                command=lambda sf_frame=subfolder_frame: self.delete_subfolder_frame(sf_frame),
                fg_color="red",
                corner_radius=10
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
            dxf_frame = ctk.CTkFrame(parent_frame, corner_radius=10)
            dxf_frame.pack(fill="x", padx=10, pady=2)
            
            dxf_label = ctk.CTkLabel(dxf_frame, text=dxf_file)
            dxf_label.pack(side="left", padx=10, pady=5)

            quantity_entry = ctk.CTkEntry(dxf_frame, placeholder_text="Quantité", width=80, corner_radius=10)
            quantity_entry.pack(side="left", padx=5)
            
            # Stocker chaque entry avec le nom du fichier et du dossier
            self.quantity_entries.append(((subfolder_name, dxf_file, subfolder_path), quantity_entry))

            ignore_button = ctk.CTkButton(
                dxf_frame, 
                text="Ignorer", 
                command=lambda lbl=dxf_frame, key=(subfolder_name, dxf_file, subfolder_path): self.ignore_dxf_file(lbl, key),
                fg_color="red",
                corner_radius=10
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

    def format_email_content(self):
        """Formate le contenu de l'email avec les fichiers et quantités."""
        email_content = ""
        grouped_files = {}

        # Regroupement des fichiers par dossier
        for (folder_name, filename, folder_path), quantity in self.quantities.items():
            if folder_name not in grouped_files:
                grouped_files[folder_name] = []
            grouped_files[folder_name].append((filename, quantity, folder_path))

        # Création du corps de l'email
        for folder, files in grouped_files.items():
            email_content += f"{folder}:\n"
            for filename, quantity, _ in files:
                email_content += f"    • {filename.split('.')[0]:<5}   qté: {quantity}\n"
            email_content += f"{files[0][2]}\n\n"  # Ajoute le chemin du dossier

        email_content += "\nCordialement."
        return email_content

    def open_gmail(self, subject, body):
        """Ouvre un brouillon dans Gmail avec le sujet et le corps pré-remplis."""
        body = body.replace('\n', '%0A')  # Encodage des sauts de ligne pour l'URL
        subject = subject.replace(' ', '%20')  # Encodage des espaces pour l'URL
        url = f"https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=&su={subject}&body={body}"
        webbrowser.open(url)

    def open_outlook(self, subject, body):
        """Ouvre un brouillon dans l'application de bureau Outlook avec le sujet et le corps pré-remplis."""
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)  # 0 = olMailItem
            mail.Subject = subject
            mail.Body = body
            mail.Display()  # Affiche le brouillon sans l'envoyer
        except Exception as e:
            logging.error(f"Erreur lors de l'ouverture d'Outlook : {e}")
            messagebox.showerror("Erreur", "Impossible d'ouvrir Outlook pour créer un brouillon.")

    def on_validate(self):
        """Vérifie que toutes les quantités ont été remplies correctement avant de valider et préparer l'email."""
        for (folder_name, filename, folder_path), entry in self.quantity_entries:
            value = entry.get()
            if value.isdigit() and int(value) > 0:
                self.quantities[(folder_name, filename, folder_path)] = int(value)
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

        # Préparer l'email à relire avant envoi selon le client sélectionné
        email_subject = f"{self.project_number} - {self.project_name} - {self.client_name}"
        email_body = self.format_email_content()
        
        if self.email_client == "Gmail":
            self.open_gmail(email_subject, email_body)
        else:
            self.open_outlook(email_subject, email_body)

    def generate_dxf(self):
        """Fonction pour générer des fichiers DXF."""
        # Implémenter la logique pour générer des fichiers DXF ici
        logging.debug("Génération des fichiers DXF...")

# Lancement de l'application
if __name__ == "__main__":
    logging.debug("Lancement de l'application.")
    app = FolderSelectorApp()
    app.mainloop()
    logging.debug("Application fermée.")
