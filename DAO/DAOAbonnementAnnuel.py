from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOAbonnementAnnuel:
    # Implémente le pattern Singleton : une seule instance de DAOAbonnementAnnuel sera utilisée dans toute l'application
    unique_instance = None

    @staticmethod
    def get_instance():
        # Crée ou retourne l'instance unique
        if DAOAbonnementAnnuel.unique_instance is None:
            DAOAbonnementAnnuel.unique_instance = DAOAbonnementAnnuel()
        return DAOAbonnementAnnuel.unique_instance

    def insert_abonnement_annuel(self, un_abonnement_annuel):
        # Insère un abonnement annuel dans la base de données
        sql = "INSERT INTO AbonnementAnnuel (numAbo, typeAbonnement) VALUES (%s, %s)"
        valeurs = (un_abonnement_annuel.get_numAbo(), un_abonnement_annuel.get_typeAbonnement())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            # Pas besoin de commit ici si la transaction est gérée en dehors
            return True
        except Error as e:
            # Affiche les détails de l'erreur SQL
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de abonnement_annuel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()  # Annule les modifications en cas d'échec
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_abonnement_annuel(self, un_abonnement_annuel):
        # Supprime un abonnement annuel identifié par son numéro
        sql = "DELETE FROM abonnement_annuel WHERE numAbo = %s"
        valeurs = (un_abonnement_annuel.get_numAbo(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de abonnement_annuel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_abonnement_annuel(self, un_abonnement_annuel):
        # Met à jour le type d'un abonnement annuel existant
        sql = "UPDATE AbonnementAnnuel SET typeAbonnement = %s WHERE numAbo = %s"
        valeurs = (un_abonnement_annuel.get_typeAbonnement(), un_abonnement_annuel.get_numAbo())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de abonnement annuel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def set_all_values(self, rs):
        # Convertit un dictionnaire de résultat SQL en objet AbonnementAnnuel
        from Composants.abonnement_annuel import AbonnementAnnuel
        un_abonnement_annuel = AbonnementAnnuel(rs["numAbo"], rs["typeAbonnement"])
        return un_abonnement_annuel