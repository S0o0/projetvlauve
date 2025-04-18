class AbonnementOccasionnel:
    def __init__(self, numAbo, duree):
        self.numAbo = numAbo  # lien avec Abonnement
        self.duree = duree  # '1j' ou '7j'

    def __str__(self):
        return f"AbonnementOccasionnel #{self.numAbo} - Durée : {self.duree}"