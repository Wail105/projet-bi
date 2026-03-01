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

CREATE TABLE dim_station (
  id_station TEXT DEFAULT NULL,
  nom_station TEXT DEFAULT NULL,
  ville TEXT DEFAULT NULL,
  altitude BIGINT DEFAULT NULL,
  zone_geo TEXT DEFAULT NULL,
  capteur_type TEXT DEFAULT NULL
);

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
