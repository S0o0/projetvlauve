from mysql.connector import Error
from DAO.DAOSession import DAOSession
from Composants.trajet import Trajet
from domaine.Vlauveur import Vlauveur

class DAOVlauveur:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOVlauveur.unique_instance is None:
            DAOVlauveur.unique_instance = DAOVlauveur()
        return DAOVlauveur.unique_instance

    def insert_vlauveur(self, vlauveur):
        sql = """
            INSERT INTO Vlauveur (numVlauveur, email, motDePasse, nom, prenom, telephone,
                                  numAdresse, nomRue, codePostal, nomVille, numAbo, numFacture)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valeurs = (
            vlauveur.numVlauveur, vlauveur.email, vlauveur.motDePasse,
            vlauveur.nom, vlauveur.prenom, vlauveur.tel,
            vlauveur.numAdresse, vlauveur.nomRue,
            vlauveur.codePostal, vlauveur.nomVille,
            vlauveur.typeAbo, None  # numFacture = None à l'insertion
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erreur lors de l'insertion du vlauveur : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_vlauveur(self, numVlauveur):
        sql = "DELETE FROM Vlauveur WHERE numVlauveur = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, (numVlauveur,))
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur lors de la suppression du vlauveur : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_vlauveur(self, vlauveur):
        sql = """
            UPDATE Vlauveur SET email=%s, motDePasse=%s, nom=%s, prenom=%s, telephone=%s,
            numAdresse=%s, nomRue=%s, codePostal=%s, nomVille=%s, numAbo=%s, numFacture=%s
            WHERE numVlauveur = %s
        """
        valeurs = (
            vlauveur.email, vlauveur.motDePasse, vlauveur.nom, vlauveur.prenom, vlauveur.tel,
            vlauveur.numAdresse, vlauveur.nomRue, vlauveur.codePostal, vlauveur.nomVille,
            vlauveur.typeAbo, None,  # numFacture = None ou à gérer
            vlauveur.numVlauveur
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur lors de la mise à jour du vlauveur : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_by_id(self, numVlauveur):
        sql = "SELECT * FROM Vlauveur WHERE numVlauveur = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (numVlauveur,))
            result = cursor.fetchone()
            if result:
                return self.set_all_values(result)
            else:
                return None
        except Error as e:
            print(f"Erreur lors de la récupération du vlauveur : {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def find_by_credentials(self, email, motDePasse):
        sql = "SELECT * FROM Vlauveur WHERE email = %s AND motDePasse = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (email, motDePasse))
            result = cursor.fetchone()
            if result:
                return self.set_all_values(result)
            else:
                return None
        except Error as e:
            print(f"Erreur lors de la vérification des identifiants : {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def set_all_values(self, rs):
        vlauveur = Vlauveur(
            rs["numVlauveur"], rs["email"], rs["motDePasse"],
            rs["nom"], rs["prenom"], rs["telephone"],
            rs["numAdresse"], rs["nomRue"], rs["codePostal"],
            rs["nomVille"], rs["numAbo"]
        )
        # On pourrait ajouter ici la récupération des trajets
        try:
            cursor = DAOSession.get_connexion().cursor(dictionary=True)
            cursor.execute("SELECT * FROM Trajet WHERE refVlauveur = %s", (rs["numVlauveur"],))
            trajets_data = cursor.fetchall()
            for t in trajets_data:
                trajet = Trajet(
                    t['ref'], t['stationDepart'], t['stationArrivee'], t['nbKmParcouru'],
                    t['dateArrivee'], t['dateRetour'], t['heureArrivee'], t['heureRetour'], t['refVlauveur']
                )
                vlauveur.ajouter_trajet(trajet)
        except Error as e:
            print(f"Erreur lors du chargement des trajets du vlauveur : {e}")
        finally:
            if cursor:
                cursor.close()

        return vlauveur