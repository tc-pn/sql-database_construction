-- ============================================================
-- schema.sql
-- Modèle normalisé pour les données essentielles de la
-- commande publique (marchés publics / DECP)
-- ============================================================
--
-- Commentaires généraux:
--   - Toutes les colonnes "id" (SIRET/SIREN...) sont stockées en
--     TEXT pour éviter les pertes liées aux arrondis et conserver les 0 en en-tête
--   - Une ligne du CSV source = un couple (marché, modification).
--     idModification peut être NULL si pas de modifs / avenant au marché.
-- ============================================================

CREATE SCHEMA IF NOT EXISTS decp;

-- =====
-- acheteur : Acheteurs
-- =====
CREATE TABLE IF NOT EXISTS decp.acheteur (
    id  VARCHAR(20) PRIMARY KEY, -- numéro SIRET/IBAN/..., entre 9 et 14 chiffres, stocké en chaine de caractère
    nom TEXT
);

-- =====
-- lieu_execution : Lieu d'éxecution du contrat
-- =====
CREATE TABLE IF NOT EXISTS decp.lieu_execution (
    id        SERIAL PRIMARY KEY, -- serial car il n'y a pas de id unique pour tous les lieux, il est donc créé
    code      VARCHAR(20) NOT NULL,
    type_code VARCHAR(50) NOT NULL,
    nom       TEXT, -- difficile d'éxecuter un contrat nulle part !
    UNIQUE (code, type_code) -- chaque combinaison (code, type_code) doit être unique
);

-- =====
-- titulaire : entreprise titulaire d'un marché
-- =====
CREATE TABLE IF NOT EXISTS decp.titulaire (
    id                   VARCHAR(20) PRIMARY KEY, -- numéro SIRET/IBAN/..., entre 9 et 14 chiffres, stocké en chaine de caractère
    type_identifiant     VARCHAR(20),
    denomination_sociale TEXT
);

-- =====
-- marche : quel marché est-il concerné ? 
-- INFORMATIONS CONTRAT
-- =====
CREATE TABLE IF NOT EXISTS decp.marche (
    id                                  VARCHAR(50) PRIMARY KEY,
    acheteur_id                         VARCHAR(20),
    lieu_execution_id                   INTEGER, 

    procedure_marche                    VARCHAR(100),
    nature                              VARCHAR(100),
    code_cpv                            VARCHAR(20),
    duree_mois                          INTEGER,
    date_publication_donnees            DATE,
    date_notification                   DATE,
    objet                               TEXT,
    montant                             NUMERIC(15,2),
    source                              VARCHAR(50),
    technique                           VARCHAR(100),

    -- lien conceptuel vers un accord-cadre (souvent hors périmètre du
    -- jeu de données -> pas de contrainte FK stricte)
    id_accord_cadre                     VARCHAR(50),
 
    modalite_execution                  TEXT,
    marche_innovant                     BOOLEAN,
    ccag                                VARCHAR(100),
    offres_recues                       INTEGER,
    attribution_avance                  BOOLEAN,
    considerations_sociales             TEXT,
    considerations_environnementales    TEXT,
    sous_traitance_declaree             BOOLEAN,
    actes_sous_traitance                TEXT,
    modifications_actes_sous_traitance  TEXT,
 
    forme_prix                          VARCHAR(50),
    type_prix                           VARCHAR(50),
    types_prix                          VARCHAR(255),
 
    origine_ue                          NUMERIC(5,2),
    origine_france                      NUMERIC(5,2),
    taux_avance                         NUMERIC(5,2),
    type_groupement_operateurs          VARCHAR(50),
 
    created_at                          TIMESTAMPTZ,
    updated_at                          TIMESTAMPTZ,
 
    CONSTRAINT fk_marche_acheteur
        FOREIGN KEY (acheteur_id) REFERENCES decp.acheteur(id),
    CONSTRAINT fk_marche_lieu_execution
        FOREIGN KEY (lieu_execution_id) REFERENCES decp.lieu_execution(id)
);

-- =====
-- modifications / avenants au marché
-- =====
CREATE TABLE IF NOT EXISTS decp.modifications (
    id TEXT PRIMARY KEY, -- idModification dans le csv
    marche_id                               VARCHAR(50),
    boolean_modification                    BOOLEAN,
    objet_modification                      TEXT,
    date_notification_modification          DATE,
    duree_mois_modification                 INTEGER,
    date_publication_donnees_modification   DATE,
    montant_modification                    NUMERIC(15,2),
    titulaires_modification                 TEXT,
 
    CONSTRAINT fk_modification_marche
        FOREIGN KEY (marche_id) REFERENCES decp.marche(id) ON DELETE CASCADE

);

-- =====
-- marché titulaire, ie groupement d'entreprises : garantir l'unicité d'un couple (entreprise, contrat)
-- elle sert aussi à conserver le rang d'une entreprise dans un contrat
-- =====
CREATE TABLE IF NOT EXISTS marche_titulaire (
    marche_id     VARCHAR(50) NOT NULL,
    titulaire_id  VARCHAR(20) NOT NULL,
    rang          SMALLINT NOT NULL,

    -- marche_id et titulaire_id sont des foreign keys récupérées des tables marche, titulaire
    -- pk_marche_titulaire est une primary key composite qui garanti l'unicité du trio entreprise, marche, rang
    -- il sera alors plus simple 
    CONSTRAINT pk_marche_titulaire PRIMARY KEY (marche_id, titulaire_id),
    CONSTRAINT fk_marche_titulaire_marche
        FOREIGN KEY (marche_id) REFERENCES decp.marche(id),
    CONSTRAINT fk_marche_titulaire_titulaire
        FOREIGN KEY (titulaire_id) REFERENCES decp.titulaire(id)
);

-- =====
-- Indices pour la performance des requêtes
-- =====

-- marché
CREATE INDEX IF NOT EXISTS idx_marche_acheteur          ON decp.marche(acheteur_id);
CREATE INDEX IF NOT EXISTS idx_marche_lieu_execution    ON decp.marche(lieu_execution_id);
CREATE INDEX IF NOT EXISTS idx_marche_code_cpv          ON decp.marche(code_cpv);
CREATE INDEX IF NOT EXISTS idx_marche_date_notification ON decp.marche(date_notification);
CREATE INDEX IF NOT EXISTS idx_marche_accord_cadre      ON decp.marche(id_accord_cadre);

-- avenants au marché
CREATE INDEX IF NOT EXISTS idx_modifications_marche ON decp.modifications(marche_id);