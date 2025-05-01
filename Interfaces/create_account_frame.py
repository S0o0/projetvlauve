from tkinter import ttk, messagebox
from Composants.vlauveur import Vlauveur
import hashlib
import secrets

class CreateAccountFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Créer un compte", font=("Arial", 14)).pack(pady=10)

        # Champs de saisie
        ttk.Label(self, text="Prénom").pack()
        self.entry_prenom = ttk.Entry(self)
        self.entry_prenom.pack()

        ttk.Label(self, text="Nom").pack()
        self.entry_nom = ttk.Entry(self)
        self.entry_nom.pack()

        ttk.Label(self, text="Email").pack()
        self.entry_email = ttk.Entry(self)
        self.entry_email.pack()

        ttk.Label(self, text="Mot de passe").pack()
        self.entry_mdp = ttk.Entry(self, show="*")
        self.entry_mdp.pack()

        ttk.Label(self, text="Téléphone").pack()
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.pack()

        ttk.Label(self, text="Numéro de rue").pack()
        self.entry_num_adresse = ttk.Entry(self)
        self.entry_num_adresse.pack()

        ttk.Label(self, text="Nom de rue").pack()
        self.entry_nom_rue = ttk.Entry(self)
        self.entry_nom_rue.pack()

        ttk.Label(self, text="Code postal").pack()
        self.entry_code_postal = ttk.Entry(self)
        self.entry_code_postal.pack()

        ttk.Label(self, text="Ville").pack()
        self.entry_ville = ttk.Entry(self)
        self.entry_ville.pack()

        ttk.Label(self, text="Type d'abonnement (occasionnel ou annuel)").pack()
        self.entry_type_abo = ttk.Entry(self)
        self.entry_type_abo.pack()

        # Boutons
        ttk.Button(self, text="Créer le compte", command=self.creer_compte).pack(pady=10)
        ttk.Button(self, text="Retour", command=self.controller.afficher_login).pack()

    def creer_compte(self):
        # Vérification simple des champs
        if self.entry_email.get() == "" or self.entry_mdp.get() == "":
            messagebox.showwarning("Erreur", "Email et mot de passe sont obligatoires.")
            return

        # Génération de l’ID utilisateur
        num = len(self.controller.utilisateurs) + 1
        
        # Récupération du mot de passe et génération du salt
        mdp = self.entry_mdp.get()
        salt = secrets.token_hex(16)
        mdp_salte = mdp + salt
        hash_mdp = hashlib.sha256(mdp_salte.encode()).hexdigest()
        hash_final = f"{hash_mdp}/{salt}"
        print("Mot de passe haché à insérer :", hash_final)

        # Création du vlauveur
        
        v = Vlauveur(
            num,
            self.entry_email.get(),
            hash_final,
            self.entry_nom.get(),
            self.entry_prenom.get(),
            self.entry_tel.get(),
            int(self.entry_num_adresse.get()),
            self.entry_nom_rue.get(),
            int(self.entry_code_postal.get()),
            self.entry_ville.get(),
            self.entry_type_abo.get()
        )

        self.controller.ajouter_utilisateur(v)
        v.leDAOVlauveur.insert_vlauveur(v)
        messagebox.showinfo("Succès", "Compte créé avec succès !")
        self.controller.connecter_utilisateur(v)