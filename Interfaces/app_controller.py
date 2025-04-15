import tkinter as tk
from Interfaces.login_frame import LoginFrame
from Interfaces.accueil_frame import AccueilFrame
from Interfaces.create_account_frame import CreateAccountFrame

class AppController:
    def __init__(self, root, utilisateurs):
        self.root = root
        self.utilisateurs = utilisateurs
        self.frame_courant = None

        self.afficher_login()

    def changer_frame(self, nouvelle_frame):
        if self.frame_courant:
            self.frame_courant.destroy()
        self.frame_courant = nouvelle_frame
        self.frame_courant.pack(fill="both", expand=True)

    def afficher_login(self):
        self.changer_frame(LoginFrame(self.root, self, self.utilisateurs))

    def afficher_creation_compte(self):
        self.changer_frame(CreateAccountFrame(self.root, self, self.utilisateurs))

    def afficher_accueil(self, email):
        self.utilisateur_actif = email
        
        self.changer_frame(AccueilFrame(self.root, self, email))
