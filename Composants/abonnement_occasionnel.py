class AbonnementOccasionnel:
    # Constructeur de la classe AbonnementOccasionnel.
    # Paramètres :
    # - numAbo : identifiant unique de l'abonnement (clé étrangère vers la table Abonnement)
    # - duree : durée de validité de l'abonnement ('1j' pour 1 jour, '7j' pour 7 jours)
    def __init__(self, numAbo, duree):
        # Initialisation directe des attributs publics (devrait utiliser les setters si on applique l'encapsulation)
        self.numAbo = numAbo  # numéro d'abonnement
        self.duree = duree    # durée : '1j' ou '7j'

    # Getter pour l'attribut encapsulé _numAbo
    def get_numAbo(self):
        return self._numAbo

    # Setter pour l'attribut _numAbo
    def set_numAbo(self, numAbo):
        self._numAbo = numAbo

    # Getter pour accéder à la durée d'abonnement
    def get_duree(self):
        return self._duree

    # Setter pour définir la durée d'abonnement
    # On pourrait ici valider que la valeur soit bien '1j' ou '7j'
    def set_duree(self, duree):
        self._duree = duree
    
    # Représentation textuelle de l'objet AbonnementOccasionnel
    # Affiche le numéro d'abonnement et la durée
    def __str__(self):
        return f"AbonnementOccasionnel #{self.numAbo} - Durée : {self.duree}"