class Vlauveur:
    def __init__(self, num_vlauveur,email,  mot_de_passe, nom, prenom, tel, num_adresse,
    nom_rue,code_postal, nom_ville, typeAbo):
        self.num_vlauveur = num_vlauveur
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.num_adresse = num_adresse
        self.nom_rue = nom_rue
        self.code_postal = code_postal
        self.nom_ville = nom_ville
        self.adresse = f"{numero_adresse} {nom_rue} {nom_ville} {code_postal}"
        self.typeAbo = typeAbo
        self.factures = []

    def verifier_identifiants(self, email, mot_de_passe,):
        return self.email == email and self.mot_de_passe == mot_de_passe
