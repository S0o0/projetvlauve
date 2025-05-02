from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOTrajet:
    # Singleton : garantit une instance unique du DAO pour les trajets
    unique_instance = None

    @staticmethod
    def get_instance():
        # Retourne l'instance unique, ou la crée si elle n'existe pas encore
        if DAOTrajet.unique_instance is None:
            DAOTrajet.unique_instance = DAOTrajet()
        return DAOTrajet.unique_instance

    def insert_trajet(self, trajet):
        # Insère un nouveau trajet dans la base de données
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
            connection.commit()  # Valide l'insertion
            return True
        except Error as e:
            print(f"Erreur lors de l'insertion du trajet : {e}")
            connection.rollback()  # Annule l'opération en cas d'erreur
            return False
        finally:
            if cursor:
                cursor.close()  # Ferme le curseur proprement

    def get_trajets_by_vlauveur(self, ref_vlauveur, date_min=None, date_max=None, distance_min=None, distance_max=None):
        # Récupère tous les trajets associés à un vlauveur donné, avec filtres facultatifs :
        # - par date minimale et maximale
        # - par distance minimale et maximale
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
            cursor.execute(sql, tuple(valeurs))  # Exécute la requête avec tous les filtres appliqués
            return cursor.fetchall()  # Retourne la liste des trajets sous forme de dictionnaires
        except Error as e:
            print(f"Erreur lors de la récupération des trajets : {e}")
            return []  # Retourne une liste vide en cas d'erreur
        finally:
            if cursor:
                cursor.close()