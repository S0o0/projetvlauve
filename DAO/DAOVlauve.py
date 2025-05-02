from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOVlauve:
    # Singleton : s'assure qu'une seule instance de DAO est utilisée dans tout le programme
    unique_instance = None

    @staticmethod
    def get_instance():
        # Retourne l'instance unique, la crée si elle n'existe pas encore
        if DAOVlauve.unique_instance is None:
            DAOVlauve.unique_instance = DAOVlauve()
        return DAOVlauve.unique_instance

    def update_statut_vlauve(self, ref_vlauve, nouveau_statut):
        # Met à jour le statut (état) d’un vlauve donné
        # Utilisé pour signaler qu’un vlauve est en circulation, en panne, etc.
        sql = "UPDATE Vlauve SET statut = %s WHERE ref = %s"
        valeurs = (nouveau_statut, ref_vlauve)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur lors de la mise à jour du statut du vlauve : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def get_vlauves_by_station(self, num_station):
        # Récupère tous les vlauves disponibles (statut = 'disponible') dans une station donnée
        sql = """
            SELECT ref, statut
            FROM Vlauve
            WHERE refStation = %s AND statut = 'disponible'
        """
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (num_station,))
            resultats = cursor.fetchall()
            return [
                type("Vlauve", (), {
                    "id": row["ref"],
                    "etat": row["statut"]
                })()
                for row in resultats
            ]
        except Error as e:
            print(f"Erreur lors de la récupération des vlauves : {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def mettre_en_circulation(self, ref_vlauve):
        # Méthode utilitaire : change l’état d’un vlauve en "occupé"
        return self.update_statut_vlauve(ref_vlauve, "occupé")