class AbonnementAnnuel:
    def __init__(self, numAbo, typeAbonnement):
        self.numAbo = numAbo  # lien avec Abonnement
        self.typeAbonnement = typeAbonnement  # 'classique' ou 'tarifReduit'

    def __str__(self):
        return f"AbonnementAnnuel #{self.numAbo} - Type : {self.typeAbonnement}"