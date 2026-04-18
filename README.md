# 🧠 PostgreSQL for AI

**PostgreSQL 18 with pgvector, Apache AGE, pg_cron & AI-ready extensions**

A production-ready **PostgreSQL Docker image optimized for AI workloads**, combining **vector search**, **graph queries**, and **scheduled pipelines** in a single database.

This setup is ideal for:

* **RAG (Retrieval-Augmented Generation)**
* **Hybrid Vector + Graph search**
* **AI metadata storage**
* **LLM memory & embeddings**
* **Agentic & knowledge-graph systems**

---

## 🚀 Features

✅ **PostgreSQL 18.2**
✅ **pgvector (v0.8.1)** – Vector similarity search
✅ **Apache AGE (PG18 / v1.7.0-rc0)** – Cypher graph queries
✅ **pg_cron** – Scheduled jobs inside PostgreSQL
✅ **pg_stat_statements** – Query performance monitoring
✅ **AI-friendly schema & search_path**
✅ **Plug-and-play with Docker Compose**
✅ **Compatible with LightRAG & LangChain**

---

## 📦 Included Extensions

| Extension              | Purpose                               |
| ---------------------- | ------------------------------------- |
| `pgvector`           | Vector embeddings & similarity search |
| `age`                | Property graph database (Cypher)      |
| `pg_cron`            | Background scheduling & pipelines     |
| `pg_stat_statements` | Query analytics                       |
| `pg_trgm`            | Text similarity                       |
| `uuid-ossp`          | UUID generation                       |

---

## 🧩 Architecture

```text
PostgreSQL 18
├── Vector Search (pgvector)
├── Graph DB (Apache AGE)
├── Scheduled Jobs (pg_cron)
└── Query Monitoring (pg_stat_statements)
```

---

## 🐳 Docker Image

Prebuilt images are published to GitHub Container Registry (GHCR):

```bash
docker pull ghcr.io/<github-owner-lowercase>/postgres-for-ai:main
```

Replace `<github-owner-lowercase>` with the lowercase GitHub repository owner that publishes the image. The GitHub Actions workflow lowercases the repository owner before publishing to GHCR, so forks publish to `ghcr.io/<lowercase-owner>/postgres-for-ai`.

### Published tags

* Pushes to `main` publish testable `main` and `sha-<commit>` tags
* Release tags such as `v1.2.3` publish semver tags like `1.2.3`, `1.2`, `1`, plus `latest`

### Platform support

The published image is a multi-architecture image for:

* `linux/amd64`
* `linux/arm64`

Apple Silicon Macs are intended to use the published image directly through the `linux/arm64` variant, assuming the GitHub Actions multi-architecture build completes successfully for that release.

---

## ▶️ Quick Start (Docker Compose)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-github-owner>/Postgres-For-AI.git
cd Postgres-For-AI
```

### 2️⃣ Start services

```bash
export GHCR_OWNER=<github-owner-lowercase>
docker-compose up -d
```

`docker-compose.yml` uses the published GHCR image:

```text
ghcr.io/${GHCR_OWNER}/postgres-for-ai:${GHCR_TAG:-main}
```

Set `GHCR_OWNER` to the lowercase GitHub owner value used by GHCR. By default, Compose pulls the `main` tag so it works before the first release exists. After a release tag such as `v1.2.3` has been published, switch to `latest` or a specific semver tag if you want the release image:

```bash
export GHCR_OWNER=<github-owner-lowercase>
export GHCR_TAG=latest
docker-compose up -d
```

### 3️⃣ Services exposed

| Service    | URL                       |
| ---------- | ------------------------- |
| PostgreSQL | `localhost:5432`        |
| pgAdmin    | `http://localhost:5050` |

**Default credentials**

```text
User: admin
Password: admin
Database: ai
```

---

## 🛠️ Database Initialization

On first startup, the following are automatically configured via
`init/001_extensions.sql`:

### ✅ Public schema ensured

```sql
CREATE SCHEMA IF NOT EXISTS public;
```

### ✅ pgvector installed in `public`

```sql
CREATE EXTENSION vector SCHEMA public;
```

This is required for tools like **LightRAG**, which expect:

```text
public.vector
```

### ✅ Optimized search_path

```sql
ALTER DATABASE ai SET search_path = ag_catalog, public, "$user";
```

* `ag_catalog` → Apache AGE
* `public` → pgvector compatibility

### ✅ Extensions enabled

```sql
CREATE EXTENSION age;
CREATE EXTENSION pg_cron;
CREATE EXTENSION pg_stat_statements;
CREATE EXTENSION pg_trgm;
CREATE EXTENSION "uuid-ossp";
```

---

## 🧪 Verify Installation

```sql
SELECT * FROM pg_extension;
```

Expected:

```text
vector
age
pg_cron
pg_stat_statements
pg_trgm
uuid-ossp
```

---

## 🧠 Example Use Cases

### 🔹 Vector Search

```sql
CREATE TABLE embeddings (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(768)
);
```

### 🔹 Graph Queries (Apache AGE)

```sql
SELECT * FROM cypher('graph', $$
  MATCH (n) RETURN n
$$) AS (n agtype);
```

### 🔹 Scheduled Jobs

```sql
SELECT cron.schedule(
  'nightly_cleanup',
  '0 2 * * *',
  $$DELETE FROM logs WHERE created_at < now() - interval '30 days'$$
);
```

---

## 🤖 Designed for AI Frameworks

Tested & compatible with:

* **LightRAG**
* **LangChain**
* **LlamaIndex**
* **Custom RAG pipelines**
* **Hybrid Graph + Vector search**

---

## 🧩 Why This Setup?

Most AI stacks require **multiple databases**:

* Vector DB
* Graph DB
* Relational DB
* Scheduler

👉 This project **unifies everything inside PostgreSQL**.

---

## 📌 Roadmap

* [ ] HNSW indexing examples
* [ ] AGE + pgvector hybrid queries
* [ ] Benchmark scripts
* [ ] Helm / Kubernetes support

---

## 🤝 Contributing

Contributions are welcome!

* Issues
* PRs
* Performance improvements
* AI-specific patterns

---

## ⭐ If You Find This Useful

Give the repo a ⭐ and feel free to share!

---

## 👤 Author

**Vishva Ram**
AI Engineer | Generative AI | RAG | Graph + Vector Systems

🔗 GitHub: [https://github.com/vishvaRam](https://github.com/vishvaRam)
