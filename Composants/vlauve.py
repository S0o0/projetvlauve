class Vlauve :
    def __init__(self, ref, electrique, statut, date_circulation,
                 nb_km_parcouru, niveau_batterie, Station):
        self.ref = ref
        self.assistance = electrique  # correspond à la colonne SQL 'assistance'
        self.discriminant = "vLauve_electrique" if electrique else "vlauve_non_electrique"
        self.statut = statut
        self.date_circulation = date_circulation
        self.nb_km_parcouru = nb_km_parcouru
        self.Station = Station
    
    def __str__(self):
        return f"{self.ref},{self.electrique},{self.Station.nom}"