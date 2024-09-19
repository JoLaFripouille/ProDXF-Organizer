import customtkinter as ctk
from tkinter import messagebox, PhotoImage, filedialog
import os
import json
import requests
import webbrowser

# Configuration paths
CONFIG_PATH = "JSON/FormatBlocks.json"
API_KEY_PATH = "API_KEY.env"
EMAIL_PATH = "JSON/AddEmail.json"
CONFIG_ENVOI_PATH = "JSON/ConfigEnvoi.json"
ACAD_TOOLS_PATH = "JSON/acadTools.json"

DEFAULT_HEIGHT = 38
DEFAULT_CORNER_RADIUS = DEFAULT_HEIGHT // 2

# Functions for configuration management
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    return {"prefix": "DEV", "suffix": "TL"}

def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)

def load_api_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, "r") as file:
            line = file.read().strip()
            if line.startswith("API_KEY="):
                return line.split("=", 1)[1]
    return ""

def save_api_key(api_key):
    with open(API_KEY_PATH, "w") as file:
        file.write(f"API_KEY={api_key}")

def load_email():
    if os.path.exists(EMAIL_PATH):
        with open(EMAIL_PATH, "r") as file:
            return json.load(file).get("email", "")
    return ""

def save_email(email):
    with open(EMAIL_PATH, "w") as file:
        json.dump({"email": email}, file, indent=4)

def load_default_client():
    if os.path.exists(CONFIG_ENVOI_PATH):
        with open(CONFIG_ENVOI_PATH, "r") as file:
            return json.load(file).get("default_client", "Gmail")
    return "Gmail"

def save_default_client(client):
    with open(CONFIG_ENVOI_PATH, "w") as file:
        json.dump({"default_client": client}, file, indent=4)

def load_acad_tools():
    if os.path.exists(ACAD_TOOLS_PATH):
        with open(ACAD_TOOLS_PATH, "r") as file:
            return json.load(file)
    return []

# Load configurations
config = load_config()
api_key = load_api_key()
email = load_email()
default_client = load_default_client()
acad_tools = load_acad_tools()

class Tab3(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)

        # Main frame containing the scrollable frame
        self.main_frame = ctk.CTkFrame(self, fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable frame for configurations
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="black", corner_radius=DEFAULT_CORNER_RADIUS)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Prefix and Suffix Configuration
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

        # API Key Configuration
        self.config_api_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_api_frame.pack(fill="x", padx=10, pady=10)

        self.entry_api_key = ctk.CTkEntry(self.config_api_frame, placeholder_text="Clé API", width=400, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.entry_api_key.insert(0, api_key)
        self.entry_api_key.pack(pady=10, padx=5)

        self.save_api_key_button = ctk.CTkButton(self.config_api_frame, text="Enregistrer Clé API", command=self.save_api_key, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_api_key_button.pack(pady=10, padx=5)

        self.visit_api_button = ctk.CTkButton(self.config_api_frame, text="Visiter API CloudConvert", command=self.visit_api_site, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.visit_api_button.pack(pady=10, padx=5)

        # Email Configuration
        self.config_email_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_email_frame.pack(fill="x", padx=10, pady=10)

        self.entry_email = ctk.CTkEntry(self.config_email_frame, placeholder_text="Email destinataire", width=400, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT, justify="center")
        self.entry_email.insert(0, email)
        self.entry_email.pack(pady=10, padx=5)

        self.save_email_button = ctk.CTkButton(self.config_email_frame, text="Enregistrer Email", command=self.save_email, corner_radius=DEFAULT_CORNER_RADIUS, height=DEFAULT_HEIGHT)
        self.save_email_button.pack(pady=10, padx=5)

        # Default Client Configuration
        self.config_client_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.config_client_frame.pack(fill="x", padx=10, pady=10)

        self.client_options = ["Gmail", "Outlook"]
        self.client_var = ctk.StringVar(value=default_client)
        self.client_dropdown = ctk.CTkOptionMenu(self.config_client_frame, values=self.client_options, variable=self.client_var, command=self.save_default_client)
        self.client_dropdown.pack(pady=10, padx=5)

        # AutoLISP Project Link
        self.autolisp_link_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.autolisp_link_frame.pack(fill="x", padx=10, pady=10)

        self.autolisp_label = ctk.CTkLabel(self.autolisp_link_frame, text="Lien du projet Autolisp ICI", font=("Helvetica", 16))
        self.autolisp_label.pack(side="left", padx=10, pady=10)

        self.github_image = PhotoImage(file="asset/img/github.png")
        self.github_button = ctk.CTkButton(
            self.autolisp_link_frame,
            image=self.github_image,
            command=lambda: webbrowser.open("https://github.com/JoLaFripouille/AutoLisp"),
            corner_radius=25,
            width=200,
            height=50,
            border_width=2,
            fg_color="#151b23",
            text=""
        )
        self.github_button.pack(side="left", padx=10, pady=10)

        # AutoCAD Tools
        self.tools_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20", corner_radius=DEFAULT_CORNER_RADIUS)
        self.tools_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_acad_tools_ui()

    def save_prefix(self):
        config["prefix"] = self.entry_prefix.get()
        save_config(config)
        messagebox.showinfo("Succès", "Préfixe enregistré avec succès.")

    def save_suffix(self):
        config["suffix"] = self.entry_suffix.get()
        save_config(config)
        messagebox.showinfo("Succès", "Suffixe enregistré avec succès.")

    def save_api_key(self):
        api_key = self.entry_api_key.get()
        save_api_key(api_key)
        messagebox.showinfo("Succès", "Clé API enregistrée avec succès.")

    def visit_api_site(self):
        webbrowser.open("https://cloudconvert.com/apis/file-conversion")

    def save_email(self):
        email = self.entry_email.get()
        save_email(email)
        messagebox.showinfo("Succès", "Email du destinataire enregistré avec succès.")

    def save_default_client(self, client):
        save_default_client(client)
        messagebox.showinfo("Succès", "Client par défaut enregistré avec succès.")

    def load_acad_tools_ui(self):
        for tool in acad_tools:
            tool_frame = ctk.CTkFrame(self.tools_frame, fg_color="gray25", corner_radius=DEFAULT_CORNER_RADIUS)
            tool_frame.pack(fill="x", padx=10, pady=5)

            tool_name_label = ctk.CTkLabel(tool_frame, text=tool["name"], font=("Helvetica", 16))
            tool_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            tool_description_label = ctk.CTkLabel(tool_frame, text=tool["description"])
            tool_description_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

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
        try:
            response = requests.get(url)
            response.raise_for_status()
            file_path = filedialog.asksaveasfilename(defaultextension=".lsp", initialfile=name, filetypes=[("Lisp Files", "*.lsp")])
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                messagebox.showinfo("Téléchargement", f"Script {name} téléchargé avec succès dans {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du téléchargement du script {name}. Erreur: {e}")
