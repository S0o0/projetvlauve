from vlauve import vlauve
class Station :
    
    def __init__(self, num_station, nom, coordonneesGPS, nom_rue, numero_rue,
                 capacite_totale, nb_places_electriques, nb_places_non_electriques,
                 nb_vlauves_electriques, nb_vlauves_non_electriques):
        self.num_station = num_station
        self.nom = nom
        self.coordonneesGPS = coordonneesGPS
        self.nom_rue = nom_rue
        self.numero_rue = numero_rue
        self.adresse = f"{numero_rue} {nom_rue}"
        self.capacite_totale = capacite_totale
        self.nb_places_electriques = nb_places_electriques
        self.nb_places_non_electriques = nb_places_non_electriques
        self.nb_vlauves_electriques = nb_vlauves_electriques
        self.nb_vlauves_non_electriques = nb_vlauves_non_electriques
        self.vlauvesDispo = []          
        
    def __str__(self):
        return f"{self.num_station},{self.nom},{self.adresse},{self.capacite_totale},{self.Reseau}"
    
    def ajouter_vlauve(self,v):
        self.vlauvesDispo.append(v)
    
    def afficher_vlauves_disponibles(self):
        print([str(v) for v in self.vlauvesDispo])
    
    def louer_vlauve(self,v):
        self.vlauvesDispo.remove(v)
    
    #Pas de différence entre ajoutervlauve et rendrevlauve
    def rendre_vlauve(self,v):
        self.ajoutervlauve(v)
    
    def repartition(self):
        compteurElectrique = 0
        compteurNElectrique = 0
        for v in self.vlauvesDispo:
            if v.electrique:
                compteurElectrique += 1
            else:
                compteurNElectrique += 1
        return f'Proporition de vélos électriques : {compteurElectrique/len(self.vlauvesDispo)* 100}%\n'\
                f'Proporition de vélos non électriques : {compteurNElectrique/len(self.vlauvesDispo)*100}%'

# reseau = Reseau(1,"Stan",2005)
# ville = Ville(54000,"Nancy",reseau)
# reseau.ajouterVille(ville)
# stat1 = Station(1,"heho","azmkljqsd",100,reseau)
# stat2 = Station(2,"mazlek","azqlsd",124,reseau)
# reseau.ajouterStation(stat1)
# reseau.ajouterStation(stat2)
# vlauve1 = vlauve(1,False,stat1)
# vlauve2 = vlauve(2,True,stat1)
# stat1.ajoutervlauve(vlauve1)
# stat1.ajoutervlauve(vlauve2)

# reseau.afficher_stations()
# stat1.afficher_vlauves_disponibles()
# print(stat1.repartition())
# Reseau.csv()