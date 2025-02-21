-- Active: 1740066578277@@127.0.0.1@5432@job_db
DROP TYPE IF EXISTS lat_lon;
CREATE TYPE lat_lon AS (
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION
);
DROP TYPE IF EXISTS search_params;

CREATE TYPE search_params AS (
    query VARCHAR(255),
    location VARCHAR(255),
    diameter INT
);
DROP TABLE IF EXISTS Job;
CREATE TABLE Job (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zip VARCHAR(5) NOT NULL,
    lat_lon lat_lon NOT NULL,
    ext_url VARCHAR(255),
    published_at DATE NOT NULL,
    start_date DATE NOT NULL,
    search_params search_params NOT NULL,
    description TEXT
);
DROP TABLE IF EXISTS JobDetails;
CREATE TABLE JobDetails (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(255) NOT NULL REFERENCES Job(id),
    details_url VARCHAR(255) NOT NULL,
    search_params search_params NOT NULL,
    FOREIGN KEY (job_id) REFERENCES Job(id)
);