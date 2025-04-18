class Abonnement:
    def __init__(self, numAbo, refVlauveur):
        self.numAbo = numAbo
        self.refVlauveur = refVlauveur

    def __str__(self):
        return f"Abonnement #{self.numAbo} - Lié à Vlauveur #{self.refVlauveur}"