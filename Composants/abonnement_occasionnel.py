class AbonnementOccasionnel:
    def __init__(self, numAbo, duree):
        self.numAbo = numAbo  # lien avec Abonnement
        self.duree = duree  # '1j' ou '7j'

    def get_numAbo(self):
        return self._numAbo

    def set_numAbo(self, numAbo):
        self._numAbo = numAbo

    def get_duree(self):
        return self._duree

    def set_duree(self, duree):
        self._duree = duree
    
    def __str__(self):
        return f"AbonnementOccasionnel #{self.numAbo} - Durée : {self.duree}"