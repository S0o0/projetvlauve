from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOStation:
    uneique_instance = None

    @staticmethod
    def get_instance():
        if DAOStation.uneique_instance is None:
            DAOStation.uneique_instance = DAOStation()
        return DAOStation.uneique_instance

    
    def get_all_stations(self):
        sql = "SELECT * FROM Station;"
        try : 
            connection = DAOSession.get_connexion()  # Récupérer la connexion à la base de données
            cursor = connection.cursor(dictionary=True)  # Utiliser un curseur pour récupérer les résultats sous forme de dictionnaire
            cursor.execute(sql)  # Exécuter la requête SQL
            results = cursor.fetchall()  # Récupérer tous les résultats
            stations = []
            
            for result in results :
                station = self.set_all_values(result)
                stations.append(station)
            return stations
        except Error as e:
            print(f"Erreur lors de la récupération des stations : {e}")
            return []  # Si une erreur survient, retourner une liste vide
        finally:
            if cursor:
                cursor.close()  # Fermer le curseur après utilisation

    # def insert_station(self, une_station):
    #     sql = "INSERT INTO Station (nom, adresse, region) VALUES (%s, %s, %s)"
    #     valeurs = (une_station.get_nom(), une_station.get_adresse(), une_station.get_region())
    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor()
    #         cursor.execute(sql, valeurs)
    #         cle = cursor.lastrowid
    #        # print(sql)
    #         return cle
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la création de station : {e}")
    #         print(sql)
    #         print(valeurs)
    #         print("rollback")
    #         connection.rollback() 
    #         return -1
    #     finally:
    #         if cursor:
    #             cursor.close()
        

    # def delete_station(self, une_station):
    #     sql = "DELETE FROM station WHERE idStation = %s"
    #     valeurs = (une_station.get_idStation(),)
    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor()
    #         cursor.execute(sql, valeurs)
    #         return True
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la suppression de station : {e}")
    #         print(sql)
    #         print(valeurs)
    #         print("rollback")
    #         connection.rollback() 
    #         return False
    #     finally:
    #         if cursor:
    #             cursor.close()

    # def find_station(self, id_station):
    #     sql = "SELECT * FROM Station WHERE idStation = %s"
    #     valeurs = (id_station,)
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
    #         print(f"Erreur lors de la recherche d'une station : {e}")
    #         print(sql)
    #         print(valeurs)
    #         return None
    #     finally:
    #         if cursor:
    #             cursor.close()

    # def update_station(self, une_station):
    #     sql = "UPDATE station SET nom = %s, adresse = %s, region = %s WHERE idStation = %s"
    #     valeurs = (une_station.get_nom(), une_station.get_adresse(), une_station.get_region(), une_station.get_idStation())
    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor()
    #         cursor.execute(sql, valeurs)
    #         return True
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la mise à jour de station : {e}")
    #         print(sql)
    #         print(valeurs)
    #         print("rollback")
    #         connection.rollback() 
    #         return False
    #     finally:
    #         if cursor:
    #             cursor.close()

    # def select_station(self, une_station):
    #     les_stations = []
    #     sql = "SELECT * FROM station WHERE "
    #     critere_id = une_station.get_idStation()
    #     critere_nom = une_station.get_nom()
    #     critere_adresse = une_station.get_adresse()
    #     critere_region = une_station.get_region()
    #     valeurs = []

    #     if critere_id is not None:
    #         sql += "idStation = %s"
    #         valeurs.append(critere_id)
    #     elif critere_nom == None and critere_adresse == None and critere_region == None:
    #         sql = "SELECT * FROM station"
    #     else:
    #         conditions = []
    #         if critere_nom is not None:
    #             conditions.append("nom = %s")
    #             valeurs.append(critere_nom)
    #         if critere_adresse is not None:
    #             conditions.append("adresse = %s")
    #             valeurs.append(critere_adresse)
    #         if critere_region is not None:
    #             conditions.append("region = %s")
    #             valeurs.append(critere_region)
    #         sql += " AND ".join(conditions)

    #     try:
    #         connection = DAOSession.get_connexion()
    #         cursor = connection.cursor(dictionary=True)
    #         cursor.execute(sql, tuple(valeurs))
    #         rs = cursor.fetchall()
    #         for row in rs:
    #             les_stations.append(self.set_all_values(row))
    #     except Error as e:
    #         print("\n<--------------------------------------->")
    #         print(f"Erreur lors de la recherche de station : {e}")
    #         print(sql)
    #         print(valeurs)
    #     finally:
    #         if cursor:
    #             cursor.close()
    #     return les_stations

    def set_all_values(self, rs):
        from Composants.station import Station
        
        une_station = Station(
            rs["numStation"],
            rs["nom"],
            rs["coordonneesGPS"],
            rs["nomRue"],
            rs["numeroRue"],
            rs["nbPlacesTotal"],
            rs["nbPlacesElectriques"],
            rs["nbPlacesNonElectriques"],
            rs["nbVlauvesElectriques"],
            rs["nbVlauvesNonElectriques"],
            rs["numReseau"])
        
        return une_station
