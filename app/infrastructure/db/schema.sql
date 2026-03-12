CREATE SCHEMA IF NOT EXISTS github_crawler;

CREATE TABLE IF NOT EXISTS github_crawler.repositories (
    github_id        TEXT PRIMARY KEY,
    repository_name  TEXT NOT NULL,
    owner_login      TEXT NOT NULL,
    repository_url   TEXT NOT NULL,
    stars_count      INTEGER NOT NULL,
    crawled_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_repositories_owner_login
    ON github_crawler.repositories (owner_login);

CREATE INDEX IF NOT EXISTS idx_repositories_stars_count
    ON github_crawler.repositories (stars_count);

CREATE INDEX IF NOT EXISTS idx_repositories_updated_at
    ON github_crawler.repositories (updated_at);


    