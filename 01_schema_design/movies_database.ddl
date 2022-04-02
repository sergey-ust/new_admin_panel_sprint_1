--CREATE USER app;
--CREATE DATABASE movies_database OWNER app;

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR (200) NOT NULL,
    description TEXT NOT NULL,
    creation_date DATE NOT NULL,
    rating FLOAT,
    type VARCHAR(15) NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    role TEXT,
    created timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR (100) NOT NULL UNIQUE,
    description TEXT,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    created timestamp with time zone NOT NULL,
    UNIQUE (genre_id, film_work_id)
);

--IF you need, you can use Unique Composite index Instead mark Unique

--CREATE UNIQUE INDEX IF NOT EXISTS person_film_work 
  --ON dbo.yourtablename(person_id, film_work_id);  