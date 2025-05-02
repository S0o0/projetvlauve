from mysql.connector import Error
from DAO.DAOSession import DAOSession
from Composants.facture import Facture

class DAOFacture:
    # Singleton pour garantir une seule instance DAOFacture dans l'application
    unique_instance = None

    @staticmethod
    def get_instance():
        # Retourne l'unique instance de DAOFacture, la crée si nécessaire
        if DAOFacture.unique_instance is None:
            DAOFacture.unique_instance = DAOFacture()
        return DAOFacture.unique_instance

    def insert_facture(self, un_facture):
        # Insère une facture dans la base de données
        sql = "INSERT INTO Facture (dateFacture, montantTotal, refAbo) VALUES (%s, %s, %s)"
        valeurs = (
            un_facture.get_dateFacture(),
            un_facture.get_montantTotal(),
            un_facture.get_refAbo()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle  # Retourne l'ID de la facture insérée
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de facture : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_facture(self, un_facture):
        # Supprime une facture identifiée par son ID
        sql = "DELETE FROM Facture WHERE idFacture = %s"
        valeurs = (un_facture.get_numero(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de facture : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_facture(self, id_facture):
        # Recherche une facture par son identifiant
        sql = "SELECT * FROM Facture WHERE idFacture = %s"
        valeurs = (id_facture,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            else:
                return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'une facture : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_facture(self, un_facture):
        # Met à jour les champs d'une facture existante
        sql = """
        UPDATE Facture
        SET dateFacture = %s, montantTotal = %s, refAbo = %s
        WHERE idFacture = %s
        """
        valeurs = (
            un_facture.get_dateFacture(),
            un_facture.get_montantTotal(),
            un_facture.get_refAbo(),
            un_facture.get_numero()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de facture : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_facture(self, un_facture):
        # Récupère une ou plusieurs factures selon les critères fournis
        les_factures = []
        sql = "SELECT * FROM Facture WHERE "
        critere_ref = un_facture.get_numero()
        valeurs = []

        if critere_ref is not None:
            sql += "idFacture = %s"
            valeurs.append(critere_ref)
        else:
            sql = "SELECT * FROM Facture"

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_factures.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de facture : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_factures

    def set_all_values(self, rs):
        # Convertit une ligne de résultat SQL en objet Facture
        return Facture(
            rs["idFacture"],
            rs["dateFacture"],
            rs["montantTotal"],
            rs["refAbo"]
        )

    def generer_facture_mensuelle(self, refVlauveur, mois, annee):
        # Calcule et insère une facture mensuelle basée sur les trajets effectués
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            sql_trajets = """
                SELECT nbKmParcouru FROM Trajet
                WHERE refVlauveur = %s AND MONTH(dateArrivee) = %s AND YEAR(dateArrivee) = %s
            """
            cursor.execute(sql_trajets, (refVlauveur, mois, annee))
            trajets = cursor.fetchall()
            total_km = sum([t['nbKmParcouru'] for t in trajets])
            montant = total_km * 0.5  # Exemple de tarif au km

            sql_insert_facture = """
                INSERT INTO Facture (refVlauveur, montantTotal, mois, annee, statut)
                VALUES (%s, %s, %s, %s, 'non payee')
            """
            cursor.execute(sql_insert_facture, (refVlauveur, montant, mois, annee))
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erreur lors de la génération de la facture : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()