USE projetvlauve;

-- Reseau
INSERT INTO Reseau VALUES
(1, "L'Agence",1990,"Bouira",10000),
(2, "Carnot", 2002,"Nancy",54000),
(3, "Les Ensanges", 1954, "Tomblaine", 54510),
(4, "Poirel", 1987, "Vandoeuvre",54200),
(5, "Barbusse", 1857, "Luneville", 54680);


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


-- SE SERVR DE CET EXEMPLE

-- 1. Abonnement sans refVlauveur
INSERT INTO Abonnement (numAbo, refVlauveur) VALUES (100, NULL);

-- 2. Facture liée à cet abonnement
INSERT INTO Facture (numero, dateFacture, montantTotal, refAbo)
VALUES (1, '2024-06-01', 45.00, 100);

-- 3. Vlauveur complet
INSERT INTO Vlauveur (
    numVlauveur, email, motDePasse, nom, prenom, telephone,
    numFacture, numAdresse, nomRue, codePostal, nomVille, numAbo
)
VALUES (
    888, 'paul.dupont@example.com', 'motdepasse123', 'Dupont', 'Paul', '+33612345678',
    1, 12, 'Rue de Paris', 75001, 'Paris', 100
);

-- 4. Mise à jour de l’abonnement avec le vrai refVlauveur
UPDATE Abonnement SET refVlauveur = 888 WHERE numAbo = 100;

-- 5. Ajouter le type d’abonnement
INSERT INTO AbonnementAnnuel (numAbo, typeAbonnement) VALUES (100, 'classique');










-- Facture
INSERT INTO Facture VALUES
(1, '2024-07-20', 15.00, 101),
(2, '2024-08-05', 20.00, 102),
(3, '2025-04-01', 12.50, 103),
(4, '2025-04-02', 25.00, 104),
(5, '2025-04-03', 30.75, 105);



-- Abonnement
INSERT INTO Abonnement VALUES
(1, 5),
(2, 1),
(3, 2),
(4, 4),
(5, 3);




-- AbonnementAnnuel
INSERT INTO AbonnementAnnuel VALUES
(200, 'classique'),
(201, 'tarifReduit'),
(202, 'classique'),
(203, 'tarifReduit'),
(204, 'classique');




-- AbonnementOccasionnel
INSERT INTO AbonnementOccasionnel VALUES
(201, '1j'),
(202, '7j'),
(203, '1j'),
(204, '7j'),
(205, '1j');


-- Vlauveur
INSERT INTO Vlauveur VALUES
(1, 'marie.doe@email.com', 'pwd123', 'Doe', 'Marie', '+33612345678', 300, 5, 'Rue de Paris', 54000, 'Nancy', 200),
(2, 'jean.durand@email.com', 'pwd456', 'Durand', 'Jean', '+33687654321', 301, 12, 'Rue Carnot', 54000, 'Nancy', 201),
(3, 'alice.martin@email.com', 'alicepass', 'Martin', 'Alice', '+33611223344', 300, 8, 'Boulevard Haussmann', 75009, 'Paris', 200),
(4, 'leo.morel@email.com', 'leo2024', 'Morel', 'Léo', '+33655667788', 301, 22, 'Rue des Lilas', 69003, 'Lyon', 201),
(5, 'emma.bernard@email.com', 'emma_pwd', 'Bernard', 'Emma', '+33699887766', 300, 3, 'Place Stanislas', 54000, 'Nancy', 200);




-- Paiement
INSERT INTO Paiement VALUES
(400, '2024-07-20', 15.00, 300),
(401, '2024-08-05', 20.00, 301),
(402, '2024-12-04', 09.00, 302),
(403, '2025-11-20', 05.00, 303),
(404, '2025-08-16', 13.00, 304);


-- Trajet
INSERT INTO Trajet VALUES
(500, 47, 48, 3.2, '2024-07-21', '2024-07-21', '10:00:00', '10:30:00', 1),
(501, 48, 47, 3.0, '2024-08-06', '2024-08-06', '09:00:00', '09:20:00', 2),
(502, 49, 46, 3.4, '2024-03-09', '2024-03-09', '15:00:00', '17:50:00', 3),
(503, 50, 45, 3.7, '2024-12-14', '2024-12-14', '07:00:00', '07:20:00', 4),
(504, 51, 44, 3.3, '2025-10-22', '2025-10-22', '12:00:00', '12:45:00', 5);