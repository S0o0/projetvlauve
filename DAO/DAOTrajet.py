from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOTrajet:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOTrajet.unique_instance is None:
            DAOTrajet.unique_instance = DAOTrajet()
        return DAOTrajet.unique_instance

    def insert_trajet(self, un_trajet):
        sql = "INSERT INTO Trajet (stationDepart, stationArrivee, nbKmParcouru, dateArrivee, dateRetour, heureArrivee, heureRetour, refVlauveur) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valeurs = (un_trajet.get_stationDepart(),
                   un_trajet.get_stationArrivee(),
                   un_trajet.get_nbKmParcouru(),
                   un_trajet.get_dateArrivee(),
                   un_trajet.get_dateRetour(),
                   un_trajet.get_heureArrivee(),
                   un_trajet.get_heureRetour(),
                   un_trajet.get_refVlauveur()
                   )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de trajet : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_trajet(self, un_trajet):
        sql = "DELETE FROM trajet WHERE idTrajet = %s"
        valeurs = (un_trajet.get_ref(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de trajet : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_trajet(self, id_trajet):
        sql = "SELECT * FROM trajet WHERE idTrajet = %s"
        valeurs = (id_trajet,)
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
            print(f"Erreur lors de la recherche d'un trajet : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_trajet(self, un_trajet):
        sql = """
        UPDATE trajet
        SET stationDepart = %s, stationArrivee = %s, nbKmParcouru = %s,
            dateArrivee = %s, dateRetour = %s, heureArrivee = %s, heureRetour = %s, refVlauveur = %s
        WHERE idTrajet = %s
        """
        valeurs = (
            un_trajet.get_stationDepart(),
            un_trajet.get_stationArrivee(),
            un_trajet.get_nbKmParcouru(),
            un_trajet.get_dateArrivee(),
            un_trajet.get_dateRetour(),
            un_trajet.get_heureArrivee(),
            un_trajet.get_heureRetour(),
            un_trajet.get_refVlauveur(),
            un_trajet.get_ref()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de trajet : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_trajet(self, un_trajet):
        les_trajets = []
        sql = "SELECT * FROM trajet WHERE "
        critere_ref = un_trajet.get_ref()
        valeurs = []

        if critere_ref is not None:
            sql += "idTrajet = %s"
            valeurs.append(critere_ref)
        else:
            sql = "SELECT * FROM trajet"

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_trajets.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de trajet : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_trajets

    def set_all_values(self, rs):
        from domaine.Trajet import Trajet  # Attention au bon chemin de ton import
        un_trajet = Trajet(
            rs["idTrajet"],
            rs["stationDepart"],
            rs["stationArrivee"],
            rs["nbKmParcouru"],
            rs["dateArrivee"],
            rs["dateRetour"],
            rs["heureArrivee"],
            rs["heureRetour"],
            rs["refVlauveur"]
        )
        return un_trajet