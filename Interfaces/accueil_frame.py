from tkinter import ttk

class AccueilFrame(ttk.Frame):
    def __init__(self, parent, controller, nom_utilisateur):
        super().__init__(parent)
        self.controller = controller

        message = f"Bienvenue {nom_utilisateur} !"
        ttk.Label(self, text=message, font=("Helvetica", 16)).pack(pady=30)
        
        ttk.Button(self, text="Déconnexion", command=self.controller.afficher_login).pack()