# Classe principale de l'interface de connexion
from tkinter import ttk, messagebox
from DAO.DAOVlauveur import DAOVlauveur

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
        print(f"Essai de connexion avec l'email: {mail} et le mot de passe (en clair): {mot_de_passe}")

        print(f"Email saisi : {repr(mail)}")
        print(f"Mot de passe saisi : {repr(mot_de_passe)}")

        
        dao = DAOVlauveur.get_instance()
        
        # Utilisation de la méthode find_by_credentials pour authentifier l'utilisateur
        utilisateur = dao.find_by_credentials(mail, mot_de_passe)

        if utilisateur:
            print(f"Utilisateur trouvé : {utilisateur.prenom} {utilisateur.nom}")
            messagebox.showinfo("Connexion réussie", f"Bienvenue {utilisateur.prenom} !")
            self.controller.connecter_utilisateur(utilisateur)
        else:
            print(f"Utilisateur avec l'email {mail} non trouvé ou mot de passe incorrect.")
            messagebox.showerror("Erreur", "Adresse mail ou mot de passe incorrect.")

