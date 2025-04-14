DROP DATABASE IF EXISTS projetVlauve;

CREATE DATABASE IF NOT EXISTS projetVlauve;

USE projetVlauve;

CREATE TABLE IF NOT EXISTS Vlauve(
    ref INT,
    assistance BOOLEAN,
    statut ENUM('disponible', 'enCirculation', 'enReparation', 'enPanne', 'perdu', 'nonDisponible'),
    dateCirculation DATE,
    nbKmParcouru DECIMAL(10,2),
    niveauBatterie FLOAT,
    discriminant ENUM('vLauveElectrique', 'vlauveNonElectrique'),
    PRIMARY KEY (ref),
    CHECK (NOT (discriminant = 'vLauveElectrique' AND niveauBatterie < 0.5 AND statut <> 'nonDisponible'))
);

CREATE TABLE IF NOT EXISTS Ville(
    codePostal INT,
    nom VARCHAR(30),
    nbMinGratuites INT,
    coutDemiHeure INT,
    PRIMARY KEY (codePostal),
    CHECK (coutDemiHeure <= 2)
);

CREATE TABLE IF NOT EXISTS Station(
    numStation INT,
    nom VARCHAR(30),
    coordonneesGPS VARCHAR(100),
    nomRue VARCHAR(30),
    numeroRue INT,
    nbPlacesTotale INT,
    nbPlacesElectriques INT,
    nbPlacesNonElectriques INT,
    nbVlauvesElectriques INT,
    nbVlauvesNonElectriques INT,
    -- numReseau INT,
    PRIMARY KEY (numStation),
    -- FOREIGN KEY (numReseau) REFERENCES Reseau(numReseau),
    CHECK (nbPlacesTotale = nbPlacesElectriques + nbPlacesNonElectriques),
    CHECK (nbVlauvesElectriques <= nbPlacesElectriques),
    CHECK (nbVlauvesNonElectriques <= nbPlacesNonElectriques)
);

CREATE TABLE IF NOT EXISTS Reseau(
    numReseau INT,
    nomReseau VARCHAR(30),
    anneeMiseEnPlace YEAR,
    nomVille VARCHAR(30),
    codePostal INT(5),
    PRIMARY KEY (numReseau)
);

CREATE TABLE IF NOT EXISTS Trajet(
    ref INT,
    stationDepart VARCHAR(30),
    -- A voir si on laisse le nom ou alors fk vers station
    stationArrivee VARCHAR(30),
    nbKmParcouru DECIMAL(10,2),
    dateArrivee DATE,
    dateRetour DATE,
    heureArrivee TIME,
    heureRetour TIME,
    refVlauveur INT,
    FOREIGN KEY (refVlauveur) REFERENCES Vlauveur(A COMPLETER)
    -- numStation INT,
    -- numReseau INT,
    -- PRIMARY KEY (ref, numStation, numReseau),
    -- FOREIGN KEY (ref) REFERENCES Vlauve(ref),
    -- FOREIGN KEY (numStation) REFERENCES Station(numStation),
    -- FOREIGN KEY (numReseau) REFERENCES Reseau(numReseau)
);

CREATE TABLE IF NOT EXISTS  Abonnement(
    numAbo INT,
    PRIMARY KEY (numAbo)
);

CREATE TABLE IF NOT EXISTS  AbonnementAnnuel(
    numAbo INT,
    montantGarantie INT,
    paiement DECIMAL(10,2),
    discriminant2 ENUM('classique', 'tarifReduit'),
    PRIMARY KEY (numAbo),
    FOREIGN KEY (numAbo) REFERENCES Abonnement(numAbo),
    CHECK (montantGarantie = 150)
);


CREATE TABLE IF NOT EXISTS  AbonnementOccasionnel(
    numAbo INT,
    PRIMARY KEY (numAbo),
    FOREIGN KEY (numAbo) REFERENCES Abonnement(numAbo)
);


CREATE TABLE IF NOT EXISTS Vlauveur(
    numVlauveur INT,
    email VARCHAR(50),
    motDePasse VARCHAR(50),
    nom VARCHAR(30),
    prenom VARCHAR(30),
    telephone VARCHAR(10),
    numeroCarte INT,
    numAdresse INT,
    nomRue VARCHAR(30),
    codePostal INT(5),
    nomVille VARCHAR(30),
    numAbo INT,
    PRIMARY KEY (numVlauveur),
    FOREIGN KEY (numAbo)REFERENCES Abonnement(numAbo)
);

CREATE TABLE IF NOT EXISTS Facture(
    numero INT,
    -- duree INT,
    montantTotal DECIMAL(10,2),
    numVla INT,
    PRIMARY KEY (numero),
    FOREIGN KEY (numVla) REFERENCES Vlauveur(numVlauveur)
);

CREATE TABLE IF NOT EXISTS Paiement(
    numeroPaiement INT,
    dateMontant DATE,
    numeroFacture INT,
    PRIMARY KEY (numeroPaiement),
    FOREIGN KEY (numeroFacture) REFERENCES Facture(numero)
);