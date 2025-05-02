import tkinter as tk
from tkinter import ttk, messagebox

class AccueilFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.vlauveur = controller.utilisateur_connecte

        ttk.Label(self, text=f"Bienvenue {self.vlauveur.prenom} {self.vlauveur.nom}", font=("Arial", 14)).pack(pady=10)

        ttk.Button(self, text="Stations disponibles", command=self.voir_stations).pack(pady=5)
        ttk.Button(self, text="Gérer mon abonnement", command=self.gerer_abonnement).pack(pady=5)
        ttk.Button(self, text="Voir mes trajets", command=self.voir_trajets).pack(pady=5)
        ttk.Button(self, text="Voir mes factures", command=self.voir_factures).pack(pady=5)
        ttk.Button(self, text="Total kilomètres parcourus", command=self.km_total).pack(pady=5)
        ttk.Button(self, text="Générer une facture", command=self.facturer).pack(pady=5)

    def voir_stations(self):
        from DAO.DAOStation import DAOStation

        stations = DAOStation.get_instance().get_all_stations()
        
        if not stations:
            messagebox.showinfo("Stations", "Aucune station disponible.")
            return

        # Créer une nouvelle fenêtre
        fenetre = tk.Toplevel(self)
        fenetre.title("Stations disponibles")
        fenetre.geometry("1000x400")

        # Définir les colonnes du tableau
        colonnes = (
            "ID", "Nom", "Adresse", "Coordonnées GPS",
            "Total places", "Vlauves électriques", "Vlauves non électriques"
        )
        tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings")
        
        for col in colonnes:
            tableau.heading(col, text=col)
            tableau.column(col, width=130, anchor="center")

        # Ajouter les données des stations
        for station in stations:
            tableau.insert("", "end", values=(
                station.numStation,
                station.nom,
                station.adresse,
                station.coordonneesGPS,
                station.nbPlacesTotal,
                station.nbVlauvesElectriques,
                station.nbVlauvesNonElectriques
            ))

        tableau.pack(expand=True, fill="both", padx=10, pady=10)

    def gerer_abonnement(self):
        from DAO.DAOAbonnement import DAOAbonnement
        
        # Exemple de fenêtre pour gérer l'abonnement
        fenetre = tk.Toplevel(self)
        fenetre.title("Gestion de l'abonnement")
        fenetre.geometry("400x200")
        
        dao = DAOAbonnement.get_instance()
        abo = dao.find_abonnement(self.vlauveur.numVlauveur)

        if not abo:
            ttk.Label(fenetre, text="Aucun abonnement actif.").pack(pady=10)
            return

        ttk.Label(fenetre, text=f"Abonnement #{abo['numAbo']}", font=("Arial", 12)).pack(pady=5)
        ttk.Label(fenetre, text=f"Type : {abo['type']}").pack(pady=5)

        if abo["type"] == "annuel":
            ttk.Label(fenetre, text=f"Formule : {abo['typeAbonnement']}").pack(pady=5)
            # Tu peux ajouter ici : montant de garantie, mode de paiement, etc.

        elif abo["type"] == "occasionnel":
            ttk.Label(fenetre, text=f"Durée : {abo['duree']}").pack(pady=5)

        else:
            ttk.Label(fenetre, text="Type d'abonnement non reconnu.").pack(pady=5)

        
    
    def voir_trajets(self):
        if len(self.vlauveur.trajets) == 0:
            messagebox.showinfo("Mes trajets", "Aucun trajet effectué.")
        else:
            for trajet in self.vlauveur.trajets:
                messagebox.showinfo("Trajet", str(trajet))

    def voir_factures(self):
        if len(self.vlauveur.factures) == 0:
            messagebox.showinfo("Mes factures", "Aucune facture générée.")
        else:
            for facture in self.vlauveur.factures:
                messagebox.showinfo("Facture", f"Facture #{facture['numero']}, mois {facture['mois']}/{facture['annee']}, montant : {facture['montant']}€")

    def km_total(self):
        total = self.vlauveur.total_km()
        messagebox.showinfo("Total des kilomètres", f"Tu as parcouru {total} km.")

    def facturer(self):
        self.vlauveur.generer_facture(mois=4, annee=2024)