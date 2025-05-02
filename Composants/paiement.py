class Paiement:
    # Constructeur de la classe Paiement
    # Paramètres :
    # - numeroPaiement : identifiant unique du paiement
    # - datePaiement : date à laquelle le paiement a été effectué
    # - montant : montant payé
    # - numeroFacture : identifiant de la facture à laquelle ce paiement est associé
    def __init__(self, numeroPaiement, datePaiement, montant, numeroFacture):
        self.numeroPaiement = numeroPaiement  # identifiant du paiement
        self.datePaiement = datePaiement      # date du paiement

        # Contrôle de validité du montant :
        # si le montant est négatif, le corrige à 0 et signale une erreur
        if montant < 0:
            print("Erreur : le montant d’un paiement ne peut pas être négatif. Correction automatique à 0.")
            self.montant = 0
        else:
            self.montant = montant

        # Le paiement doit impérativement être associé à une facture
        # Si aucun identifiant de facture n'est fourni, on assigne -1 et affiche un message d'erreur
        if numeroFacture is None:
            print("Erreur : un paiement doit être associé à une facture. Affectation par défaut à -1.")
            self.numeroFacture = -1
        else:
            self.numeroFacture = numeroFacture

    # Méthode spéciale pour afficher un paiement sous forme de chaîne lisible
    def __str__(self):
        return f"Paiement #{self.numeroPaiement} - Montant : {self.montant}€ - Le {self.datePaiement} - Pour facture #{self.numeroFacture}"