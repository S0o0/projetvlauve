from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOAbonnement:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAbonnement.unique_instance is None:
            DAOAbonnement.unique_instance = DAOAbonnement()
        return DAOAbonnement.unique_instance

    def insert_abonnement(self, un_abonnement):
        sql = "INSERT INTO Abonnement (numAbo, refVlauveur) VALUES (%s, %s)"
        valeurs = (un_abonnement.get_numAbo(), un_abonnement.get_refVlauveur())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            # print(sql)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_abonnement(self, un_abonnement):
        sql = "DELETE FROM Abonnement WHERE numAbo = %s"
        valeurs = (un_abonnement.get_numAbo(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()

    
    
    def find_abonnement(self, ref_vlauveur):
        sql_abo = "SELECT numAbo FROM Abonnement WHERE refVlauveur = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)

            # Rechercher l'abonnement principal
            cursor.execute(sql_abo, (ref_vlauveur,))
            result = cursor.fetchone()
            if not result:
                return None  # Aucun abonnement

            numAbo = result["numAbo"]

            # Vérifier si c’est un abonnement annuel
            sql_annuel = "SELECT typeAbonnement FROM AbonnementAnnuel WHERE numAbo = %s"
            cursor.execute(sql_annuel, (numAbo,))
            rs_annuel = cursor.fetchone()
            if rs_annuel:
                return {
                    "numAbo": numAbo,
                    "type": "annuel",
                    "typeAbonnement": rs_annuel["typeAbonnement"]
                }

            # Vérifier si c’est un abonnement occasionnel
            sql_occasionnel = "SELECT duree FROM AbonnementOccasionnel WHERE numAbo = %s"
            cursor.execute(sql_occasionnel, (numAbo,))
            rs_occ = cursor.fetchone()
            if rs_occ:
                return {
                    "numAbo": numAbo,
                    "type": "occasionnel",
                    "duree": rs_occ["duree"]
                }

            return {
                "numAbo": numAbo,
                "type": "inconnu"
            }

        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'abonnement : {e}")
            print(sql_abo)
            return None

        finally:
            if cursor:
                cursor.close()

    def update_abonnement(self, un_abonnement):
        sql = "UPDATE Abonnement SET refVlauveur = %s WHERE numAbo = %s"
        valeurs = (un_abonnement.get_refVlauveur(), un_abonnement.get_numAbo())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()

    # def select_abonnement(self, un_abonnement):
    #     les_abonnements = []
    #     sql = "SELECT * FROM abonnement WHERE "
    #     critere_id_vin = un_abonnement.get_idVin()
    #     critere_id_buveur = un_abonnement.get_idBuveur()
    #     critere_qte = un_abonnement.get_qte()
    #     valeurs = []

    #     if critere_id_vin is not None:
    #         sql += "idVin = %s"
    #         valeurs.append(critere_id_vin)
    #     elif critere_id_buveur is not None:
    #         sql += "buveurId = %s"
    #         valeurs.append(critere_id_buveur)
    #     elif critere_qte is not None:
    #         sql += "nbBouteilles = %s"
    #         valeurs.append(critere_qte)
    #     else:
    #         sql = "SELECT * FROM abonnement"

    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor(dictionary=True)
    #         cursor.execute(sql, tuple(valeurs))
    #         rs = cursor.fetchall()
    #         for row in rs:
    #             les_abonnements.append(self.set_all_values(row))
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la recherche de abonnement : {e}")
    #         print(sql)
    #         print(valeurs)
    #     finally:
    #         if cursor:
    #             cursor.close()
    #     return les_abonnements

    def set_all_values(self, rs):
        from Composants.abonnement import Abonnement
        un_abonnement = Abonnement(rs["numAbo"], rs["refVlauveur"])
        return un_abonnement