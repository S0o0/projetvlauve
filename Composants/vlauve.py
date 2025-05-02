class Vlauve:
    # Liste des statuts autorisés pour un vlauve (conformément à la définition ENUM dans la base SQL)
    STATUTS_AUTORISES = ["disponible", "enCirculation", "enReparation", "enPanne", "perdu", "nonDisponible"]

    # Constructeur de la classe Vlauve
    # Paramètres :
    # - ref : identifiant unique du vlauve
    # - assistance : booléen indiquant si le vlauve est à assistance électrique
    # - statut : état actuel du vlauve (doit appartenir à STATUTS_AUTORISES)
    # - dateCirculation : date de mise en service du vlauve
    # - nbKmParcouru : nombre total de kilomètres parcourus
    # - niveauBatterie : pourcentage de batterie restante (requis si assistance = True)
    # - discriminant : type de vlauve ('vLauveElectrique' ou 'vlauveNonElectrique')
    # - refStation : identifiant de la station associée (clé étrangère)
    def __init__(self, ref, assistance, statut, dateCirculation,
                 nbKmParcouru, niveauBatterie, discriminant, refStation):
        self.ref = ref
        self.assistance = assistance
        self.statut = statut
        self.dateCirculation = dateCirculation
        self.nbKmParcouru = nbKmParcouru
        self.niveauBatterie = niveauBatterie
        self.discriminant = discriminant
        self.refStation = refStation

        # Vérifie que la station est bien une référence unique (de type entier)
        if isinstance(refStation, int):
            self.refStation = refStation
        else:
            print("Erreur : Un vélo ne peut être rattaché qu’à une seule station. Par défaut, refStation mis à -1.")
            self.refStation = -1

        # Vérifie que le statut est valide (appartient à la liste des statuts autorisés)
        if statut not in Vlauve.STATUTS_AUTORISES:
            print(f"Statut '{statut}' incorrect. Par défaut, mis à 'nonDisponible'.")
            self.statut = "nonDisponible"
        else:
            self.statut = statut

        # Vérifie la cohérence entre le type de vlauve et l’assistance
        if self.discriminant == "vLauveElectrique" and not self.assistance:
            print("Un vlauve électrique doit avoir l’assistance activée.")
            self.assistance = True
        elif self.discriminant == "vlauveNonElectrique" and self.assistance:
            print("Un vlauve non électrique ne peut pas avoir d’assistance. Correction automatique.")
            self.assistance = False

        # Vérifie le niveau de batterie pour les vlauves électriques
        if self.discriminant == "vLauveElectrique" and self.niveauBatterie < 50:
            print("Niveau batterie insuffisant (< 50%). Statut : 'nonDisponible'.")
            self.statut = "nonDisponible"

    # Méthode spéciale pour afficher un vlauve de manière lisible (utile pour le debug ou les logs)
    def __str__(self):
        return f"Vlauve ref#{self.ref} - {'Électrique' if self.assistance else 'Classique'} - Statut : {self.statut} - Km : {self.nbKmParcouru}"