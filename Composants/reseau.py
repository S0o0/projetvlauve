import csv

class Reseau :
    data = []
    def __init__(self,num_reseau,nom_reseau,annee_mise_en_place, nomVille, code_postal):
        self.num_reseau = num_reseau
        self.nom_reseau = nom_reseau
        self.annee_mise_en_place = annee_mise_en_place
        self.nomVille = nomVille
        self.code_postal = code_postal
        self.stations=[]
        Reseau.data.append([self.num_reseau,self.nom_reseau,self.annee_mise_en_place,self.nomVille,self.code_postal])
        
    def __str__(self):
        return f"{self.num_reseau},{self.nom_reseau},{self.annee_mise_en_place},{self.nomVille},{self.code_postal}"
    
    def ajouterStation(self,s):
        self.stations.append(s)
    
    def afficher_stations(self):
        print([str(s) for s in self.stations])
    
    @classmethod
    def csv(cls):
        header = ['numero','nom','annee','nomVille','code_postal']
        
        with open('reseau.csv','w',encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(cls.data)