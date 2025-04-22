import tkinter as tk
from Composants.vlauveur import Vlauveur
from Interfaces.app_controller import AppController

def centrer_fenetre(fenetre, largeur, hauteur):
    # Obtenir la taille de l'écran
    ecran_largeur = fenetre.winfo_screenwidth()
    ecran_hauteur = fenetre.winfo_screenheight()

    # Calculer la position x et y pour centrer
    x = (ecran_largeur - largeur) // 2
    y = (ecran_hauteur - hauteur) // 2

    # Appliquer la taille + position
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

if __name__ == "__main__":
    # Création des utilisateurs 
    utilisateurs = [
        # Utilisateur("admin", "admin123"),
        # Utilisateur("alice", "motdepasse"),
        # Utilisateur("bob", "azerty")
        Vlauveur(1,"aze@gmail.com","1234","DJELASSI","Lenny","+3379216372","8","rue du Moulin","54000","Nancy","Mensuel")
    ]

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Application de Connexion")
    centrer_fenetre(root, 300, 250)

    app = AppController(root,utilisateurs)

    root.mainloop()
