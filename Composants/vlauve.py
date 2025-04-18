class Vlauve:

    STATUTS_AUTORISES = ["disponible", "enCirculation", "enReparation", "enPanne", "perdu", "nonDisponible"]

    def __init__(self, ref, assistance, statut, dateCirculation,
                 nbKmParcouru, niveauBatterie, discriminant, refStation):
        self.ref = ref
        self.assistance = assistance  # bool
        self.statut = statut  # string dans ENUM SQL
        self.dateCirculation = dateCirculation
        self.nbKmParcouru = nbKmParcouru
        self.niveauBatterie = niveauBatterie
        self.discriminant = discriminant  # string
        self.refStation = refStation  # clé étrangère vers Station

    # Contraintes :
        # refStation pointe vers une seule Station
        if isinstance(refStation, int):
            self.refStation = refStation
        else:
            print("Erreur : Un vélo ne peut être rattaché qu’à une seule station. Par défaut, refStation mis à -1.")
            self.refStation = -1

        # Statut autorisé
        if statut not in Vlauve.STATUTS_AUTORISES:
            print(f"Statut '{statut}' incorrect. Par défaut, mis à 'nonDisponible'.")
            self.statut = "nonDisponible"
        else:
            self.statut = statut

        # Cohérence discriminant avec assistance
        if self.discriminant == "vLauveElectrique" and not self.assistance:
            print("Un vlauve électrique doit avoir l’assistance activée.")
            self.assistance = True
        elif self.discriminant == "vlauveNonElectrique" and self.assistance:
            print("Un vlauve non électrique ne peut pas avoir d’assistance. Correction automatique.")
            self.assistance = False

        # Niveau batterie
        if self.discriminant == "vLauveElectrique" and self.niveauBatterie < 50:
            print("Niveau batterie insuffisant (< 50%). Statut : 'nonDisponible'.")
            self.statut = "nonDisponible"

    def __str__(self):
        return f"Vlauve ref#{self.ref} - {'Électrique' if self.assistance else 'Classique'} - Statut : {self.statut} - Km : {self.nbKmParcouru}"