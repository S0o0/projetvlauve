from Composants.trajet import Trajet
from DAO.DAOVlauveur import DAOVlauveur
import hashlib

class Vlauveur:
    leDAOVlauveur = DAOVlauveur.get_instance()
    
    def __init__(self, numVlauveur,email,  motDePasse, nom, prenom, tel, numAdresse,
    nomRue,codePostal, nomVille, typeAbo):
        self.numVlauveur = numVlauveur
        self.email = email
        self.motDePasse = motDePasse
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.numAdresse = numAdresse
        self.nomRue = nomRue
        self.codePostal = codePostal
        self.nomVille = nomVille
        self.adresse = f"{numAdresse} {nomRue} {nomVille} {codePostal}"
        self.typeAbo = typeAbo
        self.factures = []
        self.trajets = []  # ✅ nouvelle liste de trajets

    def get_numVlauveur(self):
        return self.numVlauveur

    def set_numVlauveur(self, numVlauveur):
        self.numVlauveur = numVlauveur

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_motDePasse(self):
        return self.motDePasse

    def set_motDePasse(self, motDePasse):
        self.motDePasse = motDePasse

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_prenom(self):
        return self.prenom

    def set_prenom(self, prenom):
        self.prenom = prenom

    def get_tel(self):
        return self.tel

    def set_tel(self, tel):
        self.tel = tel

    def get_numAdresse(self):
        return self.numAdresse

    def set_numAdresse(self, numAdresse):
        self.numAdresse = numAdresse
        self._update_adresse()

    def get_nomRue(self):
        return self.nomRue

    def set_nomRue(self, nomRue):
        self.nomRue = nomRue
        self._update_adresse()

    def get_codePostal(self):
        return self.codePostal

    def set_codePostal(self, codePostal):
        self.codePostal = codePostal
        self._update_adresse()

    def get_nomVille(self):
        return self.nomVille

    def set_nomVille(self, nomVille):
        self.nomVille = nomVille
        self._update_adresse()

    def get_typeAbo(self):
        return self.typeAbo

    def set_typeAbo(self, typeAbo):
        self.typeAbo = typeAbo

    def get_factures(self):
        return self.factures

    def ajouter_trajet(self, trajet):
        self.trajets.append(trajet)

    def afficher_trajets(self):
        print(f"Trajets effectués par {self.prenom} {self.nom} :")
        print(self.trajets)

    def total_km(self):
        total = 0
        for trajet in self.trajets:
            total += trajet.nbKmParcouru
        return total

    def __str__(self):
        return f"Vlauveur #{self.numVlauveur} - {self.prenom} {self.nom} - Email : {self.email} - Abonnement #{self.typeAbo}"

    def verifier_identifiants(self, email, motDePasse):
        if self.email != email:
            return False

        try:
            hash_stocke, salt = self.motDePasse.split("/")
        except ValueError:
            return False

        hash_test = hashlib.sha256((motDePasse + salt).encode()).hexdigest()
        return hash_test == hash_stocke


    def generer_facture(self, mois, annee, duree_gratuite=30, tarif_demi_heure=1):
        total = 0
        trajets_factures = []

        for t in self.trajets:
            if t.dateArrivee.split("-")[1] == f"{mois:02}" and t.dateArrivee.split("-")[0] == str(annee):
                heure_arrivee = int(t.heureArrivee.split(":")[0]) * 60 + int(t.heureArrivee.split(":")[1])
                heure_retour = int(t.heureRetour.split(":")[0]) * 60 + int(t.heureRetour.split(":")[1])
                duree = heure_retour - heure_arrivee

                if duree > duree_gratuite:
                    duree_facturable = duree - duree_gratuite
                    cout = ((duree_facturable - 1) // 30 + 1) * tarif_demi_heure
                    total += cout
                    trajets_factures.append(t)

        if total > 0:
            numero_facture = len(self.factures) + 1
            facture = {
                "numero": numero_facture,
                "mois": mois,
                "annee": annee,
                "montant": total,
                "trajets": trajets_factures
            }
            self.factures.append(facture)
            print(f"Facture #{numero_facture} générée : {total}€")
        else:
            print("Aucune facturation ce mois-ci.")