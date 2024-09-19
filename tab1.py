import customtkinter as ctk

class Tab1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        # Add widgets specific to Tab1 here, for example:
        label = ctk.CTkLabel(self, text="Contenu de l'onglet 1")
        label.pack(padx=20, pady=20)
