from mysql.connector import Error
from DAO.DAOSession import DAOSession
import hashlib
import secrets

class DAOVlauveur:
    # Singleton : une seule instance DAO est partagée dans l'application
    unique_instance = None

    @staticmethod
    def get_instance():
        # Retourne l'instance unique ou la crée si elle n'existe pas
        if DAOVlauveur.unique_instance is None:
            DAOVlauveur.unique_instance = DAOVlauveur()
        return DAOVlauveur.unique_instance

    def insert_vlauveur(self, vlauveur):
        # Insère un nouvel utilisateur (vlauveur) et son abonnement associé
        cursor = None
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()

            # Hash le mot de passe s'il ne l'est pas encore
            if '/' not in vlauveur.motDePasse:
                salt = secrets.token_hex(16)
                hash_mdp = hashlib.sha256((vlauveur.motDePasse + salt).encode()).hexdigest()
                vlauveur.motDePasse = f"{hash_mdp}/{salt}"

            # 1. Insertion du vlauveur sans son ID (clé auto-incrémentée)
            sql_vlauveur = """
                INSERT INTO Vlauveur (email, motDePasse, nom, prenom, telephone,
                                    numAdresse, nomRue, codePostal, nomVille, numAbo, numFacture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL)
            """
            valeurs_vlauveur = (
                vlauveur.email,
                vlauveur.motDePasse,
                vlauveur.nom,
                vlauveur.prenom,
                vlauveur.tel,
                vlauveur.numAdresse,
                vlauveur.nomRue,
                vlauveur.codePostal,
                vlauveur.nomVille
            )
            cursor.execute(sql_vlauveur, valeurs_vlauveur)
            connection.commit()

            # Récupère l'ID généré
            numVlauveur = cursor.lastrowid
            vlauveur.numVlauveur = numVlauveur

            # 2. Création de l'abonnement (numAbo unique)
            cursor.execute("SELECT MAX(numAbo) FROM Abonnement")
            result = cursor.fetchone()
            num_abo = (result[0] or 0) + 1

            # Insère l'abonnement principal
            cursor.execute(
                "INSERT INTO Abonnement (numAbo, refVlauveur) VALUES (%s, %s)",
                (num_abo, numVlauveur)
            )

            # Insère selon le type d'abonnement
            if vlauveur.typeAbo.lower() == "annuel":
                cursor.execute(
                    "INSERT INTO AbonnementAnnuel (numAbo, typeAbonnement) VALUES (%s, %s)",
                    (num_abo, "classique")  # ou "tarifReduit"
                )
            elif vlauveur.typeAbo.lower() == "occasionnel":
                cursor.execute(
                    "INSERT INTO AbonnementOccasionnel (numAbo, duree) VALUES (%s, %s)",
                    (num_abo, "1j")  # ou "7j"
                )
            else:
                raise ValueError("Type d'abonnement invalide.")

            # 3. Mise à jour du champ numAbo dans le Vlauveur
            cursor.execute(
                "UPDATE Vlauveur SET numAbo = %s WHERE numVlauveur = %s",
                (num_abo, numVlauveur)
            )
            connection.commit()
            return numVlauveur

        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de l'insertion du vlauveur : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_vlauveur(self, vlauveur):
        # Supprime un vlauveur par son ID
        sql = "DELETE FROM Vlauveur WHERE numVlauveur = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, (vlauveur.get_numVlauveur(),))
            return True
        except Error as e:
            print(f"Erreur lors de la suppression de vlauveur : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_vlauveur(self, vlauveur):
        # Met à jour les informations d’un vlauveur
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
        # Recherche un vlauveur par son identifiant
        sql = "SELECT * FROM Vlauveur WHERE numVlauveur = %s"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (numVlauveur,))
            result = cursor.fetchone()
            if result:
                return self.set_all_values(result)
            return None
        except Error as e:
            print(f"Erreur lors de la récupération du vlauveur : {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def find_by_credentials(self, email, motDePasse):
        # Authentifie un utilisateur par email + mot de passe
        sql = "SELECT * FROM Vlauveur WHERE email = %s"
        try:
            connection = DAOSession.get_connexion()
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
            if result:
                try:
                    stored_hash, stored_salt = result["motDePasse"].split("/")
                except ValueError:
                    return None
                # Compare le hash recomputé avec celui stocké
                hash_mdp = hashlib.sha256((motDePasse + stored_salt).encode()).hexdigest()
                if hash_mdp == stored_hash:
                    return self.set_all_values(result)
            return None
        except Error as e:
            print(f"Erreur lors de la vérification des identifiants : {e}")
            return None

    def set_all_values(self, rs):
        # Construit un objet Vlauveur + ses trajets
        from Composants.vlauveur import Vlauveur
        from Composants.trajet import Trajet

        vlauveur = Vlauveur(
            rs["numVlauveur"], rs["email"], rs["motDePasse"],
            rs["nom"], rs["prenom"], rs["telephone"],
            rs["numAdresse"], rs["nomRue"], rs["codePostal"],
            rs["nomVille"], rs["numAbo"]
        )
        try:
            cursor = DAOSession.get_connexion().cursor(dictionary=True)
            cursor.execute("SELECT * FROM Trajet WHERE refVlauveur = %s", (rs["numVlauveur"],))
            for t in cursor.fetchall():
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

    def get_all_vlauveurs(self):
        # Récupère tous les vlauveurs depuis la base
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Vlauveur")
            results = cursor.fetchall()
            return [self.set_all_values(r) for r in results]
        except Error as e:
            print(f"Erreur lors de la récupération des vlauveurs : {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def retirer_abonnement(self, ref_vlauveur):
        # Supprime la référence d'abonnement d’un vlauveur (sans le supprimer lui-même)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute("UPDATE Vlauveur SET numAbo = NULL WHERE numVlauveur = %s", (ref_vlauveur,))
            connection.commit()
            return True
        except Error as e:
            print(f"Erreur lors du retrait d'abonnement : {e}")
            return False
        finally:
            if cursor:
                cursor.close()
