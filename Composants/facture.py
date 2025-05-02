class Facture:
    # Constructeur de la classe Facture
    # Paramètres :
    # - numero : identifiant unique de la facture
    # - dateFacture : date d'émission de la facture
    # - montantTotal : montant total à payer (en euros)
    # - refAbo : référence vers l'abonnement concerné (clé étrangère)
    def __init__(self, numero, dateFacture, montantTotal, refAbo):
        self.numero = numero
        self.dateFacture = dateFacture
        self.montantTotal = montantTotal
        self.refAbo = refAbo  # clé étrangère vers Abonnement

        # Contrôle de validité : une facture doit être liée à un abonnement
        if refAbo is None:
            print("Erreur : une facture doit être associée à un abonnement. Affectation par défaut à -1.")
            self.refAbo = -1
        else:
            self.refAbo = refAbo

    # Représentation textuelle de la facture
    # Affiche les détails de la facture de manière lisible
    def __str__(self):
        return f"Facture #{self.numero} - Montant : {self.montantTotal}€ - Date : {self.dateFacture} - Abonnement : {self.refAbo}"

    # Accesseur (getter) pour l'attribut numero
    def get_numero(self):
        return self.numero

    # Mutateur (setter) pour l'attribut numero
    def set_numero(self, numero):
        self.numero = numero

    # Getter pour la date de la facture
    def get_dateFacture(self):
        return self.dateFacture

    # Setter pour la date de la facture
    def set_dateFacture(self, dateFacture):
        self.dateFacture = dateFacture

    # Getter pour le montant total
    def get_montantTotal(self):
        return self.montantTotal

    # Setter pour le montant total
    def set_montantTotal(self, montantTotal):
        self.montantTotal = montantTotal

    # Getter pour la référence à l'abonnement
    def get_refAbo(self):
        return self.refAbo

    # Setter pour la référence à l'abonnement
    # Si refAbo est None, on affecte -1 comme valeur par défaut et affiche un message d'erreur
    def set_refAbo(self, refAbo):
        if refAbo is None:
            print("Erreur : une facture doit être associée à un abonnement. Affectation par défaut à -1.")
            self.refAbo = -1
        else:
            self.refAbo = refAbo
