from Composants.vlauve import Vlauve
class Station :
    
    def __init__(self, numStation, nom, coordonneesGPS, nomRue, numeroRue,
                 nbPlacesTotal, nbPlacesElectriques, nbPlacesNonElectriques,
                 nbVlauvesElectriques, nbVlauvesNonElectriques, numReseau):
        self.numStation = numStation
        self.nom = nom
        self.coordonneesGPS = coordonneesGPS
        self.nomRue = nomRue
        self.numeroRue = numeroRue
        self.adresse = f"{numeroRue} {nomRue}"
        self.nbPlacesTotal = nbPlacesTotal
        self.nbPlacesElectriques = nbPlacesElectriques
        self.nbPlacesNonElectriques = nbPlacesNonElectriques
        self.nbVlauvesElectriques = nbVlauvesElectriques
        self.nbVlauvesNonElectriques = nbVlauvesNonElectriques
        self.vlauvesDispo = []
        self.numReseau = numReseau  # clé étrangère vers Reseau      
        
    def __str__(self):
        return f"Station #{self.numStation} - {self.nom} ({self.adresse}) - Total places : {self.nbPlacesTotal} - Réseau : {self.numReseau}"
    
    def ajouter_vlauve(self,v):
        self.vlauvesDispo.append(v)
    
    def afficher_vlauves_disponibles(self):
        return [v for v in self.vlauvesDispo]
    
    def louer_vlauve(self,v):
        self.vlauvesDispo.remove(v)
    
    #Pas de différence entre ajoutervlauve et rendrevlauve
    def rendre_vlauve(self,v):
        self.ajouter_vlauve(v)
    
    def repartition(self):
        compteurElectrique = 0
        compteurNElectrique = 0
        for v in self.vlauvesDispo:
            if v.discriminant == "vlauveElectrique":
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