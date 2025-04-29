USE projetvlauve;
-- Reseau
INSERT INTO Reseau VALUES
(1, "L'Agence",1990,"Bouira",10000),
(2,"Carnot",2002,"Nancy",54000),
(3,"Les Ensanges",1954,"Tomblaine",54510),
(4,"Poirel",1987,"Vandoeuvre",54200),
(5,"Barbusse",1857,"Lunéville",54680);

-- Station
INSERT INTO Station VALUES
(1, 'Station Centrale', '48.692054, 6.184417', 'Rue Nationale', 10, 100, 20, 80, 10, 50, 2),
(2, 'Carnot Centre', '48.692600, 6.183900', 'Avenue Carnot', 12, 60, 30, 30, 24, 30, 1),
(3, 'Station Toul Est', '48.6781, 5.8884', 'Avenue des Sports', 3, 45, 10, 35, 7, 25, 3),
(4, 'Station Pompidou', '49.1068, 6.1822', 'Boulevard Sébastopol', 21, 30, 15, 15, 10, 12, 4),
(5, 'Station Epinal Centre', '48.1731, 6.4494', 'Rue de la République', 16, 50, 10, 40, 9, 40, 5);




-- Vlauve
INSERT INTO Vlauve VALUES
(1, TRUE, 'disponible', '2024-06-10', 120.5, 0.9, 'vLauveElectrique', 2),
(2, FALSE, 'disponible', '2024-07-01', 60.0, 0.0, 'vlauveNonElectrique', 1),
(3, TRUE, 'enCirculation', '2024-07-15', 200.2, 0.7, 'vLauveElectrique', 3),
(4, TRUE, 'nonDisponible', '2024-05-12', 50.00, 0.3, 'vLauveElectrique', 4),
(5, FALSE, 'disponible', '2024-06-01', 80.00, 0.0, 'vlauveNonElectrique', 5);


-- Abonnement sans refVlauveur
INSERT INTO Abonnement (numAbo, refVlauveur)
VALUES (100, NULL);

-- Facture liée à cet abonnement
INSERT INTO Facture (numero, dateFacture, montantTotal, refAbo)
VALUES (1, '2024-06-01', 45.00, 100);

-- Vlauveur complet
INSERT INTO Vlauveur (
    numVlauveur, email, motDePasse, nom, prenom, telephone,
    numFacture, numAdresse, nomRue, codePostal, nomVille, numAbo
) VALUES (
    888, 'paul.dupont@example.com', 'motdepasse123', 'Dupont', 'Paul', '+33612345678',
    1, 12, 'Rue de Paris', 75001, 'Paris', 100
);

-- Mise à jour de l’abonnement
UPDATE Abonnement
SET refVlauveur = 888
WHERE numAbo = 100;

-- Ajouter le type d’abonnement
INSERT INTO AbonnementAnnuel (numAbo, typeAbonnement)
VALUES (100, 'classique');

-- Paiement
INSERT INTO Paiement VALUES
(400, '2024-07-20', 15.00, 1),
(401, '2024-08-05', 20.00, 1),
(402, '2024-12-04', 9.00, 1),
(403, '2025-11-20', 5.00, 1),
(404, '2025-08-16', 13.00, 1);


INSERT INTO Trajet (stationDepart, stationArrivee, nbKmParcouru,
    dateArrivee, dateRetour, heureArrivee, heureRetour, refVlauveur) VALUES
(1, 2, 3.2, '2024-07-21', '2024-07-21', '10:00:00', '10:30:00', 888),
(2, 3, 3.0, '2024-08-06', '2024-08-06', '09:00:00', '09:20:00', 888),
(3, 4, 3.4, '2024-03-09', '2024-03-09', '15:00:00', '15:50:00', 888),
(4, 5, 3.7, '2024-12-14', '2024-12-14', '07:00:00', '07:20:00', 888),
(5, 1, 3.3, '2025-10-22', '2025-10-22', '12:00:00', '12:45:00', 888);