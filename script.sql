DROP DATABASE IF EXISTS projetVlauve;

CREATE DATABASE IF NOT EXISTS projetVlauve;

USE projetVlauve;

CREATE TABLE IF NOT EXISTS Reseau(
    numReseau INT,
    nomReseau VARCHAR(30),
    anneeMiseEnPlace YEAR,
    nomVille VARCHAR(30),
    codePostal INT(5),
    PRIMARY KEY (numReseau)
);

CREATE TABLE IF NOT EXISTS Station(
    numStation INT,
    nom VARCHAR(30),
    coordonneesGPS VARCHAR(100),
    nomRue VARCHAR(30),
    numeroRue INT,
    nbPlacesTotal INT,
    nbPlacesElectriques INT,
    nbPlacesNonElectriques INT,
    nbVlauvesElectriques INT,
    nbVlauvesNonElectriques INT,
    numReseau INT,
    PRIMARY KEY (numStation),
    FOREIGN KEY (numReseau) REFERENCES Reseau(numReseau),
    CHECK (nbPlacesTotal = nbPlacesElectriques + nbPlacesNonElectriques),
    CHECK (nbVlauvesElectriques <= nbPlacesElectriques),
    CHECK (nbVlauvesNonElectriques <= nbPlacesNonElectriques)
);

CREATE TABLE IF NOT EXISTS Vlauve(
    ref INT,
    assistance BOOLEAN,
    statut ENUM('disponible', 'enCirculation', 'enReparation', 'enPanne', 'perdu', 'nonDisponible'),
    dateCirculation DATE,
    nbKmParcouru DECIMAL(10,2),
    niveauBatterie FLOAT,
    discriminant ENUM('vLauveElectrique', 'vlauveNonElectrique'),
    refStation INT,
    PRIMARY KEY (ref),
    FOREIGN KEY (refStation) REFERENCES Station (numStation),
    CHECK (NOT (discriminant = 'vLauveElectrique' AND niveauBatterie < 0.5 AND statut <> 'nonDisponible')),
    CHECK (
        (assistance = TRUE AND discriminant = 'vLauveElectrique') OR
        (assistance = FALSE AND discriminant = 'vlauveNonElectrique')
    )
);

-- CREATE TABLE IF NOT EXISTS Ville(
--     codePostal INT,
--     nom VARCHAR(30),
--     nbMinGratuites INT,
--     coutDemiHeure INT,
--     PRIMARY KEY (codePostal),
--     CHECK (coutDemiHeure <= 2)
-- );

CREATE TABLE IF NOT EXISTS Facture(
    numero INT AUTO_INCREMENT,
    dateFacture DATE,
    montantTotal DECIMAL(10,2),
    refAbo INT NOT NULL,
    PRIMARY KEY (numero)
    -- FOREIGN KEY (refAbo) REFERENCES Abonnement(numAbo) -- on ajoute plus tard pour éviter de faire référence à une entité avant de l'avoir
    -- créer
);

CREATE TABLE IF NOT EXISTS  Abonnement(
    numAbo INT,
    refVlauveur INT,
    PRIMARY KEY (numAbo)
    -- FOREIGN KEY (refVlauveur) REFERENCES Vlauveur(numVlauveur) -- on ajoute plus tard pour éviter de faire référence à une entité avant de l'avoir
    -- créer
);
-- Jsp comment interpréter : "Pour les abonnements annuels à tarif réduit, la copie de la carte d'identité est demandée. 
-- Ils doivent également déposer un montant de garantie (150€) par un paiement par carte."
CREATE TABLE IF NOT EXISTS  AbonnementAnnuel(
    numAbo INT,
    -- montantGarantie INT,
    -- paiement DECIMAL(10,2),
    typeAbonnement ENUM('classique', 'tarifReduit'),
    PRIMARY KEY (numAbo),
    FOREIGN KEY (numAbo) REFERENCES Abonnement(numAbo)
    -- CHECK (montantGarantie = 150)
);


CREATE TABLE IF NOT EXISTS  AbonnementOccasionnel(
    numAbo INT,
    PRIMARY KEY (numAbo),
    duree ENUM('1j','7j'),
    FOREIGN KEY (numAbo) REFERENCES Abonnement(numAbo)
);

CREATE TABLE IF NOT EXISTS Vlauveur(
    numVlauveur INT AUTO_INCREMENT,
    email VARCHAR(50),
    motDePasse VARCHAR(50),
    nom VARCHAR(30),
    prenom VARCHAR(30),
    telephone VARCHAR(12), -- de la forme '+33620981405'
    numFacture INT,
    numAdresse INT,
    nomRue VARCHAR(30),
    codePostal INT(5),
    nomVille VARCHAR(30),
    numAbo INT,
    PRIMARY KEY (numVlauveur),
    FOREIGN KEY (numAbo)REFERENCES Abonnement(numAbo),
    FOREIGN KEY (numFacture) REFERENCES Facture(numero)
);

ALTER TABLE Facture ADD FOREIGN KEY (refAbo) REFERENCES Abonnement(numAbo);

ALTER TABLE Abonnement ADD FOREIGN KEY (refVlauveur) REFERENCES Vlauveur(numVlauveur);


CREATE TABLE IF NOT EXISTS Paiement(
    numeroPaiement INT,
    datePaiement DATE,
    montant DECIMAL(10,2),
    numeroFacture INT NOT NULL,
    PRIMARY KEY (numeroPaiement),
    FOREIGN KEY (numeroFacture) REFERENCES Facture(numero)
);


CREATE TABLE IF NOT EXISTS Trajet(
    ref INT AUTO_INCREMENT,
    stationDepart INT NOT NULL,
    stationArrivee INT NOT NULL,
    nbKmParcouru DECIMAL(10,2),
    dateArrivee DATE,
    dateRetour DATE,
    heureArrivee TIME,
    heureRetour TIME,
    refVlauveur INT,
    PRIMARY KEY (ref),
    FOREIGN KEY (refVlauveur) REFERENCES Vlauveur(numVlauveur),
    FOREIGN KEY (stationDepart) REFERENCES Station(numStation),
    FOREIGN KEY (stationArrivee) REFERENCES Station(numStation)
    -- Comment modéliser "Tous les trajets d'un vlauve sont tracés" ?
    -- refVlauve INT,
    -- FOREIGN KEY (refVlauve) REFERENCES Vlauve(ref),  
    );
    