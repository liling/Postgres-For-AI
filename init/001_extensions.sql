-- 1. Ensure public schema exists and has correct permissions
CREATE SCHEMA IF NOT EXISTS public;
GRANT USAGE ON SCHEMA public TO public;

-- 2. Explicitly install pgvector into the public schema
-- This satisfies LightRAG's driver which hardcodes 'public.vector'
DROP EXTENSION IF EXISTS vector CASCADE;
CREATE EXTENSION vector SCHEMA public;

-- 3. Enable other extensions as usual
CREATE EXTENSION IF NOT EXISTS age;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
