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
    # Création des utilisateurs 
    utilisateurs = [
        # Utilisateur("admin", "admin123"),
        # Utilisateur("alice", "motdepasse"),
        # Utilisateur("bob", "azerty")
        Vlauveur(1,"aze@gmail.com","1234","DJELASSI","Lenny","+3379216372","8","rue du Moulin","54000","Nancy","Mensuel")
    ]

    # Simulation : ajout de trajets pour tester l'affichage
    from Composants.trajet import Trajet
    t1 = Trajet(1, 2, 3, 4.5, "2024-04-01", "2024-04-01", "08:00", "08:50", 1)
    t2 = Trajet(2, 3, 2, 2.0, "2024-04-02", "2024-04-02", "09:00", "09:20", 1)

    utilisateur_test.trajets.append(t1)
    utilisateur_test.trajets.append(t2)

    # Création de la fenêtre principale
    root = tk.Tk()
    centrer_fenetre(root, 400, 400)
    root.title("Application Vlauve")

    # Lancement du contrôleur principal avec utilisateur préchargé
    app = AppController(root)
    app.ajouter_utilisateur(utilisateur_test)

    root.mainloop()
