CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR (200) NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES content.person(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone,
    UNIQUE (genere_id, film_work_id)
);
--IF you need, you can use Unique Composite index Instead mark Unique

--CREATE UNIQUE INDEX IF NOT EXISTS content.person_film_work 
  --ON dbo.yourtablename(person_id, film_work_id);


CREATE TABLE IF NOT EXISTS content.gener (
    id uuid PRIMARY KEY,
    name VARCHAR (100) NOT NULL UNIQUE,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.gener_film_work (
    id uuid PRIMARY KEY,
    genere_id uuid NOT NULL REFERENCES content.gener(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    created timestamp with time zone,
    UNIQUE (genere_id, film_work_id)
); 
