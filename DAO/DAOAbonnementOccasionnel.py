from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOAbonnementOccasionnel:
    # Implémentation du pattern Singleton pour s'assurer qu'une seule instance est utilisée dans tout le programme
    unique_instance = None

    @staticmethod
    def get_instance():
        # Retourne l'instance unique, ou la crée si elle n'existe pas encore
        if DAOAbonnementOccasionnel.unique_instance is None:
            DAOAbonnementOccasionnel.unique_instance = DAOAbonnementOccasionnel()
        return DAOAbonnementOccasionnel.unique_instance

    def insert_abonnement_occasionnel(self, un_abonnement_occasionnel):
        # Insère un nouvel abonnement occasionnel dans la base de données
        sql = "INSERT INTO AbonnementOccasionnel (numAbo, duree) VALUES (%s, %s)"
        valeurs = (un_abonnement_occasionnel.get_numAbo(), un_abonnement_occasionnel.get_duree())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de abonnement_occasionnel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()  # Annule l'opération si une erreur survient
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_abonnement_occasionnel(self, un_abonnement_occasionnel):
        # Supprime un abonnement occasionnel en fonction de son numéro
        sql = "DELETE FROM abonnement_occasionnel WHERE numAbo = %s"
        valeurs = (un_abonnement_occasionnel.get_numAbo(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de abonnement_occasionnel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_abonnement_occasionnel(self, un_abonnement_occasionnel):
        # Met à jour la durée d'un abonnement occasionnel
        sql = "UPDATE AbonnementOccasionnel SET duree = %s WHERE numAbo = %s"
        valeurs = (un_abonnement_occasionnel.get_duree(), un_abonnement_occasionnel.get_numAbo())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de abonnement occasionnel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def set_all_values(self, rs):
        # Convertit une ligne de résultat SQL (dictionnaire) en un objet AbonnementOccasionnel
        from Composants.abonnement_occasionnel import AbonnementOccasionnel
        un_abonnement_occasionnel = AbonnementOccasionnel(rs["numAbo"], rs["duree"])
        return un_abonnement_occasionnel