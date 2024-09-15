import customtkinter as ctk
from tkinter import filedialog, messagebox, PhotoImage 
import os
import logging
import re
import webbrowser
import win32com.client
import json
import Generate_DXF
import requests

# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Variables de configuration pour les composants de l'interface
DEFAULT_HEIGHT = 38
DEFAULT_CORNER_RADIUS = DEFAULT_HEIGHT // 2

# Chemins des fichiers de configuration
CONFIG_PATH = "JSON/FormatBlocks.json"
API_KEY_PATH = "API_KEY.env"
EMAIL_PATH = "JSON/AddEmail.json"
CONFIG_ENVOI_PATH = "JSON/ConfigEnvoi.json"
ACAD_TOOLS_PATH = "JSON/acadTools.json"

# Définition des patterns pour ignorer les fichiers .dxf
patterns = [
    re.compile(r".+_.+_qte-\d+\.dxf", re.IGNORECASE),
    re.compile(r".+_.+_qte-\d+\.dxf", re.IGNORECASE)
]

# Fonction pour charger la configuration à partir du JSON
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    else:
        return {"prefix": "DEV", "suffix": "TL"}

# Fonction pour enregistrer la configuration dans le JSON
def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)

# Fonction pour charger la clé API depuis le fichier
def load_api_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, "r") as file:
            line = file.read().strip()
            if line.startswith("API_KEY="):
                return line.split("=", 1)[1]
    return ""

# Fonction pour enregistrer la clé API dans le fichier
def save_api_key(api_key):
    with open(API_KEY_PATH, "w") as file:
        file.write(f"API_KEY={api_key}")

# Fonction pour charger l'email depuis le fichier JSON
def load_email():
    if os.path.exists(EMAIL_PATH):
        with open(EMAIL_PATH, "r") as file:
            return json.load(file).get("email", "")
    return ""

# Fonction pour enregistrer l'email dans le fichier JSON
def save_email(email):
    with open(EMAIL_PATH, "w") as file:
        json.dump({"email": email}, file, indent=4)

# Fonction pour charger le mode d'envoi par défaut depuis le fichier JSON
def load_default_client():
    if os.path.exists(CONFIG_ENVOI_PATH):
        with open(CONFIG_ENVOI_PATH, "r") as file:
            return json.load(file).get("default_client", "Gmail")
    return "Gmail"

# Fonction pour enregistrer le mode d'envoi par défaut dans le fichier JSON
def save_default_client(client):
    with open(CONFIG_ENVOI_PATH, "w") as file:
        json.dump({"default_client": client}, file, indent=4)

# Fonction pour charger les outils AutoCAD depuis le fichier JSON
def load_acad_tools():
    if os.path.exists(ACAD_TOOLS_PATH):
        with open(ACAD_TOOLS_PATH, "r") as file:
            return json.load(file)
    else:
        return []

# Chargement de la configuration et des informations nécessaires au démarrage
config = load_config()
api_key = load_api_key()
email = load_email()
default_client = load_default_client()
acad_tools = load_acad_tools()

