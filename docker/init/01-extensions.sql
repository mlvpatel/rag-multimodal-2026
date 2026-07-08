-- Enable pgvector for dense vector search on Postgres.
-- This runs automatically the first time the Postgres data directory is
-- initialized (files in /docker-entrypoint-initdb.d are executed on init).
CREATE EXTENSION IF NOT EXISTS vector;
