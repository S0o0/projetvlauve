from Composants.vlauve import Vlauve

class Station:
    # Constructeur de la classe Station
    # Paramètres :
    # - numStation : identifiant unique de la station
    # - nom : nom de la station
    # - coordonneesGPS : localisation GPS de la station
    # - nomRue, numeroRue : composantes de l'adresse
    # - nbPlacesTotal : nombre total de places disponibles dans la station
    # - nbPlacesElectriques : nombre de places pour vlauves électriques
    # - nbPlacesNonElectriques : nombre de places pour vlauves non électriques
    # - nbVlauvesElectriques, nbVlauvesNonElectriques : compte des vlauves par type
    # - numReseau : identifiant du réseau auquel appartient la station (clé étrangère)
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
        self.vlauvesDispo = []  # liste des vlauves actuellement disponibles
        self.numReseau = numReseau  # identifiant du réseau (clé étrangère vers Reseau)      

    # Méthode spéciale d'affichage d'une station
    def __str__(self):
        return f"Station #{self.numStation} - {self.nom} ({self.adresse}) - Total places : {self.nbPlacesTotal} - Réseau : {self.numReseau}"

    # Ajoute un vlauve à la liste des vlauves disponibles dans la station
    def ajouter_vlauve(self, v):
        self.vlauvesDispo.append(v)

    # Retourne la liste des vlauves actuellement disponibles
    def afficher_vlauves_disponibles(self):
        return [v for v in self.vlauvesDispo]

    # Retire un vlauve de la station lors d'une location
    def louer_vlauve(self, v):
        self.vlauvesDispo.remove(v)

    # Récupère un vlauve après retour à la station (même effet que ajouter_vlauve)
    def rendre_vlauve(self, v):
        self.ajouter_vlauve(v)

    # Calcule et retourne la répartition des vlauves disponibles en pourcentage
    def repartition(self):
        compteurElectrique = 0
        compteurNElectrique = 0
        for v in self.vlauvesDispo:
            if v.discriminant == "vlauveElectrique":
                compteurElectrique += 1
            else:
                compteurNElectrique += 1
        return f'Proporition de vélos électriques : {compteurElectrique / len(self.vlauvesDispo) * 100}%\n' \
               f'Proporition de vélos non électriques : {compteurNElectrique / len(self.vlauvesDispo) * 100}%'