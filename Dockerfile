FROM postgres:18.2

# Set environment variables
ENV POSTGRES_VERSION=18
ENV AGE_VERSION=PG18/v1.7.0-rc0

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    postgresql-server-dev-${POSTGRES_VERSION} \
    libkrb5-dev \
    flex \
    bison \
    libreadline-dev \
    zlib1g-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install pgvector (use generic ARMv8 target to ensure Apple Silicon compatibility)
RUN cd /tmp && \
    git clone --branch v0.8.2 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make OPTFLAGS="-O2 -fPIC" && \
    make install && \
    cd .. && \
    rm -rf pgvector

# Install Apache AGE
RUN cd /tmp && \
    git clone --branch ${AGE_VERSION} https://github.com/apache/age.git && \
    cd age && \
    make install && \
    cd .. && \
    rm -rf age

# Install pg_cron for scheduling (optional but useful for AI pipelines)
RUN cd /tmp && \
    git clone https://github.com/citusdata/pg_cron.git && \
    cd pg_cron && \
    make && \
    make install && \
    cd .. && \
    rm -rf pg_cron

# Install pg_stat_statements for query performance monitoring
RUN echo "shared_preload_libraries = 'pg_cron,pg_stat_statements'" >> /usr/share/postgresql/postgresql.conf.sample
RUN echo "cron.database_name = 'postgres'" >> /usr/share/postgresql/postgresql.conf.sample

COPY init/ /docker-entrypoint-initdb.d/

# Clean up build dependencies to reduce image size
RUN apt-get purge -y --auto-remove \
    build-essential \
    git \
    wget \
    postgresql-server-dev-${POSTGRES_VERSION} \
    cmake

# Expose PostgreSQL port
EXPOSE 5432
