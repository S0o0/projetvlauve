import tkinter as tk
from Interfaces.login_frame import LoginFrame
from Interfaces.create_account_frame import CreateAccountFrame
from Interfaces.accueil_frame import AccueilFrame

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Projet Vlauve")

        self.utilisateurs = []              # liste de tous les vlauveurs enregistrés
        self.utilisateur_connecte = None    # vlauveur actuellement connecté

        self.frame_actuelle = None          # pour changer dynamiquement d’écran
        self.afficher_login()               # on démarre par l'écran de connexion

    # Méthode pour afficher l’écran de connexion
    def afficher_login(self):
        self._changer_frame(LoginFrame)

    # Méthode pour afficher la page de création de compte
    def afficher_creation_compte(self):
        self._changer_frame(CreateAccountFrame)

    # Méthode pour afficher la page d’accueil une fois connecté
    def afficher_accueil(self):
        self._changer_frame(AccueilFrame)

    # Méthode centrale pour changer de frame
    def _changer_frame(self, FrameClass):
        if self.frame_actuelle:
            self.frame_actuelle.destroy()
        self.frame_actuelle = FrameClass(self.root, self)
        self.frame_actuelle.pack()

    # Ajouter un nouvel utilisateur à la liste
    def ajouter_utilisateur(self, vlauveur):
        self.utilisateurs.append(vlauveur)

    # Enregistrer l’utilisateur connecté
    def connecter_utilisateur(self, vlauveur):
        self.utilisateur_connecte = vlauveur
        self.afficher_accueil()
