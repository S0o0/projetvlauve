from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOAbonnementAnnuel:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAbonnementAnnuel.unique_instance is None:
            DAOAbonnementAnnuel.unique_instance = DAOAbonnementAnnuel()
        return DAOAbonnementAnnuel.unique_instance

    def insert_abonnement_annuel(self, un_abonnement_annuel):
        sql = "INSERT INTO AbonnementAnnuel (numAbo, typeAbonnement) VALUES (%s, %s)"
        valeurs = (un_abonnement_annuel.get_numAbo(), un_abonnement_annuel.get_typeAbonnement())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            # print(sql)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de abonnement_annuel : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_abonnement_annuel(self, un_abonnement_annuel):
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

    # def find_abonnement_annuel(self, id_vin, id_buveur):
    #     sql = "SELECT * FROM abonnement_annuel WHERE idVin = %s AND buveurId = %s"
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
    #         print(f"Erreur lors de la recherche de abonnement_annuel : {e}")
    #         print(sql)
    #         print(valeurs)
    #         return None
    #     finally:
    #         if cursor:
    #             cursor.close()

    def update_abonnement_annuel(self, un_abonnement_annuel):
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

    # def select_abonnement_annuel(self, un_abonnement_annuel):
    #     les_abonnements_annuels = []
    #     sql = "SELECT * FROM AbonnementAnnuel WHERE "
    #     critere_id_vin = un_abonnement_annuel.get_idVin()
    #     critere_id_buveur = un_abonnement_annuel.get_idBuveur()
    #     critere_qte = un_abonnement_annuel.get_qte()
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
    #         sql = "SELECT * FROM abonnement_annuel"

    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor(dictionary=True)
    #         cursor.execute(sql, tuple(valeurs))
    #         rs = cursor.fetchall()
    #         for row in rs:
    #             les_abonnements_annuels.append(self.set_all_values(row))
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la recherche de abonnement_annuel : {e}")
    #         print(sql)
    #         print(valeurs)
    #     finally:
    #         if cursor:
    #             cursor.close()
    #     return les_abonnements_annuels

    def set_all_values(self, rs):
        from Composants.abonnement_annuel import AbonnementAnnuel
        un_abonnement_annuel = AbonnementAnnuel(rs["numAbo"], rs["typeAbonnement"])
        return un_abonnement_annuel