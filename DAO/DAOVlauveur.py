from mysql.connector import Error
from DAO.DAOSession import DAOSession
import hashlib
import secrets

class DAOVlauveur:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOVlauveur.unique_instance is None:
            DAOVlauveur.unique_instance = DAOVlauveur()
        return DAOVlauveur.unique_instance

    def insert_vlauveur(self, vlauveur):
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            
            salt = secrets.token_hex(16)
            hash_mdp = hashlib.sha256((vlauveur.motDePasse + salt).encode()).hexdigest()
            mot_de_passe_hashe = f"{hash_mdp}/{salt}"
            
            # 1. Insérer le Vlauveur sans spécifier numVlauveur
            sql_vlauveur = """
                INSERT INTO Vlauveur (email, motDePasse, nom, prenom, telephone,
                                    numAdresse, nomRue, codePostal, nomVille, numAbo, numFacture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL)
            """
            valeurs_vlauveur = (
                vlauveur.email,
                mot_de_passe_hashe,
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

            # Récupérer l'ID nouvellement créé
            numVlauveur = cursor.lastrowid
            vlauveur.numVlauveur = numVlauveur  # on le met aussi à jour dans ton objet Python

            # 2. Créer un nouvel abonnement
            cursor.execute("SELECT MAX(numAbo) FROM Abonnement")
            result = cursor.fetchone()
            num_abo = (result[0] or 0) + 1

            cursor.execute(
                "INSERT INTO Abonnement (numAbo, refVlauveur) VALUES (%s, %s)",
                (num_abo, numVlauveur)
            )

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

            # 3. Mise à jour du numAbo dans le Vlauveur
            cursor.execute(
                "UPDATE Vlauveur SET numAbo = %s WHERE numVlauveur = %s",
                (num_abo, numVlauveur)
            )

            connection.commit()
            print("Vlauveur et abonnement insérés et liés avec succès.")
            return numVlauveur

        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de l'insertion du vlauveur : {e}")
            connection.rollback()
            return -1
        finally:
            print("Insertion dans la base du mot de passe :", vlauveur.motDePasse)
            if cursor:
                cursor.close()



    def delete_vlauveur(self, vlauveur):
        sql = "DELETE FROM Vlauveur WHERE numVlauveur = %s"
        valeurs = (vlauveur.get_numVlauveur(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de vlauveur : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
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
        sql = "SELECT * FROM Vlauveur WHERE email = %s"
        cursor = None
        try:
            connection = DAOSession.get_connexion()
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
            if result:
                print(f"Mot de passe récupéré de la base: {result['motDePasse']}")
                try:
                    stored_hash, stored_salt = result["motDePasse"].split("/")
                    print(f"Hash: {stored_hash}, Salt: {stored_salt}")
                except ValueError:
                    print("Format de mot de passe invalide.")
                    return None

                hash_mdp = hashlib.sha256((motDePasse + stored_salt).encode()).hexdigest()
                print(f"Hash calculé pour la vérification : {hash_mdp}")
                print(f"Hash attendu depuis la base : {stored_hash}")
                if hash_mdp == stored_hash:
                    return self.set_all_values(result)  # L'utilisateur est authentifié
                else:
                    print("Mot de passe incorrect.")
                    return None
            else:
                print("Aucun utilisateur trouvé avec cet email.")
                return None
        except Error as e:
            print(f"Erreur lors de la vérification des identifiants : {e}")
            return None
        finally:
            if cursor:
                cursor.close()



    def set_all_values(self, rs):
        from Composants.vlauveur import Vlauveur
        vlauveur = Vlauveur(
            rs["numVlauveur"], rs["email"], rs["motDePasse"],
            rs["nom"], rs["prenom"], rs["telephone"],
            rs["numAdresse"], rs["nomRue"], rs["codePostal"],
            rs["nomVille"], rs["numAbo"]
        )
        # Si tu as des trajets à charger, vérifie aussi leur récupération
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

    
    def get_all_vlauveurs(self):
        sql = "SELECT * FROM Vlauveur"
        try:
            connection = DAOSession.get_connexion()  # Récupérer la connexion à la base de données
            cursor = connection.cursor(dictionary=True)  # Utiliser un curseur pour récupérer les résultats sous forme de dictionnaire
            cursor.execute(sql)  # Exécuter la requête SQL
            results = cursor.fetchall()  # Récupérer tous les résultats
            vlauveurs = []  # Liste pour stocker les objets Vlauveur
            
            # Pour chaque ligne dans les résultats, créer un objet Vlauveur et l'ajouter à la liste
            for result in results:
                vlauveur = self.set_all_values(result)  # Créer un objet Vlauveur à partir des données
                vlauveurs.append(vlauveur)  # Ajouter l'objet à la liste

            return vlauveurs  # Retourner la liste des vlauveurs

        except Error as e:
            print(f"Erreur lors de la récupération des vlauveurs : {e}")
            return []  # Si une erreur survient, retourner une liste vide
        finally:
            if cursor:
                cursor.close()  # Fermer le curseur après utilisation
