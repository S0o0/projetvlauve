from tkinter import messagebox
from tkinter import ttk
from Composants.utilisateur import Utilisateur

class CreateAccountFrame(ttk.Frame):
    def __init__(self, parent, controller,utilisateurs):
        super().__init__(parent)
        
        
        root = tk.Tk()
        root.title("Application de Connexion")
        centrer_fenetre(root, 300, 250)
        
        self.controller = controller
        self.utilisateurs = utilisateurs

        ttk.Label(self, text="Créer un compte").pack(pady=10)
        
        ttk.Label(self, text="Nom").pack()
        self.lastname_entry = ttk.Entry(self)
        self.lastname_entry.pack()
        
        ttk.Label(self, text="Prénom").pack()
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.pack()
        
        ttk.Label(self, text="Email").pack()
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()
        
        ttk.Label(self, text="Numéro de téléphone").pack()
        self.tel_entry = ttk.Entry(self)
        self.tel_entry.pack()
        
        ttk.Label(self, text="Adresse").pack()
        self.adresse_entry = ttk.Entry(self)
        self.adresse_entry.pack()
        
        ttk.Label(self, text="Type d'abonnement").pack()
        self.typeAbo_entry = ttk.Entry(self)
        self.typeAbo_entry.pack()

        ttk.Label(self, text="Mot de passe").pack(pady=5)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack()

        ttk.Button(self, text="Créer", command=self.create_account).pack(pady=10)
        ttk.Button(self, text="Retour", command=self.controller.afficher_login).pack()

    def create_account(self):
        nom = self.lastname_entry.get()
        prenom = self.firstname_entry.get()
        email = self.email_entry.get()
        tel = self.tel_entry.get()
        adresse = self.adresse_entry.get()
        typeAbo = self.typeAbo_entry.get()
        mot_de_passe = self.password_entry.get()        

        if not nom or not prenom or not email or not tel or not adresse or not typeAbo or not mot_de_passe:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")
            return

        for utilisateur in self.utilisateurs:
            if utilisateur.email == email:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
                return

        nouveau = Utilisateur(nom, prenom, mot_de_passe, email, tel, adresse, typeAbo)
        self.utilisateurs.append(nouveau)
        messagebox.showinfo("Succès", "Compte créé avec succès !")
        self.controller.afficher_login()