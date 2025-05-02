from mysql.connector import Error
from DAO.DAOSession import DAOSession
from Composants.facture import Facture

class DAOFacture:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOFacture.unique_instance is None:
            DAOFacture.unique_instance = DAOFacture()
        return DAOFacture.unique_instance

    def insert_facture(self, un_facture):
        sql = "INSERT INTO Facture (dateFacture, montantTotal, refAbo) VALUES (%s, %s, %s)"
        valeurs = (un_facture.get_stationDepart(),
                   un_facture.get_stationArrivee(),
                   un_facture.get_nbKmParcouru(),
                   un_facture.get_dateArrivee(),
                   un_facture.get_dateRetour(),
                   un_facture.get_heureArrivee(),
                   un_facture.get_heureRetour(),
                   un_facture.get_refVlauveur()
                   )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
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
        sql = "DELETE FROM facture WHERE idFacture = %s"
        valeurs = (un_facture.get_ref(),)
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
        sql = "SELECT * FROM facture WHERE idFacture = %s"
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
            print(f"Erreur lors de la recherche d'un facture : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_facture(self, un_facture):
        sql = """
        UPDATE facture
        SET stationDepart = %s, stationArrivee = %s, nbKmParcouru = %s,
            dateArrivee = %s, dateRetour = %s, heureArrivee = %s, heureRetour = %s, refVlauveur = %s
        WHERE idFacture = %s
        """
        valeurs = (
            un_facture.get_stationDepart(),
            un_facture.get_stationArrivee(),
            un_facture.get_nbKmParcouru(),
            un_facture.get_dateArrivee(),
            un_facture.get_dateRetour(),
            un_facture.get_heureArrivee(),
            un_facture.get_heureRetour(),
            un_facture.get_refVlauveur(),
            un_facture.get_ref()
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
        les_factures = []
        sql = "SELECT * FROM facture WHERE "
        critere_ref = un_facture.get_ref()
        valeurs = []

        if critere_ref is not None:
            sql += "idFacture = %s"
            valeurs.append(critere_ref)
        else:
            sql = "SELECT * FROM facture"

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
        un_facture = Facture(
            rs["idFacture"],
            rs["stationDepart"],
            rs["stationArrivee"],
            rs["nbKmParcouru"],
            rs["dateArrivee"],
            rs["dateRetour"],
            rs["heureArrivee"],
            rs["heureRetour"],
            rs["refVlauveur"]
        )
        return un_facture
    
        def generer_facture_mensuelle(self, refVlauveur, mois, annee):
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
                montant = total_km * 0.5  # Exemple de tarif

                sql_insert_facture = """
                    INSERT INTO Facture (refVlauveur, montant, mois, annee, statut)
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