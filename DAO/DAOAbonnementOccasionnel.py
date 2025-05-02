from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOAbonnementOccasionnel:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAbonnementOccasionnel.unique_instance is None:
            DAOAbonnementOccasionnel.unique_instance = DAOAbonnementOccasionnel()
        return DAOAbonnementOccasionnel.unique_instance

    def insert_abonnement_occasionnel(self, un_abonnement_occasionnel):
        sql = "INSERT INTO AbonnementOccasionnel (numAbo, duree) VALUES (%s, %s)"
        valeurs = (un_abonnement_occasionnel.get_numAbo(), un_abonnement_occasionnel.get_duree())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            # print(sql)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de abonnement_occasionnel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_abonnement_occasionnel(self, un_abonnement_occasionnel):
        sql = "DELETE FROM abonnement_occasionnel WHERE numAbo = %s"
        valeurs = (un_abonnement_occasionnel.get_numAbo())
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

    # def find_abonnement_occasionnel(self, id_vin, id_buveur):
    #     sql = "SELECT * FROM abonnement_occasionnel WHERE idVin = %s AND buveurId = %s"
    #     valeurs = (id_vin, id_buveur)
    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor(dictionary=True)
    #         cursor.execute(sql, valeurs)
    #         rs = cursor.fetchone()
    #         if rs:
    #             return self.set_all_values(rs)
    #         else:
    #             return None
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la recherche de abonnement_occasionnel : {e}")
    #         print(sql)
    #         print(valeurs)
    #         return None
    #     finally:
    #         if cursor:
    #             cursor.close()

    def update_abonnement_occasionnel(self, un_abonnement_occasionnel):
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

    # def select_abonnement_occasionnel(self, un_abonnement_occasionnel):
    #     les_abonnements_occasionnels = []
    #     sql = "SELECT * FROM AbonnementOccasionnel WHERE "
    #     critere_id_vin = un_abonnement_occasionnel.get_idVin()
    #     critere_id_buveur = un_abonnement_occasionnel.get_idBuveur()
    #     critere_qte = un_abonnement_occasionnel.get_qte()
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
    #         sql = "SELECT * FROM abonnement_occasionnel"

    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor(dictionary=True)
    #         cursor.execute(sql, tuple(valeurs))
    #         rs = cursor.fetchall()
    #         for row in rs:
    #             les_abonnements_occasionnels.append(self.set_all_values(row))
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la recherche de abonnement_occasionnel : {e}")
    #         print(sql)
    #         print(valeurs)
    #     finally:
    #         if cursor:
    #             cursor.close()
    #     return les_abonnements_occasionnels

    def set_all_values(self, rs):
        from Composants.abonnement_occasionnel import AbonnementOccasionnel
        un_abonnement_occasionnel = AbonnementOccasionnel(rs["numAbo"], rs["duree"])
        return un_abonnement_occasionnel