-- Rechercher tous les vélos disponibles dans une station donnée (Station Centrale)
SELECT *
FROM Vlauve
JOIN Station ON Vlauve.refStation = Station.numStation
WHERE Station.nom = 'Station Centrale'
AND Vlauve.statut = 'disponible';

-- Lister tous les trajets effectués par un abonné (id = 1 et numAbo NOT NULL)
SELECT *
FROM Trajet
JOIN Vlauveur ON Trajet.refVlauveur = Vlauveur.numVlauveur
WHERE Vlauveur.numVlauveur = 1
AND Vlauveur.numAbo IS NOT NULL;

-- Calculer le total des km parcourus par un abonné
SELECT SUM(nbKmParcouru) AS total_kilometres
FROM Trajet
JOIN Vlauveur ON Trajet.refVlauveur = Vlauveur.numVlauveur
WHERE Vlauveur.numVlauveur = 1;
 

-- Générer une facture mensuelle pour un abonné
SELECT 
SUM(Trajet.nbKmParcouru) * 1.00 AS montant_facture
FROM 
Trajet
JOIN 
Vlauveur ON Trajet.refVlauveur = Vlauveur.numVlauveur
WHERE 
Vlauveur.numVlauveur = 1
AND Trajet.dateRetour BETWEEN '2025-10-01' AND '2025-10-30';