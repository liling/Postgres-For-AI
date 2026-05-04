# PostgreSQL for AI

**PostgreSQL 18 with pgvector, Apache AGE, pg_textsearch & AI-ready extensions**

A production-ready PostgreSQL Docker image optimized for AI workloads, combining vector search, graph queries, full-text search (including Chinese), and BM25 ranking in a single database.

Ideal for:

- RAG (Retrieval-Augmented Generation)
- Hybrid Vector + Graph + Full-text search
- AI metadata storage
- LLM memory & embeddings
- Agentic & knowledge-graph systems
- Chinese text search & analysis

## Features

- **PostgreSQL 18.2**
- **pgvector (v0.8.2)** – Vector embeddings & similarity search
- **Apache AGE (PG18 / v1.7.0-rc0)** – Cypher graph queries
- **pg_textsearch (BM25)** – Full-text search with BM25 ranking
- **zhparser + SCWS** – Chinese full-text search parser
- **pg_stat_statements** – Query performance monitoring
- **pg_trgm** – Trigram text similarity
- **uuid-ossp** – UUID generation
- AI-friendly schema & search_path
- Plug-and-play with Docker Compose
- Compatible with LightRAG & LangChain

## Included Extensions

| Extension              | Version              | Purpose                                |
| ---------------------- | -------------------- | -------------------------------------- |
| `pgvector`             | v0.8.2               | Vector embeddings & similarity search  |
| `age`                  | v1.7.0-rc0           | Property graph database (Cypher)       |
| `pg_textsearch`        | 1.2.0-dev            | Full-text search with BM25 ranking     |
| `pg_stat_statements`   | 1.12                 | Query analytics                        |
| `pg_trgm`              | 1.6                  | Text similarity                        |
| `uuid-ossp`            | 1.1                  | UUID generation                        |
| `zhparser` (+ SCWS)    | -                    | Chinese text segmentation & search     |

## Architecture

```text
PostgreSQL 18
├── Vector Search (pgvector)
├── Graph DB (Apache AGE)
├── Full-text Search (pg_textsearch + BM25)
│   └── Chinese Parser (zhparser + SCWS)
└── Query Monitoring (pg_stat_statements)
```

## Docker Image

Prebuilt images are published to GitHub Container Registry (GHCR):

```bash
docker pull ghcr.io/<github-owner-lowercase>/postgres-for-ai:main
```

Replace `<github-owner-lowercase>` with the lowercase GitHub repository owner that publishes the image.

### Published tags

- Pushes to `main` publish `main` and `sha-<commit>` tags
- Release tags such as `v1.2.3` publish semver tags like `1.2.3`, `1.2`, `1`, plus `latest`

### Platform support

Multi-architecture image for `linux/amd64` and `linux/arm64`.

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-github-owner>/Postgres-For-AI.git
cd Postgres-For-AI
```

### 2. Start services

```bash
export GHCR_OWNER=<github-owner-lowercase>
docker compose up -d
```

Set `GHCR_OWNER` to the lowercase GitHub owner value used by GHCR. After a release tag is published, switch to `latest` or a specific semver tag:

```bash
export GHCR_OWNER=<github-owner-lowercase>
export GHCR_TAG=latest
docker compose up -d
```

### 3. Services

| Service    | URL                       |
| ---------- | ------------------------- |
| PostgreSQL | `localhost:5432`          |
| pgAdmin    | `http://localhost:5050`   |

**Default credentials**: `admin` / `admin`, database `ai`

## Database Initialization

On first startup, `init/001_extensions.sql` automatically:

- Ensures `public` schema exists
- Installs pgvector into `public` schema (required by LightRAG)
- Enables all extensions
- Creates Chinese text search configuration `zh` using zhparser

### Verified extensions

```sql
SELECT extname, extversion FROM pg_extension ORDER BY extname;
```

```text
age                | 1.7.0
pg_stat_statements | 1.12
pg_textsearch      | 1.2.0-dev
pg_trgm            | 1.6
plpgsql            | 1.0
uuid-ossp          | 1.1
vector             | 0.8.2
```

## Example Use Cases

### Vector Search

```sql
CREATE TABLE embeddings (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(768)
);
```

### Graph Queries (Apache AGE)

```sql
SELECT * FROM cypher('graph', $$
  MATCH (n) RETURN n
$$) AS (n agtype);
```

### Chinese Full-text Search

```sql
-- The 'zh' configuration is created automatically
-- Insert test data
CREATE TABLE articles (id SERIAL PRIMARY KEY, content TEXT);
INSERT INTO articles (content) VALUES ('PostgreSQL 是一个强大的开源数据库');

-- Search using zhparser
SELECT * FROM articles
WHERE to_tsvector('zh', content) @@ to_tsquery('zh', '数据库');
```

### BM25 Full-text Search (pg_textsearch)

```sql
-- Create a BM25 index on a table
CALL paradedb.create_bm25(
  index_name => 'articles_idx',
  table_name => 'articles',
  key_field => 'id',
  text_fields => '{content: {}}'
);

-- Search with BM25 scoring
SELECT * FROM articles_idx.search('content:数据库');
```

## Designed for AI Frameworks

Tested & compatible with:

- **LightRAG**
- **LangChain**
- **LlamaIndex**
- **Custom RAG pipelines**
- **Hybrid Graph + Vector + Full-text search**

## Author

**Ling Li**
