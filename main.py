import customtkinter as ctk
from tab1 import Tab1  # Assuming you have Tab1 in tab1.py
from tab2 import Tab2  # Importing the second tab class
from tab3 import Tab3  # Assuming you have Tab3 in tab3.py
import logging

# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration des constantes
DEFAULT_HEIGHT = 38
DEFAULT_CORNER_RADIUS = DEFAULT_HEIGHT // 2

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

        # Boutons pour simuler des onglets dans la sidebar
        self.button_onglet1 = ctk.CTkButton(
            self.sidebar_frame, text="Onglet 1", command=self.show_tab1, corner_radius=DEFAULT_CORNER_RADIUS
        )
        self.button_onglet1.pack(padx=10, pady=10)

        self.button_onglet2 = ctk.CTkButton(
            self.sidebar_frame, text="Onglet 2", command=self.show_tab2, corner_radius=DEFAULT_CORNER_RADIUS
        )
        self.button_onglet2.pack(padx=10, pady=10)

        self.button_onglet3 = ctk.CTkButton(
            self.sidebar_frame, text="Onglet 3", command=self.show_tab3, corner_radius=DEFAULT_CORNER_RADIUS
        )
        self.button_onglet3.pack(padx=10, pady=10)

        # Initialiser les tabs
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)
        self.tab3 = Tab3(self)

        # Place tabs in the main grid
        self.tab1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.tab2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.tab3.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Affichage initial du premier onglet
        self.show_tab1()

    def show_tab1(self):
        """Affiche le premier onglet et cache les autres."""
        self.tab1.tkraise()

    def show_tab2(self):
        """Affiche le second onglet et cache les autres."""
        self.tab2.tkraise()

    def show_tab3(self):
        """Affiche le troisième onglet et cache les autres."""
        self.tab3.tkraise()

# Lancement de l'application
if __name__ == "__main__":
    logging.debug("Lancement de l'application.")
    app = FolderSelectorApp()
    app.mainloop()
    logging.debug("Application fermée.")
