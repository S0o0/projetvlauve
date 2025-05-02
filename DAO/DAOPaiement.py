from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOPaiement:
    # Singleton pour s'assurer qu'une seule instance DAO est utilisée
    unique_instance = None  # correction du nom de l'attribut (était 'nique_instance')

    @staticmethod
    def get_instance():
        # Retourne l'instance unique ou la crée si elle n'existe pas encore
        if DAOPaiement.unique_instance is None:
            DAOPaiement.unique_instance = DAOPaiement()
        return DAOPaiement.unique_instance

    def enregistrer_paiement(self, numFacture, montant, moyenPaiement):
        # Enregistre un nouveau paiement dans la base de données
        # et met à jour le statut de la facture associée comme "payée"
        sql = """
            INSERT INTO Paiement (numFacture, montant, datePaiement, moyenPaiement)
            VALUES (%s, %s, NOW(), %s)
        """
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()

            # Exécute la requête d'insertion du paiement
            cursor.execute(sql, (numFacture, montant, moyenPaiement))

            # Met à jour le statut de la facture à "payée"
            cursor.execute(
                "UPDATE Facture SET statut = 'payee' WHERE numFacture = %s",
                (numFacture,)
            )

            # Valide les changements dans la base
            connection.commit()
            return True
        except Error as e:
            # Affiche l'erreur et annule les opérations si une erreur survient
            print(f"Erreur lors de l'enregistrement du paiement : {e}")
            connection.rollback()
            return False
        finally:
            # Ferme le curseur même en cas d'erreur
            if cursor:
                cursor.close()
