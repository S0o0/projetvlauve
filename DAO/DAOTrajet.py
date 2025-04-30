from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOTrajet:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOTrajet.unique_instance is None:
            DAOTrajet.unique_instance = DAOTrajet()
        return DAOTrajet.unique_instance

    def insert_facture(self, une_facture):
        sql = """
            INSERT INTO Facture (dateFacture, montantTotal, refAbo)
            VALUES (%s, %s, %s)
        """
        valeurs = (
            une_facture.get_dateFacture(),
            une_facture.get_montantTotal(),
            une_facture.get_refAbo()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print(f"Erreur lors de l'insertion de la facture : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_facture(self, une_facture):
        sql = "DELETE FROM Facture WHERE numero = %s"
        valeurs = (une_facture.get_numero(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print(f"Erreur lors de la suppression de la facture : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_facture(self, numero):
        sql = "SELECT * FROM Facture WHERE numero = %s"
        valeurs = (numero,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            return None
        except Error as e:
            print(f"Erreur lors de la recherche de la facture : {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def update_facture(self, une_facture):
        sql = """
            UPDATE Facture SET dateFacture = %s, montantTotal = %s, refAbo = %s
            WHERE numero = %s
        """
        valeurs = (
            une_facture.get_dateFacture(),
            une_facture.get_montantTotal(),
            une_facture.get_refAbo(),
            une_facture.get_numero()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print(f"Erreur lors de la mise à jour de la facture : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_facture(self):
        sql = "SELECT * FROM Facture"
        factures = []
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                factures.append(self.set_all_values(row))
        except Error as e:
            print(f"Erreur lors de la récupération des factures : {e}")
        finally:
            if cursor:
                cursor.close()
        return factures

    def set_all_values(self, rs):
        return Facture(
            numero=rs["numero"],
            dateFacture=rs["dateFacture"],
            montantTotal=rs["montantTotal"],
            refAbo=rs["refAbo"]
        )
        return un_trajet