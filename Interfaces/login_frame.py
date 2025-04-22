# Classe principale de l'interface de connexion
from tkinter import ttk, messagebox

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Adresse mail").pack(pady=5)
        self.mail_entry = ttk.Entry(self)
        self.mail_entry.pack()

        ttk.Label(self, text="Mot de passe").pack(pady=5)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack()

        ttk.Button(self, text="Se connecter", command=self.login).pack(pady=10)
        ttk.Button(self, text="Créer un compte", command=self.controller.afficher_creation_compte).pack()

    def login(self):
        mail = self.mail_entry.get()
        mot_de_passe = self.password_entry.get()

        for utilisateur in self.controller.utilisateurs:
            if utilisateur.verifier_identifiants(mail, mot_de_passe):
                messagebox.showinfo("Connexion réussie", f"Bienvenue {utilisateur.prenom} !")
                self.controller.connecter_utilisateur(utilisateur)
                return

        messagebox.showerror("Erreur", "Adresse mail ou mot de passe incorrect.")
