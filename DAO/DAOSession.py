import mysql.connector
from mysql.connector import Error 
<<<<<<< HEAD
=======

>>>>>>> main
class DAOSession:
    
    # Propriétés statiques
    HOST = "localhost"
    LOGIN = "root"
    MDP = ""
    DB="projetVlauve"
<<<<<<< HEAD
=======
    PORT = 3306
>>>>>>> main
    connection = None

    @staticmethod
    def creer_connection():
        try:
            DAOSession.connection = mysql.connector.connect(
                host=DAOSession.HOST,
                user=DAOSession.LOGIN,
                password=DAOSession.MDP,
<<<<<<< HEAD
                database=DAOSession.DB
=======
                database=DAOSession.DB,
                port=DAOSession.PORT
>>>>>>> main
            )
            if DAOSession.connection.is_connected():
                print("Connexion à la base de données réussie")
            else:
                print("Erreur de connexion à la base")
        except Error as e:
            print(f"Erreur durant la connexion à la base de données: {e}")

    @staticmethod
    def get_connexion():
        if DAOSession.connection is None:
            DAOSession.creer_connection()
        return DAOSession.connection
   
    def open():
        DAOSession.get_connexion().start_transaction()

   
    def close():
        DAOSession.get_connexion().commit()
        DAOSession.get_connexion().close()
        DAOSession.connection = None
<<<<<<< HEAD
        print("Fermeture de la connexion à la base de données")
=======
        print("Fermeture de la connexion à la base de données")


    



>>>>>>> main
