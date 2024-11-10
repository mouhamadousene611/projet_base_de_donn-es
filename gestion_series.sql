create database if not exists Serie;
use serie;

-- creation de la table serie
CREATE TABLE series (
id_series INT AUTO_INCREMENT PRIMARY KEY,
titre VARCHAR(255) NOT NULL,
description_serie TEXT,
date_publication DATE,
langue VARCHAR(50),
genre VARCHAR(100),
categorie ENUM('Film', 'Anime') NOT NULL,
maison_production VARCHAR(100)
);

-- creation de la table episode 

CREATE TABLE episodes (
id_episode INT AUTO_INCREMENT PRIMARY KEY,
id_series INT,
titre_episode VARCHAR(255) NOT NULL,
season INT,
numero INT,
date_diffusion DATE,
FOREIGN KEY (id_series) REFERENCES series(id_series)
);

-- creation de la table caractere

CREATE TABLE caractere (
id_caractere INT AUTO_INCREMENT PRIMARY KEY,
id_series INT,
nom_caractere VARCHAR(100) NOT NULL,
roles VARCHAR(50), 
descriptions TEXT,
FOREIGN KEY (id_series) REFERENCES series(id_series)
);

CREATE TABLE categories (
id_category INT AUTO_INCREMENT PRIMARY KEY,
categorie VARCHAR(100) NOT NULL
);

CREATE TABLE series_categories (
id_series INT,
id_category INT,
PRIMARY KEY (id_series, id_category),
FOREIGN KEY (id_series) REFERENCES series(id_series),
FOREIGN KEY (id_category) REFERENCES categories(id_category)
);

CREATE TABLE images (
id_image INT AUTO_INCREMENT PRIMARY KEY,
id_series INT,
url VARCHAR(255) NOT NULL, -- URL or file path of the image
descriptions TEXT,
FOREIGN KEY (id_series) REFERENCES series(id_series)
);
-- ------------------------------------------------------------------------------
-- inserons des données dans la table serie

INSERT INTO series (titre, description_serie, date_publication, langue, genre, categorie, maison_production) VALUES 
("Naruto Shippuden", "Continuation de l'histoire de Naruto Uzumaki.", "2007-02-15", "Japonais", "Action", "Anime", "Studio Pierrot"),
("Inception", "Un voleur qui entre dans les rêves des gens.", "2010-07-16", "Anglais", "Science-fiction", "Film", "Warner Bros"),
("Pirate_des_caraibes", "la  fontaine de jouvence qui est un boisson qui offre une longitivité a celui qui le boit ", "2011-05-18", "Espanol", "Aventure, Comédie", "Film", "Jerry Bruckheimer Films");

INSERT INTO series (titre, description_serie, date_publication, langue, genre, categorie, maison_production) VALUES 
("Casa des papels", "braquage de banques", "2017-12-20", "espagnole", "Action", "Film", "Studio Pierrot");

-- inserons des données dans la table serie
INSERT INTO categories (categorie) VALUES 
("Action"),
("Comédie"),
("Drame"),
("Science-fiction"),
("Anime");

INSERT INTO episodes (id_series, titre_episode, season, numero, date_diffusion)
VALUES 
(1, "C'est moi Naruto Uzumaki!", 1, 1, '2002-10-03'),
(1, "je m'appelle Konohamaru!", 1, 2, '2002-10-10'),
(1, "Sasuke et Sakura ?", 1, 3, '2002-10-17'),
(1, "passe ou recalé: Teste de survi", 1, 4, '2002-10-24'),
(1, "la decision de Kakashi", 1, 5, '2002-10-31'),
(1, "une mission dangereuse", 1, 6, '2002-11-07');

INSERT INTO episodes (id_series, titre_episode, season, numero, date_diffusion)
VALUES 
(3, "On est de retour", 1, 1, '2017-05-02'),  -- Episode 1 air date
(3, "Aïkido", 1, 2, '2017-05-09'),
(3, "48 mètres sous terre", 1, 3, '2017-05-16'),
(3, "Plus rien n'avait d'importance", 1, 4, '2017-05-23'),
(3, "La Dérive", 1, 5, '2017-05-30'),
(3, "Leçon d'anatomie", 1, 6, '2017-06-06');



