class Facture:
    def __init__(self, numero, dateFacture, montantTotal, refAbo):
        self.numero = numero
        self.dateFacture = dateFacture
        self.montantTotal = montantTotal
        self.refAbo = refAbo  # clé étrangère vers Abonnement

    # Contraintes : 
        # La facture doit être liée à un abonnement
        if refAbo is None:
            print("Erreur : une facture doit être associée à un abonnement. Affectation par défaut à -1.")
            self.refAbo = -1
        else:
            self.refAbo = refAbo

    def __str__(self):
        return f"Facture #{self.numero} - Montant : {self.montantTotal}€ - Date : {self.dateFacture} - Abonnement : {self.refAbo}"