from mysql.connector import Error
from DAO.DAOSession import DAOSession


class DAOAbonnement:
    # Attribut de classe pour stocker l'instance unique (pattern Singleton)
    unique_instance = None

    @staticmethod
    def get_instance():
        # Retourne l'instance unique de DAOAbonnement, la crée si elle n'existe pas encore
        if DAOAbonnement.unique_instance is None:
            DAOAbonnement.unique_instance = DAOAbonnement()
        return DAOAbonnement.unique_instance

    def insert_abonnement(self, un_abonnement):
        # Insère un nouvel abonnement dans la base
        sql = "INSERT INTO Abonnement (numAbo, refVlauveur) VALUES (%s, %s)"
        valeurs = (un_abonnement.get_numAbo(), un_abonnement.get_refVlauveur())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def ajouter_abonnement_annuel(self, numAbo, typeAbonnement):
        # Ajoute un abonnement annuel : insère d'abord l'entrée dans Abonnement (si absente), puis dans AbonnementAnnuel
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute("INSERT IGNORE INTO Abonnement (numAbo, refVlauveur) VALUES (%s, %s)", (numAbo, numAbo))
            cursor.execute("INSERT INTO AbonnementAnnuel (numAbo, typeAbonnement) VALUES (%s, %s)", (numAbo, typeAbonnement))
            connection.commit()
            return numAbo
        except Error as e:
            print(f"Erreur ajout abonnement annuel : {e}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def ajouter_abonnement_occasionnel(self, numAbo, duree):
        # Ajoute un abonnement occasionnel dans les deux tables concernées
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute("INSERT IGNORE INTO Abonnement (numAbo, refVlauveur) VALUES (%s, %s)", (numAbo, numAbo))
            cursor.execute("INSERT INTO AbonnementOccasionnel (numAbo, duree) VALUES (%s, %s)", (numAbo, duree))
            connection.commit()
            return numAbo
        except Error as e:
            print(f"Erreur ajout abonnement occasionnel : {e}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def delete_abonnement(self, un_abonnement):
        # Supprime un abonnement (et ses liens éventuels dans les tables liées)
        num_abo = un_abonnement.get_numAbo()

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()

            # Supprimer les enregistrements associés
            cursor.execute("DELETE FROM AbonnementAnnuel WHERE numAbo = %s", (num_abo,))
            cursor.execute("DELETE FROM AbonnementOccasionnel WHERE numAbo = %s", (num_abo,))

            # Libérer la clé étrangère refVlauveur
            cursor.execute("UPDATE Abonnement SET refVlauveur = NULL WHERE numAbo = %s", (num_abo,))

            # Supprimer l'abonnement principal
            cursor.execute("DELETE FROM Abonnement WHERE numAbo = %s", (num_abo,))

            connection.commit()
            return True

        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de l'abonnement : {e}")
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_abonnement(self, ref_vlauveur):
        # Recherche un abonnement par la référence vlauveur
        sql_abo = "SELECT numAbo FROM Abonnement WHERE refVlauveur = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(sql_abo, (ref_vlauveur,))
            result = cursor.fetchone()
            if not result:
                return None

            numAbo = result["numAbo"]

            # Vérifie si c’est un abonnement annuel
            sql_annuel = "SELECT typeAbonnement FROM AbonnementAnnuel WHERE numAbo = %s"
            cursor.execute(sql_annuel, (numAbo,))
            rs_annuel = cursor.fetchone()
            if rs_annuel:
                return {
                    "numAbo": numAbo,
                    "type": "annuel",
                    "typeAbonnement": rs_annuel["typeAbonnement"]
                }

            # Vérifie si c’est un abonnement occasionnel
            sql_occasionnel = "SELECT duree FROM AbonnementOccasionnel WHERE numAbo = %s"
            cursor.execute(sql_occasionnel, (numAbo,))
            rs_occ = cursor.fetchone()
            if rs_occ:
                return {
                    "numAbo": numAbo,
                    "type": "occasionnel",
                    "duree": rs_occ["duree"]
                }

            return {
                "numAbo": numAbo,
                "type": "inconnu"
            }

        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'abonnement : {e}")
            print(sql_abo)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_abonnement(self, un_abonnement):
        # Met à jour le champ refVlauveur d'un abonnement existant
        sql = "UPDATE Abonnement SET refVlauveur = %s WHERE numAbo = %s"
        valeurs = (un_abonnement.get_refVlauveur(), un_abonnement.get_numAbo())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def modifier_abonnement_annuel(self, num_abo, nouveau_type):
        # Met à jour le type d’un abonnement annuel
        sql = "UPDATE AbonnementAnnuel SET typeAbonnement = %s WHERE numAbo = %s"
        valeurs = (nouveau_type, num_abo)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur modification abonnement annuel : {e}")
            print(sql, valeurs)
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def modifier_abonnement_occasionnel(self, num_abo, nouvelle_duree):
        # Met à jour la durée d’un abonnement occasionnel
        sql = "UPDATE AbonnementOccasionnel SET duree = %s WHERE numAbo = %s"
        valeurs = (nouvelle_duree, num_abo)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur modification abonnement occasionnel : {e}")
            print(sql, valeurs)
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def set_all_values(self, rs):
        # Construit un objet Abonnement à partir d’un dictionnaire de résultats SQL
        from Composants.abonnement import Abonnement
        un_abonnement = Abonnement(rs["numAbo"], rs["refVlauveur"])
        return un_abonnement