# Initialisation de l'application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class FolderSelectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("ProDXF Organizer")
        self.geometry("1000x680")

        # Load images for Gmail and Outlook
        self.gmail_image = PhotoImage(file="asset/img/gmail.png")
        self.outlook_image = PhotoImage(file="asset/img/outlook.png")

        # Configuration de la grille principale
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame latérale pour les boutons d'onglets
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=DEFAULT_CORNER_RADIUS)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Boutons pour simuler des onglets dans la sidebar
        self.button_onglet1 = ctk.CTkButton(self.sidebar_frame, text="Envoyer des fichiers DXF", command=self.show_frame1, font=("Helvetica", 20), corner_radius=DEFAULT_CORNER_RADIUS, fg_color="black", text_color="white", border_color="white", border_width=2, width=260, height=60)
        self.button_onglet1.pack(padx=10, pady=10)

        self.button_onglet2 = ctk.CTkButton(self.sidebar_frame, text="Generer des fichiers DXF", command=self.show_frame2, font=("Helvetica", 20), corner_radius=DEFAULT_CORNER_RADIUS, fg_color="#1a1a1a", text_color="white", width=260, height=60)
        self.button_onglet2.pack(padx=10, pady=10)

        self.button_onglet3 = ctk.CTkButton(self.sidebar_frame, text="Configuration", command=self.show_frame3, font=("Helvetica", 20), corner_radius=DEFAULT_CORNER_RADIUS, fg_color="#1a1a1a", text_color="white", width=260, height=60)
        self.button_onglet3.pack(padx=10, pady=10)

        # Frames pour chaque "onglet"
        self.frame1 = ctk.CTkFrame(self, fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)
        self.frame2 = ctk.CTkFrame(self, fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)
        self.frame3 = ctk.CTkFrame(self, fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)

        self.frame1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame3.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Ajout d'une scrollable frame dans la frame3
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame3, fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Affichage initial du premier onglet
        self.show_frame1()

        # Contenu de la première frame (Onglet 1)
        self.select_button = ctk.CTkButton(self.frame1, text="Sélectionnez un dossier", command=self.select_folder, font=("Helvetica", 20), corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT*1.5)
        self.select_button.pack(pady=20)

        self.folder_label = ctk.CTkLabel(self.frame1, text="")
        self.folder_label.pack(pady=10)

        self.subfolders_scroll_frame = ctk.CTkScrollableFrame(self.frame1, corner_radius=DEFAULT_CORNER_RADIUS)

        # Initialize the button with the default client image
        self.email_client = default_client
        self.email_client_button = ctk.CTkButton(
            self.frame1,
            image=self.gmail_image if self.email_client == "Gmail" else self.outlook_image,
            command=self.toggle_email_client,
            corner_radius=2,
            hover=False,
            height=DEFAULT_HEIGHT,
            fg_color='black',
            text=""  # Hide text to only show the image
        )
        self.email_client_button.pack(anchor="ne", padx=10, pady=10)
        
        self.validate_button = ctk.CTkButton(self.frame1, text="Valider", command=self.on_validate, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)

        # Contenu de la deuxième frame (Onglet 2)
        self.select_dwg_button = ctk.CTkButton(self.frame2, text="Sélectionnez un fichier DWG", command=self.select_dwg_file, font=("Helvetica", 20), corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT*1.5)
        self.select_dwg_button.pack(pady=20)

        self.dwg_file_label = ctk.CTkLabel(self.frame2, text="")
        self.dwg_file_label.pack(pady=10)

        self.big_button = ctk.CTkButton(
            self.frame2,
            text="Générer les fichiers .dxf",
            corner_radius=20,
            width=270,
            height=110,
            fg_color="black",
            border_color="white",
            border_width=2,
            font=("Helvetica", 22),
            command=self.generate_dxf
        )
        self.big_button.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.frame2, width=400)
        self.progress_bar.set(0)

        # Contenu de la troisième frame (Configuration) déplacé vers scrollable_frame
        self.config_prefix_suffix_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_prefix_suffix_frame.pack(fill="x", padx=10, pady=10)

        self.entry_prefix = ctk.CTkEntry(self.config_prefix_suffix_frame, placeholder_text="Préfixe", width=200, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT, justify="center")
        self.entry_prefix.insert(0, config["prefix"])
        self.entry_prefix.pack(side="left", pady=10, padx=5)

        self.save_prefix_button = ctk.CTkButton(self.config_prefix_suffix_frame, text="Enregistrer", command=self.save_prefix, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_prefix_button.pack(side="left", pady=10, padx=5)

        self.entry_suffix = ctk.CTkEntry(self.config_prefix_suffix_frame, placeholder_text="Suffixe", width=200, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT, justify="center")
        self.entry_suffix.insert(0, config["suffix"])
        self.entry_suffix.pack(side="left", pady=10, padx=5)

        self.save_suffix_button = ctk.CTkButton(self.config_prefix_suffix_frame, text="Enregistrer", command=self.save_suffix, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_suffix_button.pack(side="left", pady=10, padx=5)

        # Frame pour la gestion de la clé API
        self.config_api_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_api_frame.pack(fill="x", padx=10, pady=10)

        self.entry_api_key = ctk.CTkEntry(self.config_api_frame, placeholder_text="Clé API", width=400, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.entry_api_key.insert(0, api_key)
        self.entry_api_key.pack(pady=10, padx=5)

        self.save_api_key_button = ctk.CTkButton(self.config_api_frame, text="Enregistrer Clé API", command=self.save_api_key, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_api_key_button.pack(pady=10, padx=5)

        # Bouton pour visiter le site CloudConvert
        self.visit_api_button = ctk.CTkButton(self.config_api_frame, text="Visiter API CloudConvert", command=self.visit_api_site, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.visit_api_button.pack(pady=10, padx=5)

        # Frame pour la configuration de l'adresse email du destinataire
        self.config_email_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_email_frame.pack(fill="x", padx=10, pady=10)

        self.entry_email = ctk.CTkEntry(self.config_email_frame, placeholder_text="Email destinataire", width=400, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT, justify="center")
        self.entry_email.insert(0, email)
        self.entry_email.pack(pady=10, padx=5)

        self.save_email_button = ctk.CTkButton(self.config_email_frame, text="Enregistrer Email", command=self.save_email, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_email_button.pack(pady=10, padx=5)

        # Frame pour la configuration du mode d'envoi par défaut (Gmail ou Outlook)
        self.config_client_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_client_frame.pack(fill="x", padx=10, pady=10)

        self.entry_client = ctk.CTkEntry(self.config_client_frame, placeholder_text="Client (Gmail/Outlook)", width=400, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT, justify="center")
        self.entry_client.insert(0, default_client)
        self.entry_client.pack(pady=10, padx=5)

        self.save_client_button = ctk.CTkButton(self.config_client_frame, text="Enregistrer Client", command=self.save_default_client, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_client_button.pack(pady=10, padx=5)

        # Frame scrollable pour les outils AutoCAD
        self.tools_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.tools_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame for Autolisp project link
        self.autolisp_link_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.autolisp_link_frame.pack(fill="x", padx=10, pady=10)

        # Label for the Autolisp project link
        self.autolisp_label = ctk.CTkLabel(self.autolisp_link_frame, text="Lien du projet Autolisp ICI", font=("Helvetica", 16))
        self.autolisp_label.pack(side="left", padx=10, pady=10)

        # Load the GitHub image
        self.github_image = PhotoImage(file="asset/img/github.png")

        # Button to open the GitHub link
        self.github_button = ctk.CTkButton(
            self.autolisp_link_frame,
            image=self.github_image,
            command=lambda: webbrowser.open("https://github.com/JoLaFripouille/AutoLisp"),
            corner_radius=25,
            width=200,
            height=50,
            border_width=2,
            fg_color="#151b23",
            text="",  # Hide text to only show the image
            hover=True  # Disable hover animation if needed
        )
        self.github_button.pack(side="left", padx=10, pady=10)

        # Chargement dynamique des outils AutoCAD depuis le JSON
        self.load_acad_tools_ui()

        # Variables pour les informations extraites du chemin
        self.subfolder_frames = {}
        self.quantities = {}
        self.quantity_entries = []
        self.client_name = ""
        self.project_number = ""
        self.project_name = ""
        self.email_client = default_client
        self.dwg_file = ""

    def load_acad_tools_ui(self):
        """Charge dynamiquement les outils AutoCAD depuis le JSON dans l'interface utilisateur."""
        for tool in acad_tools:
            tool_frame = ctk.CTkFrame(self.tools_frame, fg_color="gray25", corner_radius=DEFAULT_CORNER_RADIUS)
            tool_frame.pack(fill="x", padx=10, pady=5)

            tool_name_label = ctk.CTkLabel(tool_frame, text=tool["name"], font=("Helvetica", 16))
            tool_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            tool_description_label = ctk.CTkLabel(tool_frame, text=tool["description"])
            tool_description_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            # Configure the tool_frame's grid to have an empty column that will push the button to the right
            tool_frame.grid_columnconfigure(1, weight=1)

            download_button = ctk.CTkButton(
                tool_frame, 
                text="Télécharger", 
                command=lambda url=tool["url"], name=tool["name"]: self.download_lisp(url, name), 
                corner_radius=DEFAULT_CORNER_RADIUS, 
                height=DEFAULT_HEIGHT
            )
            download_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")




    def download_lisp(self, url, name):
        """Télécharge le script Lisp depuis l'URL spécifiée."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifie si la requête a réussi
            file_path = filedialog.asksaveasfilename(defaultextension=".lsp", initialfile=name, filetypes=[("Lisp Files", "*.lsp")])
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                messagebox.showinfo("Téléchargement", f"Script {name} téléchargé avec succès dans {file_path}")
        except Exception as e:
            logging.error(f"Erreur lors du téléchargement du script {name} : {e}")
            messagebox.showerror("Erreur", f"Échec du téléchargement du script {name}.")

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
        """Affiche la troisième frame (Configuration) et cache les autres."""
        self.frame3.tkraise()
        self.button_onglet3.configure(fg_color="black", text_color="white", border_color="white", border_width=2)
        self.button_onglet1.configure(fg_color="#1a1a1a", text_color="white", border_width=0)
        self.button_onglet2.configure(fg_color="#1a1a1a", text_color="white", border_width=0)

    def select_folder(self):
        # Ouvre une fenêtre de dialogue pour sélectionner un dossier
        folder_path = filedialog.askdirectory()
        if folder_path:
            logging.debug(f"Dossier sélectionné : {folder_path}")
            self.folder_label.configure(text=folder_path)
            self.extract_project_info(folder_path)
            self.subfolders_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            self.display_subfolders(folder_path)
        else:
            logging.debug("Aucun dossier sélectionné.")

    def select_dwg_file(self):
        # Ouvre une fenêtre de dialogue pour sélectionner un fichier DWG
        file_path = filedialog.askopenfilename(filetypes=[("DWG files", "*.dwg")])
        if file_path:
            logging.debug(f"Fichier DWG sélectionné : {file_path}")
            self.dwg_file = file_path
            self.dwg_file_label.configure(text=file_path)
            self.big_button.pack_forget()  # Cache le bouton après avoir cliqué dessus
            self.progress_bar.pack(pady=20)  # Affiche la barre de progression pendant le traitement
            self.generate_dxf()  # Lancer le traitement immédiatement après la sélection
        else:
            logging.debug("Aucun fichier DWG sélectionné.")
            self.big_button.pack_forget()  # Cache le bouton si aucun fichier n'est sélectionné

    def generate_dxf(self):
        """Fonction pour générer des fichiers DXF."""
        if self.dwg_file:
            try:
                logging.debug(f"Génération des fichiers DXF à partir de {self.dwg_file}...")
                prefix = config.get("prefix", "TL")
                suffix = config.get("suffix", "DEV")
                self.progress_bar.set(0.5)  # Mettre à jour la progression à mi-chemin (exemple)
                Generate_DXF.process_dwg(self.dwg_file, prefix, suffix)  # Traitement du fichier DWG
                self.progress_bar.set(1)  # Compléter la barre de progression
                messagebox.showinfo("Succès", "Génération des fichiers DXF terminée avec succès.")
            except Exception as e:
                logging.error(f"Erreur lors de la génération des fichiers DXF : {e}")
                messagebox.showerror("Erreur", "Échec de la génération des fichiers DXF.")
            finally:
                self.progress_bar.pack_forget()  # Cache la barre de progression après le traitement
                self.big_button.pack(pady=20)  # Réaffiche le bouton
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier DWG avant de générer les fichiers DXF.")

    def extract_project_info(self, folder_path):
        """Extrait le nom du client, le numéro d'affaire et le nom du projet depuis le chemin du dossier."""
        path_parts = folder_path.split(os.sep)
        try:
            chantier_index = path_parts.index('Chantier')
            self.client_name = path_parts[chantier_index + 1]
            project_info = path_parts[chantier_index + 2]
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

    # Function to open Gmail with the recipient email pre-filled
    def open_gmail(self, subject, body):
        """Ouvre un brouillon dans Gmail avec le sujet, le corps et le destinataire pré-remplis."""
        recipient_email = load_email()  # Load the recipient email from the JSON file
        body = body.replace('\n', '%0A')  # Encode line breaks for the URL
        subject = subject.replace(' ', '%20')  # Encode spaces for the URL
        url = f"https://mail.google.com/mail/?view=cm&fs=1&tf=1&to={recipient_email}&su={subject}&body={body}"
        webbrowser.open(url)

    # Function to open Outlook with the recipient email pre-filled
    def open_outlook(self, subject, body):
        """Ouvre un brouillon dans l'application de bureau Outlook avec le sujet, le corps et le destinataire pré-remplis."""
        try:
            recipient_email = load_email()  # Load the recipient email from the JSON file
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)  # 0 = olMailItem
            mail.Subject = subject
            mail.Body = body
            mail.To = recipient_email  # Set the recipient email
            mail.Display()  # Display the draft without sending it
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

    def toggle_email_client(self):
        """Change le client de messagerie entre Gmail et Outlook et met à jour l'image du bouton."""
        if self.email_client == "Gmail":
            self.email_client = "Outlook"
            self.email_client_button.configure(image=self.outlook_image)
        else:
            self.email_client = "Gmail"
            self.email_client_button.configure(image=self.gmail_image)

    def save_prefix(self):
        """Enregistre le préfixe dans la configuration."""
        config["prefix"] = self.entry_prefix.get()
        save_config(config)
        messagebox.showinfo("Succès", "Préfixe enregistré avec succès.")

    def save_suffix(self):
        """Enregistre le suffixe dans la configuration."""
        config["suffix"] = self.entry_suffix.get()
        save_config(config)
        messagebox.showinfo("Succès", "Suffixe enregistré avec succès.")

    def save_api_key(self):
        """Enregistre la clé API."""
        api_key = self.entry_api_key.get()
        save_api_key(api_key)
        messagebox.showinfo("Succès", "Clé API enregistrée avec succès.")

    def visit_api_site(self):
        """Ouvre le site CloudConvert pour configurer l'API."""
        webbrowser.open("https://cloudconvert.com/apis/file-conversion")

    def save_email(self):
        """Enregistre l'email du destinataire."""
        email = self.entry_email.get()
        save_email(email)
        messagebox.showinfo("Succès", "Email du destinataire enregistré avec succès.")

    def save_default_client(self):
        """Enregistre le client par défaut pour l'envoi des emails."""
        client = self.entry_client.get()
        save_default_client(client)
        messagebox.showinfo("Succès", "Client par défaut enregistré avec succès.")

# Lancement de l'application
if __name__ == "__main__":
    logging.debug("Lancement de l'application.")
    app = FolderSelectorApp()
    app.mainloop()
    logging.debug("Application fermée.")
