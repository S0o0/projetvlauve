class Paiement:
    def __init__(self, numeroPaiement, datePaiement, montant, numeroFacture):
        self.numeroPaiement = numeroPaiement
        self.datePaiement = datePaiement
        self.montant = montant
        self.numeroFacture = numeroFacture

    # Contraintes :
        # Contrôle du montant
        if montant < 0:
            print("Erreur : le montant d’un paiement ne peut pas être négatif. Correction automatique à 0.")
            self.montant = 0
        else:
            self.montant = montant

        # Le paiement doit être lié à une facture
        if numeroFacture is None:
            print("Erreur : un paiement doit être associé à une facture. Affectation par défaut à -1.")
            self.numeroFacture = -1
        else:
            self.numeroFacture = numeroFacture

    def __str__(self):
        return f"Paiement #{self.numeroPaiement} - Montant : {self.montant}€ - Le {self.datePaiement} - Pour facture #{self.numeroFacture}"