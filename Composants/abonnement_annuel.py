class AbonnementAnnuel:
    # Constructeur de la classe AbonnementAnnuel.
    # Prend en paramètres :
    # - numAbo : identifiant de l'abonnement (clé étrangère vers la table Abonnement)
    # - typeAbonnement : type de formule ('classique' ou 'tarifReduit')
    def __init__(self, numAbo, typeAbonnement):
        # Initialisation directe des attributs publics (à remplacer par les setters si encapsulation souhaitée)
        self.numAbo = numAbo  # lien vers un abonnement principal
        self.typeAbonnement = typeAbonnement  # 'classique' ou 'tarifReduit'

    # Getter pour l'attribut _numAbo (version encapsulée)
    def get_numAbo(self):
        return self._numAbo

    # Setter pour l'attribut _numAbo
    # Permet de définir l'identifiant de l'abonnement
    def set_numAbo(self, numAbo):
        self._numAbo = numAbo

    # Getter pour le type d'abonnement (encapsulation de l'accès à l'attribut _typeAbonnement)
    def get_typeAbonnement(self):
        return self._typeAbonnement

    # Setter pour définir le type d'abonnement
    # Doit contenir idéalement une vérification de validité ('classique' ou 'tarifReduit')
    def set_typeAbonnement(self, typeAbonnement):
        self._typeAbonnement = typeAbonnement

    # Méthode spéciale permettant d'afficher un abonnement annuel sous forme textuelle
    # Utilisée notamment lors de l'impression ou du debug
    def __str__(self):
        return f"AbonnementAnnuel #{self.numAbo} - Type : {self.typeAbonnement}"