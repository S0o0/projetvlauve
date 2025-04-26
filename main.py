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

def main():
    
    from DAO.DAOSession import DAOSession

    # Ouvrir la session DAO
    DAOSession.open()

    DAOSession.close()

if __name__ == "__main__":
    main()
    # 🧪 Utilisateur de test avec quelques trajets
    utilisateur_test = Vlauveur(
        numVlauveur=1,
        email="test@vlauve.fr",
        motDePasse="1234",
        nom="Durand",
        prenom="Claire",
        tel="+33612345678",
        numAdresse=10,
        nomRue="Rue de l'Exemple",
        codePostal=54000,
        nomVille="Nancy",
        typeAbo="annuel"
    )
   

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Application de Connexion")
    centrer_fenetre(root, 300, 250)

    app = AppController(root)

    root.mainloop()
