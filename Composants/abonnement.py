class Abonnement:
    def __init__(self, numAbo, refVlauveur):
        self.numAbo = numAbo
        self.refVlauveur = refVlauveur

    def get_numAbo(self):
        return self._numAbo

    def set_numAbo(self, numAbo):
        self._numAbo = numAbo

    def get_refVlauveur(self):
        return self._refVlauveur

    def set_refVlauveur(self, refVlauveur):
        self._refVlauveur = refVlauveur

    
    def __str__(self):
        return f"Abonnement #{self.numAbo} - Lié à Vlauveur #{self.refVlauveur}"
    
    