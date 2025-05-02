from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOTrajet:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOTrajet.unique_instance is None:
            DAOTrajet.unique_instance = DAOTrajet()
        return DAOTrajet.unique_instance

    def insert_trajet(self, trajet):
        sql = """
            INSERT INTO Trajet (stationDepart, stationArrivee, nbKmParcouru,
                                dateArrivee, dateRetour, heureArrivee, heureRetour, refVlauveur)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valeurs = (
            trajet.stationDepart, trajet.stationArrivee, trajet.nbKmParcouru,
            trajet.dateArrivee, trajet.dateRetour, trajet.heureArrivee, trajet.heureRetour,
            trajet.refVlauveur
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur lors de l'insertion du trajet : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def get_trajets_by_vlauveur(self, ref_vlauveur, date_min=None, date_max=None, distance_min=None, distance_max=None):
        sql = """
            SELECT stationDepart, stationArrivee, nbKmParcouru, 
                   dateArrivee, dateRetour, heureArrivee, heureRetour
            FROM Trajet
            WHERE refVlauveur = %s
        """
        valeurs = [ref_vlauveur]

        if date_min:
            sql += " AND dateArrivee >= %s"
            valeurs.append(date_min)
        if date_max:
            sql += " AND dateArrivee <= %s"
            valeurs.append(date_max)
        if distance_min:
            sql += " AND nbKmParcouru >= %s"
            valeurs.append(distance_min)
        if distance_max:
            sql += " AND nbKmParcouru <= %s"
            valeurs.append(distance_max)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            return cursor.fetchall()
        except Error as e:
            print(f"Erreur lors de la récupération des trajets : {e}")
            return []
        finally:
            if cursor:
                cursor.close()