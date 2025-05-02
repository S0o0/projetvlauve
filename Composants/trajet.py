class Trajet:
    # Constructeur de la classe Trajet
    # Paramètres :
    # - ref : identifiant unique du trajet
    # - stationDepart : station de départ (obligatoire)
    # - stationArrivee : station d'arrivée (obligatoire)
    # - nbKmParcouru : distance parcourue en kilomètres
    # - dateArrivee, dateRetour : dates du début et de la fin du trajet
    # - heureArrivee, heureRetour : heures associées aux dates ci-dessus
    # - refVlauveur : identifiant du vlauveur qui a effectué le trajet
    def __init__(self, ref, stationDepart, stationArrivee, nbKmParcouru,
                 dateArrivee, dateRetour, heureArrivee, heureRetour, refVlauveur):
        self.ref = ref
        self.nbKmParcouru = nbKmParcouru
        self.dateArrivee = dateArrivee
        self.dateRetour = dateRetour
        self.heureArrivee = heureArrivee
        self.heureRetour = heureRetour
        self.refVlauveur = refVlauveur

        # Contraintes : station de départ et d’arrivée sont obligatoires
        if stationDepart is None or stationArrivee is None:
            print("Erreur : un trajet doit avoir une station de départ et une station d’arrivée. Affectation par défaut à -1.")
            self.stationDepart = -1
            self.stationArrivee = -1
        else:
            self.stationDepart = stationDepart
            self.stationArrivee = stationArrivee

    # Représentation textuelle du trajet
    def __str__(self):
        return f"Trajet #{self.ref} - {self.nbKmParcouru}km - De Station {self.stationDepart} à {self.stationArrivee} - Vlauveur #{self.refVlauveur}"

    # Accesseurs (getters) et mutateurs (setters) pour chaque attribut

    def get_ref(self):
        return self.ref

    def set_ref(self, ref):
        self.ref = ref

    def get_stationDepart(self):
        return self.stationDepart

    def set_stationDepart(self, stationDepart):
        if stationDepart is not None:
            self.stationDepart = stationDepart
        else:
            print("Erreur : station de départ obligatoire.")
            self.stationDepart = -1

    def get_stationArrivee(self):
        return self.stationArrivee

    def set_stationArrivee(self, stationArrivee):
        if stationArrivee is not None:
            self.stationArrivee = stationArrivee
        else:
            print("Erreur : station d'arrivée obligatoire.")
            self.stationArrivee = -1

    def get_nbKmParcouru(self):
        return self.nbKmParcouru

    def set_nbKmParcouru(self, nbKmParcouru):
        self.nbKmParcouru = nbKmParcouru

    def get_dateArrivee(self):
        return self.dateArrivee

    def set_dateArrivee(self, dateArrivee):
        self.dateArrivee = dateArrivee

    def get_dateRetour(self):
        return self.dateRetour

    def set_dateRetour(self, dateRetour):
        self.dateRetour = dateRetour

    def get_heureArrivee(self):
        return self.heureArrivee

    def set_heureArrivee(self, heureArrivee):
        self.heureArrivee = heureArrivee

    def get_heureRetour(self):
        return self.heureRetour

    def set_heureRetour(self, heureRetour):
        self.heureRetour = heureRetour

    def get_refVlauveur(self):
        return self.refVlauveur

    def set_refVlauveur(self, refVlauveur):
        self.refVlauveur = refVlauveur