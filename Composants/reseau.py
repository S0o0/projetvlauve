import csv

class Reseau:
    data = []

    def __init__(self, numReseau, nomReseau, anneeMiseEnPlace, nomVille, codePostal):
        self.numReseau = numReseau
        self.nomReseau = nomReseau
        self.anneeMiseEnPlace = anneeMiseEnPlace
        self.nomVille = nomVille
        self.codePostal = codePostal
        self.stations = []
        Reseau.data.append([self.numReseau, self.nomReseau, self.anneeMiseEnPlace, self.nomVille, self.codePostal])

    def __str__(self):
        return f"Réseau #{self.numReseau} - {self.nomReseau} ({self.nomVille}, {self.codePostal}) - Mis en place en {self.anneeMiseEnPlace}"

    def ajouterStation(self, s):
        self.stations.append(s)

    def afficher_stations(self):
        print([str(s) for s in self.stations])

    @classmethod
    def csv(cls):
        header = ['numero', 'nom', 'annee', 'nomVille', 'code_postal']
        with open('reseau.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(cls.data)