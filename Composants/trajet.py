class Trajet:
    def __init__(self, ref, stationDepart, stationArrivee, nbKmParcouru,
                 dateArrivee, dateRetour, heureArrivee, heureRetour, refVlauveur):
        self.ref = ref
        self.stationDepart = stationDepart
        self.stationArrivee = stationArrivee
        self.nbKmParcouru = nbKmParcouru
        self.dateArrivee = dateArrivee
        self.dateRetour = dateRetour
        self.heureArrivee = heureArrivee
        self.heureRetour = heureRetour
        self.refVlauveur = refVlauveur

    # Contraintes :
        # Station de départ et d’arrivée obligatoires
        if stationDepart is None or stationArrivee is None:
            print("Erreur : un trajet doit avoir une station de départ et une station d’arrivée. Affectation par défaut à -1.")
            self.stationDepart = -1
            self.stationArrivee = -1
        else:
            self.stationDepart = stationDepart
            self.stationArrivee = stationArrivee

    def __str__(self):
        return f"Trajet #{self.ref} - {self.nbKmParcouru}km - De Station {self.stationDepart} à {self.stationArrivee} - Vlauveur #{self.refVlauveur}"