class AbonnementAnnuel:
    def __init__(self, numAbo, typeAbonnement):
        self.numAbo = numAbo  # lien avec Abonnement
        self.typeAbonnement = typeAbonnement  # 'classique' ou 'tarifReduit'

    def get_numAbo(self):
        return self._numAbo

    def set_numAbo(self, numAbo):
        self._numAbo = numAbo

    def get_typeAbonnement(self):
        return self._typeAbonnement

    def set_typeAbonnement(self, typeAbonnement):
        self._typeAbonnement = typeAbonnement

    def __str__(self):
        return f"AbonnementAnnuel #{self.numAbo} - Type : {self.typeAbonnement}"