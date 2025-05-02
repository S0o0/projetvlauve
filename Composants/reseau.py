import csv  # Module utilisé pour écrire dans des fichiers CSV

class Reseau:
    # Liste de classe servant à stocker les données de tous les réseaux créés
    data = []

    # Constructeur de la classe Reseau
    # Paramètres :
    # - numReseau : identifiant unique du réseau
    # - nomReseau : nom du réseau
    # - anneeMiseEnPlace : année d’installation du réseau
    # - nomVille : ville dans laquelle le réseau est déployé
    # - codePostal : code postal de la ville
    def __init__(self, numReseau, nomReseau, anneeMiseEnPlace, nomVille, codePostal):
        self.numReseau = numReseau
        self.nomReseau = nomReseau
        self.anneeMiseEnPlace = anneeMiseEnPlace
        self.nomVille = nomVille
        self.codePostal = codePostal
        self.stations = []  # Liste des stations associées à ce réseau

        # Ajoute les informations du réseau dans la liste statique `data` pour un usage commun (ex : export CSV)
        Reseau.data.append([self.numReseau, self.nomReseau, self.anneeMiseEnPlace, self.nomVille, self.codePostal])

    # Méthode spéciale pour représenter un réseau sous forme de chaîne lisible
    def __str__(self):
        return f"Réseau #{self.numReseau} - {self.nomReseau} ({self.nomVille}, {self.codePostal}) - Mis en place en {self.anneeMiseEnPlace}"

    # Ajoute une station à la liste des stations du réseau
    def ajouterStation(self, s):
        self.stations.append(s)

    # Affiche la liste des stations du réseau en version texte
    def afficher_stations(self):
        print([str(s) for s in self.stations])

    # Méthode de classe pour exporter les données de tous les réseaux en fichier CSV
    @classmethod
    def csv(cls):
        header = ['numero', 'nom', 'annee', 'nomVille', 'code_postal']
        with open('reseau.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)      # écrit l’en-tête
            writer.writerows(cls.data)   # écrit chaque ligne de données collectée dans cls.data