from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOVlauve:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOVlauve.unique_instance is None:
            DAOVlauve.unique_instance = DAOVlauve()
        return DAOVlauve.unique_instance

    def update_statut_vlauve(self, ref_vlauve, nouveau_statut):
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
        return self.update_statut_vlauve(ref_vlauve, "occupé")