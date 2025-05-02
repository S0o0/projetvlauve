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

        #Bouton Ajouter
        ttk.Button(self, text="Ajouter un abonnement", command=self.ajouter_abonnement).pack(pady=5)
        
        # Bouton Modifier
        ttk.Button(fenetre, text="Modifier", command=lambda: self.modifier_abonnement(abo)).pack(pady=5)

        # Bouton Supprimer
        ttk.Button(fenetre, text="Supprimer", command=lambda: self.supprimer_abonnement(abo['numAbo'], fenetre)).pack(pady=5)
    
    def ajouter_abonnement(self):
        # Fenêtre d'ajout d'abonnement
        fenetre = tk.Toplevel(self)
        fenetre.title("Ajouter un abonnement")
        fenetre.geometry("400x300")

        # Sélectionner le type d'abonnement (Annuel ou Occasionnel)
        ttk.Label(fenetre, text="Type d'abonnement :").pack(pady=10)

        type_var = tk.StringVar()

        # Choisir entre Abonnement Annuel ou Occasionnel
        type_combobox = ttk.Combobox(fenetre, textvariable=type_var, values=["annuel", "occasionnel"], state="readonly")
        type_combobox.pack(pady=10)
        type_combobox.set("annuel")  # Par défaut, l'abonnement est annuel

        # Créer les champs supplémentaires en fonction du type choisi
        def afficher_options_abonnement(event):
            # Supprimer les anciens widgets
            for widget in fenetre.winfo_children():
                if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Label):
                    widget.destroy()

            # Afficher les champs en fonction du type d'abonnement sélectionné
            if type_var.get() == "annuel":
                ttk.Label(fenetre, text="Formule (classique/tarifReduit) :").pack(pady=10)
                formule_var = tk.StringVar()
                formule_entry = ttk.Entry(fenetre, textvariable=formule_var)
                formule_entry.pack(pady=10)

                def valider_annuel():
                    from DAO.DAOAbonnement import DAOAbonnement
                    if formule_var.get().strip().lower() not in ["classique", "tarifreduit"]:
                        messagebox.showerror("Erreur", "Formule invalide.")
                        return

                    # Ajouter l'abonnement annuel
                    dao = DAOAbonnement.get_instance()
                    dao.ajouter_abonnement_annuel(self.vlauveur.numVlauveur, formule_var.get().strip().lower())
                    messagebox.showinfo("Succès", "Abonnement annuel ajouté.")
                    fenetre.destroy()

                ttk.Button(fenetre, text="Ajouter Abonnement Annuel", command=valider_annuel).pack(pady=10)

            elif type_var.get() == "occasionnel":
                ttk.Label(fenetre, text="Durée (1j/7j) :").pack(pady=10)
                duree_var = tk.StringVar()
                duree_entry = ttk.Entry(fenetre, textvariable=duree_var)
                duree_entry.pack(pady=10)

                def valider_occasionnel():
                    from DAO.DAOAbonnement import DAOAbonnement
                    if duree_var.get().strip().lower() not in ["1j", "7j"]:
                        messagebox.showerror("Erreur", "Durée invalide.")
                        return

                    # Ajouter l'abonnement occasionnel
                    dao = DAO.DAOAbonnement.get_instance()
                    dao.ajouter_abonnement_occasionnel(self.vlauveur.numVlauveur, duree_var.get().strip().lower())
                    messagebox.showinfo("Succès", "Abonnement occasionnel ajouté.")
                    fenetre.destroy()

                ttk.Button(fenetre, text="Ajouter Abonnement Occasionnel", command=valider_occasionnel).pack(pady=10)

        # Ajouter un event pour mettre à jour la fenêtre en fonction du type d'abonnement
        type_combobox.bind("<<ComboboxSelected>>", afficher_options_abonnement)
        
        # Afficher les options d'abonnement au départ
        afficher_options_abonnement(None)


    def modifier_abonnement(self, abo):
        fenetre_modif = tk.Toplevel(self)
        fenetre_modif.title("Modifier l'abonnement")
        fenetre_modif.geometry("400x300")

        if abo["type"] == "annuel":
            ttk.Label(fenetre_modif, text="Nouvelle formule (classique/tarifReduit):").pack(pady=5)
            formule_var = tk.StringVar(value=abo["typeAbonnement"])
            formule_entry = ttk.Entry(fenetre_modif, textvariable=formule_var)
            formule_entry.pack(pady=5)

            def valider():
                from DAO.DAOAbonnement import DAOAbonnement
                nouveau_type = formule_var.get().strip().lower()
                if nouveau_type not in ["classique", "tarifreduit"]:
                    messagebox.showerror("Erreur", "Formule invalide.")
                    return

                DAOAbonnement.get_instance().modifier_abonnement_annuel(abo["numAbo"], nouveau_type)
                messagebox.showinfo("Succès", "Abonnement modifié.")
                fenetre_modif.destroy()

            ttk.Button(fenetre_modif, text="Valider", command=valider).pack(pady=10)

        elif abo["type"] == "occasionnel":
            ttk.Label(fenetre_modif, text="Nouvelle durée (1j/7j):").pack(pady=5)
            duree_var = tk.StringVar(value=str(abo["duree"]))
            duree_entry = ttk.Entry(fenetre_modif, textvariable=duree_var)
            duree_entry.pack(pady=5)

            def valider():
                from DAO.DAOAbonnement import DAOAbonnement
                nouveau_type = duree_var.get().strip().lower()
                if nouveau_type not in ["1j", "7j"]:
                    messagebox.showerror("Erreur", "Formule invalide.")
                    return

                DAOAbonnement.get_instance().modifier_abonnement_occasionnel(abo["numAbo"], nouveau_type)
                messagebox.showinfo("Succès", "Abonnement modifié.")
                fenetre_modif.destroy()

            ttk.Button(fenetre_modif, text="Valider", command=valider).pack(pady=10)

        else:
            ttk.Label(fenetre_modif, text="Type non reconnu.").pack()

    def supprimer_abonnement(self, num_abo, fenetre_parent):
        from DAO.DAOAbonnement import DAOAbonnement

        confirm = messagebox.askyesno("Confirmation", "Supprimer l'abonnement ?")
        if confirm:
            from Composants.abonnement import Abonnement
            abo = Abonnement(num_abo, self.vlauveur.numVlauveur)
            DAOAbonnement.get_instance().delete_abonnement(abo)
            messagebox.showinfo("Succès", "Abonnement supprimé.")
            fenetre_parent.destroy()

    def voir_trajets(self):
        trajets = self.vlauveur.trajets
        if not trajets:
            messagebox.showinfo("Mes trajets", "Aucun trajet effectué.")
            return

        # Nouvelle fenêtre avec Treeview
        fenetre = tk.Toplevel(self)
        fenetre.title("Mes trajets")
        fenetre.geometry("1200x400")

        colonnes = (
            "Réf", "Départ", "Arrivée", "Km parcourus",
            "Date départ", "Heure départ", "Date retour", "Heure retour", "Vlauveur"
        )

        tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings")

        for col in colonnes:
            tableau.heading(col, text=col)
            tableau.column(col, width=120, anchor="center")

        for trajet in trajets:
            tableau.insert("", "end", values=(
                trajet.get_ref(),
                trajet.get_stationDepart(),
                trajet.get_stationArrivee(),
                trajet.get_nbKmParcouru(),
                trajet.get_dateArrivee(),
                trajet.get_heureArrivee(),
                trajet.get_dateRetour(),
                trajet.get_heureRetour(),
                trajet.get_refVlauveur()
            ))

        tableau.pack(expand=True, fill="both", padx=10, pady=10)



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