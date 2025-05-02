from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOPaiement:
    nique_instance = None

    @staticmethod
    def get_instance():
        if DAOPaiement.unique_instance is None:
            DAOPaiement.unique_instance = DAOPaiement()
        return DAOPaiement.unique_instance

    def enregistrer_paiement(self, numFacture, montant, moyenPaiement):
        sql = """
            INSERT INTO Paiement (numFacture, montant, datePaiement, moyenPaiement)
            VALUES (%s, %s, NOW(), %s)
        """
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, (numFacture, montant, moyenPaiement))

            # Mise à jour du statut de la facture
            cursor.execute(
                "UPDATE Facture SET statut = 'payee' WHERE numFacture = %s",
                (numFacture,)
            )

            connection.commit()
            return True
        except Error as e:
            print(f"Erreur lors de l'enregistrement du paiement : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
