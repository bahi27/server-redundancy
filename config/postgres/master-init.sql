-- ===== CRÉER L'UTILISATEUR DE RÉPLICATION =====
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';

-- ===== CRÉER LA BASE DE DONNÉES =====
CREATE DATABASE serverdb;

-- ===== CRÉER LES TABLES =====
\c serverdb

CREATE TABLE test (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===== INSÉRER DES DONNÉES DE TEST =====
INSERT INTO test (message) VALUES ('Initial data from Master');
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- ===== COMMIT =====
COMMIT;