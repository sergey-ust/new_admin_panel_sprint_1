--CREATE USER app;
--CREATE DATABASE movies_database OWNER app;

CREATE SCHEMA content
    CREATE TABLE IF NOT EXISTS film_work (
        id uuid PRIMARY KEY,
        title VARCHAR (200) NOT NULL,
        description TEXT,
        creation_date DATE,
        rating FLOAT,
        type TEXT NOT NULL,
        created timestamp with time zone,
        modified timestamp with time zone
    )
    CREATE TABLE IF NOT EXISTS person (
        id uuid PRIMARY KEY,
        full_name TEXT NOT NULL,
        created timestamp with time zone,
        modified timestamp with time zone
    )
    CREATE TABLE IF NOT EXISTS person_film_work (
        id uuid PRIMARY KEY,
        person_id uuid NOT NULL REFERENCES person(id) ON DELETE CASCADE,
        film_work_id uuid NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
        role TEXT NOT NULL,
        created timestamp with time zone
    )
    CREATE TABLE IF NOT EXISTS genre (
        id uuid PRIMARY KEY,
        name VARCHAR (100) NOT NULL UNIQUE,
        description TEXT,
        created timestamp with time zone,
        modified timestamp with time zone
    )
    CREATE TABLE IF NOT EXISTS genre_film_work (
        id uuid PRIMARY KEY,
        genre_id uuid NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
        film_work_id uuid NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
        created timestamp with time zone,
        UNIQUE (genre_id, film_work_id)
    );

--IF you need, you can use Unique Composite index Instead mark Unique

--CREATE UNIQUE INDEX IF NOT EXISTS person_film_work 
  --ON dbo.yourtablename(person_id, film_work_id);  