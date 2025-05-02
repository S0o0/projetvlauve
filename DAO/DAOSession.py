import mysql.connector
from mysql.connector import Error 

class DAOSession:
    # Classe utilitaire pour gérer la connexion à la base de données MySQL

    # Paramètres de connexion (constants pour la session)
    HOST = "localhost"      # Adresse du serveur de base de données
    LOGIN = "root"          # Nom d'utilisateur MySQL
    MDP = ""                # Mot de passe MySQL (à adapter selon configuration locale)
    DB = "projetVlauve"     # Nom de la base de données cible
    connection = None       # Objet de connexion partagée (singleton)

    @staticmethod
    def creer_connection():
        # Établit une connexion à la base de données si ce n'est pas déjà fait
        try:
            DAOSession.connection = mysql.connector.connect(
                host=DAOSession.HOST,
                user=DAOSession.LOGIN,
                password=DAOSession.MDP,
                database=DAOSession.DB
            )
            if DAOSession.connection.is_connected():
                print("Connexion à la base de données réussie")
            else:
                print("Erreur de connexion à la base")
        except Error as e:
            print(f"Erreur durant la connexion à la base de données: {e}")

    @staticmethod
    def get_connexion():
        # Retourne la connexion active, ou la crée si nécessaire
        if DAOSession.connection is None:
            DAOSession.creer_connection()
        return DAOSession.connection

    @staticmethod
    def open():
        # Démarre une transaction explicite sur la connexion active
        DAOSession.get_connexion().start_transaction()

    @staticmethod
    def close():
        # Termine proprement la session SQL : commit + fermeture de connexion
        DAOSession.get_connexion().commit()  # Applique les modifications
        DAOSession.get_connexion().close()   # Ferme la connexion MySQL
        DAOSession.connection = None         # Réinitialise l'état
        print("Fermeture de la connexion à la base de données")
