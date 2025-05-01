import tkinter as tk
from Composants.vlauveur import Vlauveur
from Interfaces.app_controller import AppController
from DAO.DAOSession import DAOSession
from DAO.DAOVlauveur import DAOVlauveur

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

    # dao = DAOVlauveur()
    # email = "test@gmail.com"
    # mot_de_passe = "azerty"  # mot de passe en clair utilisé à l'inscription

    # print(f"Essai de connexion avec l'email: {email} et le mot de passe: {mot_de_passe}")
    # vlauveur = dao.find_by_credentials(email, mot_de_passe)

    # if vlauveur:
    #     print("Connexion réussie :", vlauveur.nom, vlauveur.prenom)
    # else:
    #     print("Adresse mail ou mot de passe incorrect.")
    
    DAOSession.close()

if __name__ == "__main__":
    main()
   
   

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Application de Connexion")
    centrer_fenetre(root, 300, 250)

    app = AppController(root)

    root.mainloop()
