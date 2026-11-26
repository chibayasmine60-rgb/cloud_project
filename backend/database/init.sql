CREATE TABLE departments(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
CREATE TABLE announcements (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

INSERT INTO departments (name, description) VALUES ('Informatique', 'Programmation, reseaux et bases de donnees');
INSERT INTO departments (name, description) VALUES ('Mathematiques', 'Algebre, analyse et statistiques');
INSERT INTO departments (name, description) VALUES ('Physique', 'Mecanique, optique et electricite');
INSERT INTO departments (name, description) VALUES ('Langues', 'Anglais, francais et traduction');
INSERT INTO departments (name, description) VALUES ('Médecine', 'Etudes medicales, anatomie et stages a l''hopital');
INSERT INTO departments (name, description) VALUES ('Biologie', 'Cellules, genetique et sciences de la vie');
INSERT INTO departments (name, description) VALUES ('Chimie', 'Chimie organique et travaux pratiques en laboratoire');

INSERT INTO announcements (title, content) VALUES ('Rentree universitaire', 'La rentree commence le 15 septembre');
INSERT INTO announcements (title, content) VALUES ('Portes ouvertes', 'Journee portes ouvertes le samedi 12 octobre');
INSERT INTO announcements (title, content) VALUES ('Examens', 'Les examens du premier semestre commencent en janvier');
INSERT INTO announcements (title, content) VALUES ('Conference cloud', 'Conference sur le cloud computing a l amphi A');
INSERT INTO announcements (title, content) VALUES ('Bourses d''etudes', 'Le dossier de bourse est a deposer avant le 30 novembre');
INSERT INTO announcements (title, content) VALUES ('Residence universitaire', 'Les inscriptions a la residence sont ouvertes');
INSERT INTO announcements (title, content) VALUES ('Stage en entreprise', 'Les etudiants de master peuvent deposer leur demande de stage');
INSERT INTO announcements (title, content) VALUES ('Bibliotheque', 'Nouveaux horaires: de 8h a 18h du dimanche au jeudi');

INSERT INTO users (username, password_hash) VALUES ('admin', 'PASTE_HASH_HERE');
UPDATE users
SET password_hash ='pbkdf2:sha256:1000000$NI92JzPpcmCnYmn1$0835bdbc08790501aa7d2e82112ad1c3e66fd2fa96fcf7bade3c8b5efc2d9004'
WHERE username = 'admin';


