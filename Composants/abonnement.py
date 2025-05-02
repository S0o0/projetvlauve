class Abonnement:
    # Constructeur de la classe Abonnement.
    # Paramètres :
    # - numAbo : identifiant unique de l'abonnement
    # - refVlauveur : identifiant du vlauveur auquel cet abonnement est lié
    def __init__(self, numAbo, refVlauveur):
        self.set_numAbo(numAbo)           # appel du setter pour initialiser _numAbo
        self.set_refVlauveur(refVlauveur) # appel du setter pour initialiser _refVlauveur

    # Getter pour l'attribut _numAbo
    # Retourne le numéro de l'abonnement
    def get_numAbo(self):
        return self._numAbo

    # Setter pour l'attribut _numAbo
    # Permet de définir ou modifier le numéro de l'abonnement
    def set_numAbo(self, numAbo):
        self._numAbo = numAbo

    # Getter pour l'attribut _refVlauveur
    # Retourne la référence du vlauveur associé à cet abonnement
    def get_refVlauveur(self):
        return self._refVlauveur

    # Setter pour l'attribut _refVlauveur
    # Permet de lier l'abonnement à un vlauveur
    def set_refVlauveur(self, refVlauveur):
        self._refVlauveur = refVlauveur

    # Représentation textuelle de l'abonnement
    # Permet un affichage lisible pour le debug ou l'impression
    def __str__(self):
        return f"Abonnement #{self.get_numAbo()} - Lié à Vlauveur #{self.get_refVlauveur()}"