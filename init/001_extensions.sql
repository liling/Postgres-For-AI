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
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS pg_textsearch;

-- Register zhparser as a text search parser
CREATE EXTENSION IF NOT EXISTS zhparser;
CREATE TEXT SEARCH CONFIGURATION zh (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION zh ADD MAPPING FOR n,v,a,i,e,l,j WITH simple;
