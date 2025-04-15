# Classe principale de l'interface de connexion
from tkinter import messagebox
from tkinter import ttk

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller, utilisateurs):
        super().__init__(parent)
        self.controller = controller
        self.utilisateurs = utilisateurs

        ttk.Label(self, text="Email").pack(pady=5)
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()

        ttk.Label(self, text="Mot de passe").pack(pady=5)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack()

        ttk.Button(self, text="Se connecter", command=self.login).pack(pady=10)
        ttk.Button(self, text="Créer un compte", command=self.controller.afficher_creation_compte).pack()
    
    def login(self):
        email = self.email_entry.get()
        mot_de_passe = self.password_entry.get()
        # Vérifie les identifiants parmi les utilisateurs existants
        for utilisateur in self.utilisateurs:
            if utilisateur.verifier_identifiants(email, mot_de_passe):
                messagebox.showinfo("Succès", f"Bienvenue {email} !")
                self.controller.afficher_accueil(email)
                return
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

