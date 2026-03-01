-- PostgreSQL Database Dump
-- Généré le : dim. 01 mars 2026 à 19:01
--
-- Base de données : dw_agriculture

BEGIN;

-- --------------------------------------------------------

--
-- Structure de la table dim_alerte
--

CREATE TABLE dim_alerte (
  id_alerte BIGINT DEFAULT NULL,
  severity_index TEXT DEFAULT NULL,
  alert_msg TEXT DEFAULT NULL,
  type_precip TEXT DEFAULT NULL
);

--
-- Déchargement des données de la table dim_alerte
--

INSERT INTO dim_alerte (id_alerte, severity_index, alert_msg, type_precip) VALUES
(1, 'Jaune', 'Vigilance recommandée, précipitations modérées.', 'Pluie'),
(2, 'Orange', 'Alerte orange : risque élevé de crues.', 'Neige'),
(3, 'RAS', 'Situation normale, aucune alerte.', 'Grêle'),
(4, 'Jaune', 'Vigilance recommandée, précipitations modérées.', 'Grêle'),
(5, 'RAS', 'Situation normale, aucune alerte.', 'Neige'),
(6, 'Orange', 'Alerte orange : risque élevé de crues.', 'Pluie'),
(7, 'RAS', 'Situation normale, aucune alerte.', 'Pluie'),
(8, 'Jaune', 'Vigilance recommandée, précipitations modérées.', 'Neige'),
(9, 'Orange', 'Alerte orange : risque élevé de crues.', 'Grêle'),
(10, 'Rouge', 'ALERTE ROUGE : danger immédiat, évacuation conseillée.', 'Neige'),
(11, 'Rouge', 'ALERTE ROUGE : danger immédiat, évacuation conseillée.', 'Pluie'),
(12, 'Rouge', 'ALERTE ROUGE : danger immédiat, évacuation conseillée.', 'Grêle');

-- --------------------------------------------------------

--
-- Structure de la table dim_station
--

CREATE TABLE dim_station (
  id_station TEXT DEFAULT NULL,
  nom_station TEXT DEFAULT NULL,
  ville TEXT DEFAULT NULL,
  altitude BIGINT DEFAULT NULL,
  zone_geo TEXT DEFAULT NULL,
  capteur_type TEXT DEFAULT NULL
);

--
-- Déchargement des données de la table dim_station
--

INSERT INTO dim_station (id_station, nom_station, ville, altitude, zone_geo, capteur_type) VALUES
('ST001', 'Haouz-Nord', 'Marrakech', 450, 'Haouz', 'Digital'),
('ST002', 'Haouz-Sud', 'Marrakech', 520, 'Haouz', 'Analogique'),
('ST003', 'Gharb-Est', 'Kenitra', 15, 'Gharb', 'Digital'),
('ST004', 'Gharb-Ouest', 'Kenitra', 25, 'Gharb', 'Digital'),
('ST005', 'Souss-Côtier', 'Agadir', 30, 'Souss-Massa', 'Analogique'),
('ST006', 'Souss-Intérieur', 'Agadir', 180, 'Souss-Massa', 'Digital'),
('ST007', 'Tadla-Centre', 'Beni Mellal', 390, 'Tadla', 'Digital'),
('ST008', 'Tadla-Nord', 'Beni Mellal', 420, 'Tadla', 'Analogique'),
('ST009', 'Doukkala-1', 'El Jadida', 20, 'Doukkala', 'Digital'),
('ST010', 'Doukkala-2', 'El Jadida', 35, 'Doukkala', 'Analogique'),
('ST011', 'Moulouya-Amont', 'Oujda', 950, 'Moulouya', 'Digital'),
('ST012', 'Moulouya-Aval', 'Oujda', 320, 'Moulouya', 'Digital'),
('ST013', 'Saiss-Principal', 'Fès', 580, 'Saiss', 'Analogique'),
('ST014', 'Saiss-Secondaire', 'Fès', 610, 'Saiss', 'Digital'),
('ST015', 'Draa-Haut', 'Ouarzazate', 1150, 'Draa-Tafilalet', 'Analogique'),
('ST016', 'Draa-Bas', 'Ouarzazate', 780, 'Draa-Tafilalet', 'Digital'),
('ST017', 'Tensift-Amont', 'Essaouira', 45, 'Tensift', 'Digital'),
('ST018', 'Tensift-Aval', 'Essaouira', 60, 'Tensift', 'Analogique'),
('ST019', 'Loukkos-Nord', 'Larache', 10, 'Loukkos', 'Digital'),
('ST020', 'Loukkos-Sud', 'Larache', 18, 'Loukkos', 'Digital');

-- --------------------------------------------------------

--
-- Structure de la table dim_temps
--

CREATE TABLE dim_temps (
  id_date BIGINT DEFAULT NULL,
  date TEXT DEFAULT NULL,
  jour INTEGER DEFAULT NULL,
  mois INTEGER DEFAULT NULL,
  trimestre INTEGER DEFAULT NULL,
  annee INTEGER DEFAULT NULL,
  saison TEXT DEFAULT NULL
);

--
-- Déchargement des données de la table dim_temps
--

COMMIT;
