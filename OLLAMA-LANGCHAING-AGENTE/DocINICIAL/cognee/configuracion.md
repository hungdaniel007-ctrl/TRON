# maestro.md - Contenido de: /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration

**Extensiones procesadas:** `.md`

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/relational-databases.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Relational Databases

> Configure relational databases for metadata and state storage in Cognee

Relational databases store metadata, document information, and system state in Cognee. They track documents, chunks, and provenance (where data came from and how it's linked).

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Providers

Cognee supports two relational database options:

* **SQLite** — File-based database, works out of the box (default)
* **Postgres** — Production-ready database for multi-process concurrency

## Configuration

<Accordion title="Environment Variables">
  Set these environment variables in your `.env` file:

  * `DB_PROVIDER` — The database provider (sqlite, postgres)
  * `DB_NAME` — Database name
  * `DB_HOST` — Database host (Postgres only)
  * `DB_PORT` — Database port (Postgres only)
  * `DB_USERNAME` — Database username (Postgres only)
  * `DB_PASSWORD` — Database password (Postgres only)
</Accordion>

## Setup Guides

<AccordionGroup>
  <Accordion title="SQLite (Default)">
    SQLite is file-based and requires no additional setup. It's perfect for local development and single-user scenarios.

    ```dotenv  theme={null}
    DB_PROVIDER="sqlite"
    DB_NAME="cognee_db"
    ```

    **Installation**: SQLite is included by default with Cognee. No additional installation required.

    **Data Location**: Data is stored under the Cognee system directory. You can override the root with `SYSTEM_ROOT_DIRECTORY` in your `.env` file.
  </Accordion>

  <Accordion title="Postgres">
    Postgres is recommended for production environments, multi-process concurrency, or when you need external hosting.

    ```dotenv  theme={null}
    DB_PROVIDER="postgres"
    DB_NAME="cognee_db"
    DB_HOST="127.0.0.1"            # use host.docker.internal when running inside Docker
    DB_PORT="5432"
    DB_USERNAME="cognee"
    DB_PASSWORD="cognee"
    ```

    **Installation**: Install the Postgres extras:

    ```bash  theme={null}
    pip install "cognee[postgres]"
    # or for binary version
    pip install "cognee[postgres-binary]"
    ```

    **Docker Setup**: Use the built-in Postgres service:

    ```bash  theme={null}
    docker compose --profile postgres up -d
    ```

    **Docker Networking**: When running Cognee in Docker and Postgres on your host, set:

    ```dotenv  theme={null}
    DB_HOST="host.docker.internal"
    ```
  </Accordion>
</AccordionGroup>

## Advanced Options

<Accordion title="Migration Configuration">
  Use migration settings to extract data from a relational database and load it into the graph store.

  ```dotenv  theme={null}
  MIGRATION_DB_PROVIDER="sqlite"   # or postgres
  MIGRATION_DB_PATH="/path/to/migration/directory"
  MIGRATION_DB_NAME="migration_database.sqlite"
  # For Postgres migrations
  # MIGRATION_DB_HOST=127.0.0.1
  # MIGRATION_DB_PORT=5432
  # MIGRATION_DB_USERNAME=cognee
  # MIGRATION_DB_PASSWORD=cognee
  ```
</Accordion>

<Accordion title="Backend Access Control">
  Enable per-user dataset isolation for multi-tenant scenarios.

  ```dotenv  theme={null}
  ENABLE_BACKEND_ACCESS_CONTROL="true"
  ```

  This feature is available for both SQLite and Postgres.
</Accordion>

## Troubleshooting

<Accordion title="Common Issues">
  **Postgres Connectivity**: Verify the database is listening on `DB_HOST:DB_PORT` and credentials are correct:

  ```bash  theme={null}
  psql -h 127.0.0.1 -U cognee -d cognee_db
  ```

  **Docker Networking**: Use `host.docker.internal` for host-to-container access on macOS/Windows.

  **SQLite Concurrency**: SQLite has limited write concurrency; prefer Postgres for heavy multi-user workloads.
</Accordion>

## When to Use Each

* **SQLite**: Local development, single-user applications, simple deployments
* **Postgres**: Production environments, multi-user applications, external hosting, co-location with pgvector

<Columns cols={3}>
  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Configure vector databases for embedding storage
  </Card>

  <Card title="Graph Stores" icon="network" href="/setup-configuration/graph-stores">
    Set up graph databases for knowledge graphs
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/graph-stores.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Graph Stores

> Configure graph databases for knowledge graph storage and relationship reasoning in Cognee

Graph stores capture entities and relationships in knowledge graphs. They enable Cognee to understand structure and navigate connections between concepts, providing powerful reasoning capabilities.

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Providers

Cognee supports multiple graph store options:

* **Kuzu** — Local file-based graph database (default)
* **Kuzu-remote** — Kuzu with HTTP API access
* **Neo4j** — Production-ready graph database
* **Neptune** — Amazon Neptune cloud graph database
* **Neptune Analytics** — Amazon Neptune Analytics hybrid solution

## Configuration

<Accordion title="Environment Variables">
  Set these environment variables in your `.env` file:

  * `GRAPH_DATABASE_PROVIDER` — The graph store provider (kuzu, kuzu-remote, neo4j, neptune, neptune\_analytics)
  * `GRAPH_DATABASE_URL` — Database URL or connection string
  * `GRAPH_DATABASE_USERNAME` — Database username (optional)
  * `GRAPH_DATABASE_PASSWORD` — Database password (optional)
  * `GRAPH_DATABASE_NAME` — Database name (optional)
</Accordion>

## Setup Guides

<AccordionGroup>
  <Accordion title="Kuzu (Default)">
    Kuzu is file-based and requires no network setup. It's perfect for local development and single-user scenarios.

    ```dotenv  theme={null}
    GRAPH_DATABASE_PROVIDER="kuzu"
    # Optional: override location
    # SYSTEM_ROOT_DIRECTORY=/absolute/path/.cognee_system
    # The graph file will default to <SYSTEM_ROOT_DIRECTORY>/databases/cognee_graph_kuzu
    ```

    **Installation**: Kuzu is included by default with Cognee. No additional installation required.

    **Data Location**: The graph is stored on disk. Path defaults under the Cognee system directory and is created automatically.

    <Warning>
      **Concurrency Limitation**: Kuzu uses file-based locking and is not suitable for concurrent use from different agents or processes. For multi-agent scenarios, use Neo4j instead.
    </Warning>
  </Accordion>

  <Accordion title="Kuzu (Remote API)">
    Use Kuzu with an HTTP API when you need remote access or want to run Kuzu as a service.

    ```dotenv  theme={null}
    GRAPH_DATABASE_PROVIDER="kuzu-remote"
    GRAPH_DATABASE_URL="http://localhost:8000"
    GRAPH_DATABASE_USERNAME="<optional>"
    GRAPH_DATABASE_PASSWORD="<optional>"
    ```

    **Installation**: Requires a running Kuzu service exposing an HTTP API.
  </Accordion>

  <Accordion title="Neo4j">
    Neo4j is recommended for production environments and multi-user scenarios.

    ```dotenv  theme={null}
    ENABLE_BACKEND_ACCESS_CONTROL="true"
    GRAPH_DATABASE_PROVIDER="neo4j"
    GRAPH_DATABASE_URL="bolt://localhost:7687"
    GRAPH_DATABASE_NAME="neo4j"
    GRAPH_DATABASE_USERNAME="neo4j"
    GRAPH_DATABASE_PASSWORD="pleaseletmein"
    ```

    **Installation**: Install Neo4j extras:

    ```bash  theme={null}
    pip install "cognee[neo4j]"
    ```

    **Docker Setup**: Start the bundled Neo4j service with APOC + GDS plugins:

    ```bash  theme={null}
    docker compose --profile neo4j up -d
    ```
  </Accordion>

  <Accordion title="Neptune (Graph-only)">
    Use Amazon Neptune for cloud-based graph storage.

    ```dotenv  theme={null}
    GRAPH_DATABASE_PROVIDER="neptune"
    GRAPH_DATABASE_URL="neptune://<GRAPH_ID>"
    # AWS credentials via environment or default SDK chain
    ```

    **Installation**: Install Neptune extras:

    ```bash  theme={null}
    pip install "cognee[neptune]"
    ```

    **Note**: AWS credentials should be configured via environment variables or AWS SDK.
  </Accordion>

  <Accordion title="Neptune Analytics (Hybrid)">
    Use Amazon Neptune Analytics as a hybrid vector + graph backend.

    ```dotenv  theme={null}
    GRAPH_DATABASE_PROVIDER="neptune_analytics"
    GRAPH_DATABASE_URL="neptune-graph://<GRAPH_ID>"
    # AWS credentials via environment or default SDK chain
    ```

    **Installation**: Install Neptune extras:

    ```bash  theme={null}
    pip install "cognee[neptune]"
    ```

    **Note**: This is the same as the vector store configuration. Neptune Analytics serves both purposes.
  </Accordion>
</AccordionGroup>

## Advanced Options

<Accordion title="Backend Access Control">
  Enable per-user dataset isolation for multi-tenant scenarios.

  ```dotenv  theme={null}
  ENABLE_BACKEND_ACCESS_CONTROL="true"
  ```

  This feature is available for Kuzu and other supported graph stores.
</Accordion>

## Provider Comparison

<Accordion title="Graph Store Comparison">
  | Provider          | Setup           | Performance | Use Case              |
  | ----------------- | --------------- | ----------- | --------------------- |
  | Kuzu              | Zero setup      | Good        | Local development     |
  | Kuzu-remote       | Server required | Good        | Remote access         |
  | Neo4j             | Server required | Excellent   | Production            |
  | Neptune           | AWS required    | Excellent   | Cloud solution        |
  | Neptune Analytics | AWS required    | Excellent   | Hybrid cloud solution |
</Accordion>

## Important Considerations

<Accordion title="Data Location">
  * **Local providers** (Kuzu): Graph files are created automatically under `SYSTEM_ROOT_DIRECTORY`
  * **Remote providers** (Neo4j, Neptune): Require running services or cloud setup
  * **Path management**: Local graphs are managed automatically, no manual path configuration needed
</Accordion>

<Accordion title="Performance Notes">
  * **Kuzu**: Single-file storage with good local performance
  * **Neo4j**: Excellent for production workloads with proper indexing
  * **Neptune**: Cloud-scale performance with managed infrastructure
  * **Hybrid solutions**: Combine graph and vector capabilities in one system
</Accordion>

## Notes

* **Backend Access Control**: When enabled, Kuzu supports per-user dataset isolation
* **Path Management**: Local Kuzu databases are created automatically under the system directory
* **Cloud Integration**: Neptune providers require AWS credentials and proper IAM permissions

<Columns cols={3}>
  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Configure vector databases for embedding storage
  </Card>

  <Card title="Relational Databases" icon="database" href="/setup-configuration/relational-databases">
    Set up SQLite or Postgres for metadata storage
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/maestro.md

```
# maestro.md - Contenido de: /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration

**Extensiones procesadas:** `.md`

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/relational-databases.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Relational Databases

> Configure relational databases for metadata and state storage in Cognee

Relational databases store metadata, document information, and system state in Cognee. They track documents, chunks, and provenance (where data came from and how it's linked).

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Providers

Cognee supports two relational database options:

* **SQLite** — File-based database, works out of the box (default)
* **Postgres** — Production-ready database for multi-process concurrency

## Configuration

<Accordion title="Environment Variables">
  Set these environment variables in your `.env` file:

  * `DB_PROVIDER` — The database provider (sqlite, postgres)
  * `DB_NAME` — Database name
  * `DB_HOST` — Database host (Postgres only)
  * `DB_PORT` — Database port (Postgres only)
  * `DB_USERNAME` — Database username (Postgres only)
  * `DB_PASSWORD` — Database password (Postgres only)
</Accordion>

## Setup Guides

<AccordionGroup>
  <Accordion title="SQLite (Default)">
    SQLite is file-based and requires no additional setup. It's perfect for local development and single-user scenarios.

    ```dotenv  theme={null}
    DB_PROVIDER="sqlite"
    DB_NAME="cognee_db"
    ```

    **Installation**: SQLite is included by default with Cognee. No additional installation required.

    **Data Location**: Data is stored under the Cognee system directory. You can override the root with `SYSTEM_ROOT_DIRECTORY` in your `.env` file.
  </Accordion>

  <Accordion title="Postgres">
    Postgres is recommended for production environments, multi-process concurrency, or when you need external hosting.

    ```dotenv  theme={null}
    DB_PROVIDER="postgres"
    DB_NAME="cognee_db"
    DB_HOST="127.0.0.1"            # use host.docker.internal when running inside Docker
    DB_PORT="5432"
    DB_USERNAME="cognee"
    DB_PASSWORD="cognee"
    ```

    **Installation**: Install the Postgres extras:

    ```bash  theme={null}
    pip install "cognee[postgres]"
    # or for binary version
    pip install "cognee[postgres-binary]"
    ```

    **Docker Setup**: Use the built-in Postgres service:

    ```bash  theme={null}
    docker compose --profile postgres up -d
    ```

    **Docker Networking**: When running Cognee in Docker and Postgres on your host, set:

    ```dotenv  theme={null}
    DB_HOST="host.docker.internal"
    ```
  </Accordion>
</AccordionGroup>

## Advanced Options

<Accordion title="Migration Configuration">
  Use migration settings to extract data from a relational database and load it into the graph store.

  ```dotenv  theme={null}
  MIGRATION_DB_PROVIDER="sqlite"   # or postgres
  MIGRATION_DB_PATH="/path/to/migration/directory"
  MIGRATION_DB_NAME="migration_database.sqlite"
  # For Postgres migrations
  # MIGRATION_DB_HOST=127.0.0.1
  # MIGRATION_DB_PORT=5432
  # MIGRATION_DB_USERNAME=cognee
  # MIGRATION_DB_PASSWORD=cognee
  ```
</Accordion>

<Accordion title="Backend Access Control">
  Enable per-user dataset isolation for multi-tenant scenarios.

  ```dotenv  theme={null}
  ENABLE_BACKEND_ACCESS_CONTROL="true"
  ```

  This feature is available for both SQLite and Postgres.
</Accordion>

## Troubleshooting

<Accordion title="Common Issues">
  **Postgres Connectivity**: Verify the database is listening on `DB_HOST:DB_PORT` and credentials are correct:

  ```bash  theme={null}
  psql -h 127.0.0.1 -U cognee -d cognee_db
  ```

  **Docker Networking**: Use `host.docker.internal` for host-to-container access on macOS/Windows.

  **SQLite Concurrency**: SQLite has limited write concurrency; prefer Postgres for heavy multi-user workloads.
</Accordion>

## When to Use Each

* **SQLite**: Local development, single-user applications, simple deployments
* **Postgres**: Production environments, multi-user applications, external hosting, co-location with pgvector

<Columns cols={3}>
  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Configure vector databases for embedding storage
  </Card>

  <Card title="Graph Stores" icon="network" href="/setup-configuration/graph-stores">
    Set up graph databases for knowledge graphs
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/graph-stores.md

```

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/community-maintained/falkordb.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# FalkorDB

> Use FalkorDB as both a graph and vector store (hybrid store) through a community-maintained adapter

FalkorDB is an open-source graph database optimized for GraphRAG.
It supports both cloud-hosted and self-hosted deployments.

<Note>
  Cognee can use FalkorDB as both a [vector store](/setup-configuration/vector-stores) and a
  [graph store](/setup-configuration/graph-stores) backend through this
  [community-maintained](/setup-configuration/community-maintained/overview) [adapter](https://github.com/topoteretes/cognee-community/tree/main/packages/hybrid/falkordb).
</Note>

## Installation

This adapter is a separate package from core Cognee.
Before installing, complete the [Cognee installation](/getting-started/installation) and ensure
your environment is configured with [LLM and embedding providers](/setup-configuration/overview).
After that, install the adapter package:

```bash  theme={null}
uv pip install cognee-community-hybrid-adapter-falkor
```

## Configuration

Run a local FalkorDB instance:

```bash  theme={null}
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge
```

Configure in Python:

```python  theme={null}
from cognee_community_hybrid_adapter_falkor import register
from cognee import config

config.set_vector_db_config(
        {
            "vector_db_provider": "falkor",
            "vector_db_url": "localhost",
            "vector_db_port": 6379,
        }
    )
config.set_graph_db_config(
    {
        "graph_database_provider": "falkor",
        "graph_database_url": "localhost",
        "graph_database_port": 6379,
    }
)
```

Or via environment variables:

```dotenv  theme={null}
VECTOR_DB_PROVIDER="falkor"
VECTOR_DB_URL="http://localhost:6379"
VECTOR_DB_KEY=""

GRAPH_DATABASE_PROVIDER="falkor"
GRAPH_DATABASE_URL="localhost"
GRAPH_DATABASE_PORT="6379"
```

## Important Notes

<Accordion title="Adapter Registration">
  Import `register` from the adapter package before using FalkorDB with Cognee. This registers the adapter with Cognee's provider system.
</Accordion>

<Accordion title="Embedding Dimensions">
  Ensure `EMBEDDING_DIMENSIONS` matches your embedding model. See [Embedding Providers](/setup-configuration/embedding-providers) for configuration.

  Changing dimensions requires recreating collections or running `prune.prune_system()`.
</Accordion>

## Resources

<CardGroup cols={3}>
  <Card title="FalkorDB Docs" icon="book" href="https://docs.falkordb.com/">
    Official documentation
  </Card>

  <Card title="Adapter Source" icon="github" href="https://github.com/topoteretes/cognee-community/tree/main/packages/hybrid/falkordb">
    GitHub repository
  </Card>

  <Card title="Extended Example" icon="lightbulb" href="https://github.com/topoteretes/cognee-community/tree/main/packages/hybrid/falkordb/examples/example.py">
    FAQ docs assistant example.
  </Card>
</CardGroup>

<Columns cols={3}>
  <Card title="Graph Stores" icon="database" href="/setup-configuration/graph-stores">
    Official vector providers
  </Card>

  <Card title="Community Overview" icon="users" href="/setup-configuration/community-maintained/overview">
    All community integrations
  </Card>

  <Card title="Setup Overview" icon="settings" href="/setup-configuration/overview">
    Configuration guide
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/community-maintained/redis.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Redis

> Use Redis as a vector store through a community-maintained adapter

Redis is a fast in-memory data store that supports vector similarity search through the Redis Search module. It supports both cloud-hosted (Redis Cloud) and self-hosted deployments.

<Note>
  Cognee can use Redis as a [vector store](/setup-configuration/vector-stores) backend through this [community-maintained](/setup-configuration/community-maintained/overview) [adapter](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/redis).
</Note>

## Installation

This adapter is a separate package from core Cognee. Before installing, complete the [Cognee installation](/getting-started/installation) and ensure your environment is configured with [LLM and embedding providers](/setup-configuration/overview). After that, install the adapter package:

```bash  theme={null}
uv pip install cognee-community-vector-adapter-redis
```

## Configuration

<Tabs>
  <Tab title="Docker (Local)">
    Run a local Redis instance with the Search module enabled:

    ```bash  theme={null}
    docker run -d --name redis -p 6379:6379 redis:8.0.2
    ```

    Configure in Python:

    ```python  theme={null}
    from cognee_community_vector_adapter_redis import register
    from cognee import config

    config.set_vector_db_config({
        "vector_db_provider": "redis",
        "vector_db_url": "redis://localhost:6379",
    })
    ```

    Or via environment variables:

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="redis"
    VECTOR_DB_URL="redis://localhost:6379"
    ```
  </Tab>

  <Tab title="Redis Cloud">
    Get your connection URL from the [Redis Cloud](https://redis.io/try-free) dashboard. Make sure to enable the Search module.

    ```python  theme={null}
    from cognee_community_vector_adapter_redis import register
    from cognee import config

    config.set_vector_db_config({
        "vector_db_provider": "redis",
        "vector_db_url": "redis://user:password@your-redis-cloud-url:port",
    })
    ```

    Or via environment variables:

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="redis"
    VECTOR_DB_URL="redis://user:password@your-redis-cloud-url:port"
    ```
  </Tab>

  <Tab title="Redis with SSL">
    For secure connections, use the `rediss://` protocol:

    ```python  theme={null}
    from cognee_community_vector_adapter_redis import register
    from cognee import config

    config.set_vector_db_config({
        "vector_db_provider": "redis",
        "vector_db_url": "rediss://localhost:6380",
    })
    ```

    Or via environment variables:

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="redis"
    VECTOR_DB_URL="rediss://localhost:6380"
    ```
  </Tab>
</Tabs>

## Important Notes

<Accordion title="Adapter Registration">
  Import `register` from the adapter package before using Redis with Cognee. This registers the adapter with Cognee's provider system.
</Accordion>

<Accordion title="Troubleshooting">
  1. **Connection Errors**: Ensure Redis is running and accessible at the specified URL
  2. **Search Module Missing**: Make sure Redis has the Search module enabled
  3. **Embedding Dimension Mismatch**: Verify embedding engine dimensions match index configuration
  4. **Collection Not Found**: Always create collections before adding data points
</Accordion>

## Resources

<CardGroup cols={3}>
  <Card title="RedisVL Docs" icon="book" href="https://docs.redisvl.com">
    RedisVL library documentation (powers this adapter)
  </Card>

  <Card title="Adapter Source" icon="github" href="https://github.com/topoteretes/cognee-community/tree/main/packages/vector/redis">
    GitHub repository
  </Card>

  <Card title="Extended Example" icon="lightbulb" href="https://github.com/topoteretes/cognee-community/blob/main/packages/vector/redis/examples/example.py">
    Full usage example script
  </Card>
</CardGroup>

<Columns cols={3}>
  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Official vector providers
  </Card>

  <Card title="Community Overview" icon="users" href="/setup-configuration/community-maintained/overview">
    All community integrations
  </Card>

  <Card title="Setup Overview" icon="settings" href="/setup-configuration/overview">
    Configuration guide
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/community-maintained/qdrant.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Qdrant

> Use Qdrant as a vector store through a community-maintained adapter

Qdrant is a vector search engine that stores embeddings and performs similarity searches. It supports both cloud-hosted and self-hosted deployments.

<Note>
  Cognee can use Qdrant as a [vector store](/setup-configuration/vector-stores) backend through this [community-maintained](/setup-configuration/community-maintained/overview) [adapter](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/qdrant).
</Note>

## Installation

This adapter is a separate package from core Cognee. Before installing, complete the [Cognee installation](/getting-started/installation) and ensure your environment is configured with [LLM and embedding providers](/setup-configuration/overview). After that, install the adapter package:

```bash  theme={null}
uv pip install cognee-community-vector-adapter-qdrant
```

## Configuration

<Tabs>
  <Tab title="Docker (Local)">
    Run a local Qdrant instance:

    ```bash  theme={null}
    docker run -p 6333:6333 -p 6334:6334 \
        -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
        qdrant/qdrant
    ```

    Configure in Python:

    ```python  theme={null}
    from cognee_community_vector_adapter_qdrant import register
    from cognee import config

    config.set_vector_db_config({
        "vector_db_provider": "qdrant",
        "vector_db_url": "http://localhost:6333",
        "vector_db_key": "",
    })
    ```

    Or via environment variables:

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="qdrant"
    VECTOR_DB_URL="http://localhost:6333"
    VECTOR_DB_KEY=""
    ```
  </Tab>

  <Tab title="Qdrant Cloud">
    Get your API key and URL from the [Qdrant Cloud](https://qdrant.tech/documentation/cloud/) dashboard.

    ```python  theme={null}
    from cognee_community_vector_adapter_qdrant import register
    from cognee import config

    config.set_vector_db_config({
        "vector_db_provider": "qdrant",
        "vector_db_url": "https://your-cluster.qdrant.io",
        "vector_db_key": "your_api_key",
    })
    ```

    Or via environment variables:

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="qdrant"
    VECTOR_DB_URL="https://your-cluster.qdrant.io"
    VECTOR_DB_KEY="your_api_key"
    ```
  </Tab>
</Tabs>

## Important Notes

<Accordion title="Embedding Dimensions">
  Ensure `EMBEDDING_DIMENSIONS` matches your embedding model. See [Embedding Providers](/setup-configuration/embedding-providers) for configuration.

  Changing dimensions requires recreating collections or running `prune.prune_system()`.
</Accordion>

## Resources

<CardGroup cols={3}>
  <Card title="Qdrant Docs" icon="book" href="https://qdrant.tech/documentation/">
    Official documentation
  </Card>

  <Card title="Adapter Source" icon="github" href="https://github.com/topoteretes/cognee-community/tree/main/packages/vector/qdrant">
    GitHub repository
  </Card>

  <Card title="Extended Example" icon="lightbulb" href="https://github.com/topoteretes/cognee-community/tree/main/packages/vector/qdrant/example.py">
    FAQ docs assistant example.
  </Card>
</CardGroup>

<Columns cols={3}>
  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Official vector providers
  </Card>

  <Card title="Community Overview" icon="users" href="/setup-configuration/community-maintained/overview">
    All community integrations
  </Card>

  <Card title="Setup Overview" icon="settings" href="/setup-configuration/overview">
    Configuration guide
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/community-maintained/overview.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Adapters Overview

> Adapters and extensions built by the Cognee community

Community-maintained integrations are adapters built and maintained by the Cognee community. These extend Cognee's functionality with additional providers and services.

<Note>
  Community integrations are maintained separately from the core Cognee package. For issues or contributions, visit the [cognee-community repository](https://github.com/topoteretes/cognee-community).
</Note>

## Available Integrations

### Vector Stores

* **[Qdrant](/setup-configuration/community-maintained/qdrant)** — High-performance vector search engine
* **[Redis](/setup-configuration/community-maintained/redis)** — Fast vector similarity search via Redis Search module
* **[Milvus](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/milvus)** — Cloud-native vector database (docs coming soon)
* **[Pinecone](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/pinecone)** — Managed vector database (docs coming soon)
* **[Weaviate](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/weaviate)** — Open-source vector search engine (docs coming soon)
* **[Azure AI Search](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/azureaisearch)** — Azure cognitive search service (docs coming soon)
* **[OpenSearch](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/opensearch)** — OpenSearch vector engine (docs coming soon)

### Hybrid Stores

* **[DuckDB](https://github.com/topoteretes/cognee-community/tree/main/packages/hybrid/duckdb)** — In-process analytical database (docs coming soon)
* **[FalkorDB](/setup-configuration/community-maintained/falkordb)** — Graph database with vector support (docs coming soon)

### Graph Stores

* **[Memgraph](https://github.com/topoteretes/cognee-community/tree/main/packages/graph/memgraph)** — In-memory graph database (docs coming soon)
* **[NetworkX](https://github.com/topoteretes/cognee-community/tree/main/packages/graph/networkx)** — Python graph library adapter (docs coming soon)

### Observability

* **[KeywordsAI](https://github.com/topoteretes/cognee-community/tree/main/packages/observability/keywordsai)** — LLM monitoring and analytics (docs coming soon)

## Contributing

To contribute a new community integration:

1. Fork the [cognee-community repository](https://github.com/topoteretes/cognee-community)
2. Follow the adapter development guide
3. Submit a pull request with your integration
4. Add documentation following the existing patterns

## Support

For community integration support:

* Check the integration's README in the repository
* Open issues in the cognee-community repository
* Join the [Discord community](https://discord.gg/cqF6RhDYWz) for help

<Columns cols={2}>
  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Official vector store providers
  </Card>

  <Card title="Setup Overview" icon="settings" href="/setup-configuration/overview">
    Configuration overview
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/vector-stores.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Vector Stores

> Configure vector databases for embedding storage and semantic search in Cognee

Vector stores hold embeddings for semantic similarity search. They enable Cognee to find conceptually related content based on meaning rather than exact text matches.

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Providers

Cognee supports multiple vector store options:

* **LanceDB** — File-based vector store, works out of the box (default)
* **PGVector** — Postgres-backed vector storage with pgvector extension
* **Qdrant** — High-performance vector database and similarity search engine
* **Redis** — Fast vector similarity search via Redis Search module
* **ChromaDB** — HTTP server-based vector database
* **FalkorDB** — Hybrid graph + vector database
* **Neptune Analytics** — Amazon Neptune Analytics hybrid solution

## Configuration

<Accordion title="Environment Variables">
  Set these environment variables in your `.env` file:

  * `VECTOR_DB_PROVIDER` — The vector store provider (lancedb, pgvector, qdrant, redis, chromadb, falkordb, neptune\_analytics)
  * `VECTOR_DB_URL` — Database URL or connection string
  * `VECTOR_DB_KEY` — Authentication key (provider-specific)
  * `VECTOR_DB_PORT` — Database port (for some providers)
</Accordion>

## Setup Guides

<AccordionGroup>
  <Accordion title="LanceDB (Default)">
    LanceDB is file-based and requires no additional setup. It's perfect for local development and single-user scenarios.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="lancedb"
    # Optional, can be a path or URL. Defaults to <SYSTEM_ROOT_DIRECTORY>/databases/cognee.lancedb
    # VECTOR_DB_URL=/absolute/or/relative/path/to/cognee.lancedb
    ```

    **Installation**: LanceDB is included by default with Cognee. No additional installation required.

    **Data Location**: Vectors are stored in a local directory. Defaults under the Cognee system path if `VECTOR_DB_URL` is empty.
  </Accordion>

  <Accordion title="PGVector">
    PGVector stores vectors inside your Postgres database using the pgvector extension.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="pgvector"
    # Uses the same Postgres connection as your relational DB (DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD)
    ```

    **Installation**: Install the Postgres extras:

    ```bash  theme={null}
    pip install "cognee[postgres]"
    # or for binary version
    pip install "cognee[postgres-binary]"
    ```

    **Docker Setup**: Use the built-in Postgres with pgvector:

    ```bash  theme={null}
    docker compose --profile postgres up -d
    ```

    **Note**: If using your own Postgres, ensure `CREATE EXTENSION IF NOT EXISTS vector;` is available in the target database.
  </Accordion>

  <Accordion title="Qdrant">
    Qdrant requires a running instance of the Qdrant server.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="qdrant"
    VECTOR_DB_URL="http://localhost:6333"
    ```

    **Installation**: Since Qdrant is a community adapter, you have to install the community package:

    ```bash  theme={null}
    pip install cognee-community-vector-adapter-qdrant
    ```

    **Configuration**: To make sure Cognee uses Qdrant, you have to register it beforehand with the following line:

    ```python  theme={null}
    from cognee_community_vector_adapter_qdrant import register
    ```

    For more details on setting up Qdrant, visit the [more detailed description](/setup-configuration/community-maintained/qdrant) of this adapter.

    **Docker Setup**: Start the Qdrant service:

    ```bash  theme={null}
    docker run -p 6333:6333 -p 6334:6334 \
        -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
        qdrant/qdrant
    ```

    **Access**: Default port is 6333 for the database, and you can access the Qdrant dashboard at "localhost:6333/dashboard".
  </Accordion>

  <Accordion title="Redis">
    Redis can be used as a vector store through the Redis Search module, providing fast vector similarity search capabilities.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="redis"
    VECTOR_DB_URL="redis://localhost:6379"
    # VECTOR_DB_KEY is optional and not used by Redis
    ```

    **Installation**: Since Redis is a community adapter, you have to install the community package:

    ```bash  theme={null}
    pip install cognee-community-vector-adapter-redis
    ```

    **Configuration**: To make sure Cognee uses Redis, you have to register it beforehand with the following line:

    ```python  theme={null}
    from cognee_community_vector_adapter_redis import register
    ```

    You can also configure Redis programmatically:

    ```python  theme={null}
    from cognee import config

    config.set_vector_db_config({
        "vector_db_provider": "redis",
        "vector_db_url": "redis://localhost:6379",
    })
    ```

    For more details on setting up Redis, visit the [more detailed description](/setup-configuration/community-maintained/redis) of this adapter.

    **Docker Setup**: Start a Redis instance with Search module enabled:

    ```bash  theme={null}
    docker run -d --name redis -p 6379:6379 redis:8.0.2
    ```

    Or use **Redis Cloud** with the Search module enabled: [Redis Cloud](https://redis.io/try-free)

    **Connection URL Examples**:

    * Local: `redis://localhost:6379`
    * With authentication: `redis://user:password@localhost:6379`
    * With SSL: `rediss://localhost:6380`
  </Accordion>

  <Accordion title="ChromaDB">
    ChromaDB requires a running Chroma server and authentication token.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="chromadb"
    VECTOR_DB_URL="http://localhost:3002"
    VECTOR_DB_KEY="<your_token>"
    ```

    **Installation**: Install ChromaDB extras:

    ```bash  theme={null}
    pip install "cognee[chromadb]"
    # or directly
    pip install chromadb
    ```

    **Docker Setup**: Start the bundled ChromaDB server:

    ```bash  theme={null}
    docker compose --profile chromadb up -d
    ```
  </Accordion>

  <Accordion title="FalkorDB">
    FalkorDB can serve as both graph and vector store, providing a hybrid solution.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="falkordb"
    VECTOR_DB_URL="localhost"
    VECTOR_DB_PORT="6379"
    ```

    **Installation**: Since FalkorDB is a community adapter, you have to install the community package:

    ```bash  theme={null}
    pip install cognee-community-hybrid-adapter-falkor
    ```

    **Configuration**: To make sure Cognee uses FalkorDB, you have to register it beforehand with the following line:

    ```python  theme={null}
    from cognee_community_hybrid_adapter_falkor import register
    ```

    For more details on setting up FalkorDB, visit the [more detailed description](/setup-configuration/community-maintained/falkordb) of this adapter.

    **Docker Setup**: Start the FalkorDB service:

    ```bash  theme={null}
    docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge
    ```

    **Access**: Default ports are 6379 (DB) and 3000 (UI).
  </Accordion>

  <Accordion title="Neptune Analytics">
    Use Amazon Neptune Analytics as a hybrid vector + graph backend.

    ```dotenv  theme={null}
    VECTOR_DB_PROVIDER="neptune_analytics"
    VECTOR_DB_URL="neptune-graph://<GRAPH_ID>"
    # AWS credentials via environment or default SDK chain
    ```

    **Installation**: Install Neptune extras:

    ```bash  theme={null}
    pip install "cognee[neptune]"
    ```

    **Note**: URL must start with `neptune-graph://` and AWS credentials should be configured via environment variables or AWS SDK.
  </Accordion>
</AccordionGroup>

## Important Considerations

<Accordion title="Dimension Consistency">
  Ensure `EMBEDDING_DIMENSIONS` matches your vector store collection/table schemas:

  * PGVector column size
  * LanceDB Vector size
  * ChromaDB collection schema

  Changing dimensions requires recreating collections.
</Accordion>

<Accordion title="Provider Comparison">
  | Provider          | Setup             | Performance | Use Case                       |
  | ----------------- | ----------------- | ----------- | ------------------------------ |
  | LanceDB           | Zero setup        | Good        | Local development              |
  | PGVector          | Postgres required | Excellent   | Production with Postgres       |
  | Qdrant            | Server required   | Excellent   | High-performance vector search |
  | Redis             | Server required   | Excellent   | Low-latency in-memory search   |
  | ChromaDB          | Server required   | Good        | Dedicated vector store         |
  | FalkorDB          | Server required   | Good        | Hybrid graph + vector          |
  | Neptune Analytics | AWS required      | Excellent   | Cloud hybrid solution          |
</Accordion>

## Community-Maintained Providers

Additional vector stores are available through community-maintained adapters:

* **[Qdrant](/setup-configuration/community-maintained/qdrant)** — Vector search engine with cloud and self-hosted options
* **[Redis](/setup-configuration/community-maintained/redis)** — Fast vector similarity search
* **[FalkorDB](/setup-configuration/community-maintained/falkordb)** — Hybrid vector and graph store
* **Milvus, Pinecone, Weaviate, and more** — See [all community adapters](/setup-configuration/community-maintained/overview)

## Notes

* **Embedding Integration**: Vector stores use your embedding engine from the Embeddings section
* **Dimension Matching**: Keep `EMBEDDING_DIMENSIONS` consistent between embedding provider and vector store
* **Performance**: Local providers (LanceDB) are simpler but cloud providers offer better scalability

<Columns cols={3}>
  <Card title="Embedding Providers" icon="layers" href="/setup-configuration/embedding-providers">
    Configure embedding providers for vector generation
  </Card>

  <Card title="Graph Stores" icon="network" href="/setup-configuration/graph-stores">
    Set up graph databases for knowledge graphs
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/permissions.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Permissions Setup

> Configure Cognee's permission system and access control

Enable Cognee's permission system for data isolation and access control. For detailed concepts, see [Cognee Permissions System](/core-concepts/multi-user-mode/permissions-system/overview).

## Enable Permission System

Set the environment variable to enable access control:

```dotenv  theme={null}
ENABLE_BACKEND_ACCESS_CONTROL=true
REQUIRE_AUTHENTICATION=true
```

<Warning>
  **Database Override**: Permission mode enforces Kùzu (graph) and LanceDB (vector). Custom providers are ignored.
</Warning>

## Database Setup

Choose your relational database:

* **SQLite** — Local development (auto-creates files)
* **Postgres** — Production (requires manual setup)

See [Relational Databases](./relational-databases) for detailed configuration.

## Authentication

### API Server

Start the server with authentication:

```bash  theme={null}
uvicorn cognee.api.client:app --host 0.0.0.0 --port 8000
```

**Default credentials (development only):**

* Username: `default_user@example.com`
* Password: `default_password`

### Programmatic Access

See [Permission Snippets](/guides/permission-snippets) for complete programmatic examples.

## Data Organization

Data is automatically organized by user and dataset. Each user gets isolated storage:

```
.cognee_system/databases/<user_uuid>/
├── <dataset_uuid>.pkl         # Kùzu graph database
└── <dataset_uuid>.lance.db/   # LanceDB vector database
```

## Troubleshooting

**Permission Denied**: Verify user has required permission on the dataset.

**Data Isolation**: Check per-user database files exist:

```bash  theme={null}
ls -la .cognee_system/databases/<user_uuid>/
```

**Database Conflicts**: Custom providers are ignored in permission mode.

<Columns cols={2}>
  <Card title="Permission System" icon="brain" href="/core-concepts/multi-user-mode/permissions-system/overview">
    Learn about users, tenants, roles, and ACL
  </Card>

  <Card title="Usage Guide" icon="book-open" href="/guides/permission-snippets">
    How to use permission features
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/llm-providers.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# LLM Providers

> Configure LLM providers for text generation and reasoning in Cognee

LLM (Large Language Model) providers handle text generation, reasoning, and structured output tasks in Cognee. You can choose from cloud providers like OpenAI and Anthropic, or run models locally with Ollama.

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Providers

Cognee supports multiple LLM providers:

* **OpenAI** — GPT models via OpenAI API (default)
* **Azure OpenAI** — GPT models via Azure OpenAI Service
* **Google Gemini** — Gemini models via Google AI
* **Anthropic** — Claude models via Anthropic API
* **AWS Bedrock** — Models available via AWS Bedrock
* **Ollama** — Local models via Ollama
* **LM Studio** — Local models via LM Studio
* **Custom** — OpenAI-compatible endpoints (like vLLM)

<Warning>
  **LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.
</Warning>

## Configuration

<Accordion title="Environment Variables">
  Set these environment variables in your `.env` file:

  * `LLM_PROVIDER` — The provider to use (openai, gemini, anthropic, ollama, custom)
  * `LLM_MODEL` — The specific model to use
  * `LLM_API_KEY` — Your API key for the provider
  * `LLM_ENDPOINT` — Custom endpoint URL (for Azure, Ollama, or custom providers)
  * `LLM_API_VERSION` — API version (for Azure OpenAI)
  * `LLM_MAX_TOKENS` — Maximum tokens per request (optional)
</Accordion>

## Provider Setup Guides

<AccordionGroup>
  <Accordion title="OpenAI (Default)">
    OpenAI is the default provider and works out of the box with minimal configuration.

    ```dotenv  theme={null}
    LLM_PROVIDER="openai"
    LLM_MODEL="gpt-4o-mini"
    LLM_API_KEY="sk-..."
    # Optional overrides
    # LLM_ENDPOINT=https://api.openai.com/v1
    # LLM_API_VERSION=
    # LLM_MAX_TOKENS=16384
    ```
  </Accordion>

  <Accordion title="Azure OpenAI">
    Use Azure OpenAI Service with your own deployment.

    ```dotenv  theme={null}
    LLM_PROVIDER="openai"
    LLM_MODEL="azure/gpt-4o-mini"
    LLM_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/gpt-4o-mini"
    LLM_API_KEY="az-..."
    LLM_API_VERSION="2024-12-01-preview"
    ```
  </Accordion>

  <Accordion title="Google Gemini">
    Use Google's Gemini models for text generation.

    ```dotenv  theme={null}
    LLM_PROVIDER="gemini"
    LLM_MODEL="gemini/gemini-2.0-flash"
    LLM_API_KEY="AIza..."
    # Optional
    # LLM_ENDPOINT=https://generativelanguage.googleapis.com/
    # LLM_API_VERSION=v1beta
    ```
  </Accordion>

  <Accordion title="Anthropic">
    Use Anthropic's Claude models for reasoning tasks.

    ```dotenv  theme={null}
    LLM_PROVIDER="anthropic"
    LLM_MODEL="claude-3-5-sonnet-20241022"
    LLM_API_KEY="sk-ant-..."
    ```
  </Accordion>

  <Accordion title="AWS Bedrock">
    Use models available on AWS Bedrock for various tasks. For Bedrock specifically, you will need to
    also specify some information regarding AWS.

    ```dotenv  theme={null}
    LLM_API_KEY="<your_bedrock_api_key>"
    LLM_MODEL="eu.amazon.nova-lite-v1:0"
    LLM_PROVIDER="bedrock"
    LLM_MAX_TOKENS="16384"
    AWS_REGION="<your_aws_region>"
    AWS_ACCESS_KEY_ID="<your_aws_access_key_id>"
    AWS_SECRET_ACCESS_KEY="<your_aws_secret_access_key>"
    AWS_SESSION_TOKEN="<your_aws_session_token>"

    # Optional parameters
    #AWS_BEDROCK_RUNTIME_ENDPOINT="bedrock-runtime.eu-west-1.amazonaws.com"
    #AWS_PROFILE_NAME="<path_to_your_aws_credentials_file>"
    ```

    There are **multiple ways of connecting** to Bedrock models:

    1. Using an API key and region. Simply generate you key on AWS, and put it in the `LLM_API_KEY` env variable.
    2. Using AWS Credentials. You can only specify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, no need for the `LLM_API_KEY`.
       In this case, if you are using temporary credentials (e.g. `AWS_ACCESS_KEY_ID` starting with `ASIA...`), then you also
       must specify the `AWS_SESSION_TOKEN`.
    3. Using AWS profiles. Create a file called something like `/.aws/credentials`, and store your credentials inside it.

    **Installation**: Install the required dependency:

    ```bash  theme={null}
    pip install cognee[aws]
    ```

    <Info>
      **Model Name**
      The name of the model might differ based on the region (the name begins with **eu** for Europe, **us** of USA, etc.)
    </Info>
  </Accordion>

  <Accordion title="Ollama (Local)">
    Run models locally with Ollama for privacy and cost control.

    ```dotenv  theme={null}
    LLM_PROVIDER="ollama"
    LLM_MODEL="llama3.1:8b"
    LLM_ENDPOINT="http://localhost:11434/v1"
    LLM_API_KEY="ollama"
    ```

    **Installation**: Install Ollama from [ollama.ai](https://ollama.ai) and pull your desired model:

    ```bash  theme={null}
    ollama pull llama3.1:8b
    ```

    ### Known Issues

    * **Requires `HUGGINGFACE_TOKENIZER`**: Ollama currently needs this env var set even when used only as LLM. Fix in progress.
    * **`NoDataError` with mixed providers**: Using Ollama as LLM and OpenAI as embedding provider may fail with `NoDataError`. Workaround: use the same provider for both.
  </Accordion>

  <Accordion title="LM Studio (Local)">
    Run models locally with LM Studio for privacy and cost control.

    ```dotenv  theme={null}
    LLM_PROVIDER="custom"
    LLM_MODEL="lm_studio/magistral-small-2509"
    LLM_ENDPOINT="http://127.0.0.1:1234/v1"
    LLM_API_KEY="."
    LLM_INSTRUCTOR_MODE="json_schema_mode"
    ```

    **Installation**: Install LM Studio from [lmstudio.ai](https://lmstudio.ai/) and download your desired model from
    LM Studio's interface.
    Load your model, start the LM Studio server, and Cognee will be able to connect to it.

    <Info>
      **Set up instructor mode**
      The `LLM_INSTRUCTOR_MODE` env variable controls the LiteLLM instructor [mode](https://python.useinstructor.com/modes-comparison/),
      i.e. the model's response type.
      This may vary depending on the model, and you would need to change it accordingly.
    </Info>
  </Accordion>

  <Accordion title="Custom Providers">
    Use OpenAI-compatible endpoints like OpenRouter or other services.

    ```dotenv  theme={null}
    LLM_PROVIDER="custom"
    LLM_MODEL="openrouter/google/gemini-2.0-flash-lite-preview-02-05:free"
    LLM_ENDPOINT="https://openrouter.ai/api/v1"
    LLM_API_KEY="or-..."
    # Optional fallback chain
    # FALLBACK_MODEL=
    # FALLBACK_ENDPOINT=
    # FALLBACK_API_KEY=
    ```

    **Custom Provider Prefixes**: When using `LLM_PROVIDER="custom"`, you must include the correct provider prefix in your model name. Cognee forwards requests to [LiteLLM](https://docs.litellm.ai/docs/providers), which uses these prefixes to route requests correctly.

    Common prefixes include:

    * `hosted_vllm/` — vLLM servers
    * `openrouter/` — OpenRouter
    * `lm_studio/` — LM Studio
    * `openai/` — OpenAI-compatible APIs

    See the [LiteLLM providers documentation](https://docs.litellm.ai/docs/providers) for the full list of supported prefixes.

    Below is an example for vLLm:

    <Accordion title="vLLM">
      Use vLLM for high-performance model serving with OpenAI-compatible API.

      ```dotenv  theme={null}
      LLM_PROVIDER="custom"
      LLM_MODEL="hosted_vllm/<your-model-name>"
      LLM_ENDPOINT="https://your-vllm-endpoint/v1"
      LLM_API_KEY="."
      ```

      **Example with Gemma:**

      ```dotenv  theme={null}
      LLM_PROVIDER="custom"
      LLM_MODEL="hosted_vllm/gemma-3-12b"
      LLM_ENDPOINT="https://your-vllm-endpoint/v1"
      LLM_API_KEY="."
      ```

      <Warning>
        **Important**: The `hosted_vllm/` prefix is required for LiteLLM to correctly route requests to your vLLM server. The model name after the prefix should match the model ID returned by your vLLM server's `/v1/models` endpoint.
      </Warning>

      To find the correct model name, see [their documentation](https://docs.litellm.ai/docs/providers/vllm).
    </Accordion>
  </Accordion>
</AccordionGroup>

## Advanced Options

<Accordion title="Rate Limiting">
  Control client-side throttling for LLM calls to manage API usage and costs.

  **Configuration (in .env):**

  ```dotenv  theme={null}
  LLM_RATE_LIMIT_ENABLED="true"
  LLM_RATE_LIMIT_REQUESTS="60"
  LLM_RATE_LIMIT_INTERVAL="60"
  ```

  **How it works:**

  * **Client-side limiter**: Cognee paces outbound LLM calls before they reach the provider
  * **Moving window**: Spreads allowance across the time window for smoother throughput
  * **Per-process scope**: In-memory limits don't share across multiple processes/containers
  * **Auto-applied**: Works with all providers (OpenAI, Gemini, Anthropic, Ollama, Custom)

  **Example**: `60` requests per `60` seconds ≈ 1 request/second average rate.
</Accordion>

## Notes

* If `EMBEDDING_API_KEY` is not set, Cognee falls back to `LLM_API_KEY` for embeddings
* Rate limiting helps manage API usage and costs
* Structured output frameworks ensure consistent data extraction from LLM responses
* If you are using `Instructor` as the structured output framework, you can control the
  response type of the LLM through the `LLM_INSTRUCTOR_MODE` env variable, which sets the
  corresponding instructor [mode](https://python.useinstructor.com/modes-comparison/)
  (e.g. `json_mode` for JSON output)

<Columns cols={3}>
  <Card title="Embedding Providers" icon="layers" href="/setup-configuration/embedding-providers">
    Configure embedding providers for semantic search
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>

  <Card title="Relational Databases" icon="database" href="/setup-configuration/relational-databases">
    Set up SQLite or Postgres for metadata storage
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/structured-output-backends.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Structured Output Backends

> Configure structured output frameworks for reliable data extraction in Cognee

Structured output backends ensure reliable data extraction from LLM responses. Cognee supports two frameworks that convert LLM text into structured Pydantic models for knowledge graph extraction and other tasks.

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Frameworks

Cognee supports two structured output approaches:

* **LiteLLM + Instructor** — Provider-agnostic client with Pydantic coercion (default)
* **BAML** — DSL-based framework with type registry and guardrails

Both frameworks produce the same Pydantic-validated outputs, so your application code remains unchanged regardless of which backend you choose.

## How It Works

Cognee uses a unified interface that abstracts the underlying framework:

```python  theme={null}
from cognee.infrastructure.llm.LLMGateway import LLMGateway
await LLMGateway.acreate_structured_output(text, system_prompt, response_model)
```

The `STRUCTURED_OUTPUT_FRAMEWORK` environment variable determines which backend processes your requests, but the API remains identical.

## Configuration

<Tabs>
  <Tab title="LiteLLM + Instructor (Default)">
    ```dotenv  theme={null}
    STRUCTURED_OUTPUT_FRAMEWORK=instructor
    ```
  </Tab>

  <Tab title="BAML">
    ```dotenv  theme={null}
    STRUCTURED_OUTPUT_FRAMEWORK=baml
    ```
  </Tab>
</Tabs>

## Important Notes

* **Unified Interface**: Your application code uses the same `acreate_structured_output()` call regardless of framework
* **Provider Flexibility**: Both frameworks support the same LLM providers
* **Output Consistency**: Both produce identical Pydantic-validated results
* **Performance**: Framework choice doesn't significantly impact performance

<Columns cols={3}>
  <Card title="LLM Providers" icon="brain" href="/setup-configuration/llm-providers">
    Configure LLM providers for text generation
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>

  <Card title="Custom Prompts" icon="text-wrap" href="/guides/custom-prompts">
    Learn about custom prompt configuration
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/embedding-providers.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Embedding Providers

> Configure embedding providers for semantic search in Cognee

Embedding providers convert text into vector representations that enable semantic search. These vectors capture the meaning of text, allowing Cognee to find conceptually related content even when the wording is different.

<Info>
  **New to configuration?**

  See the [Setup Configuration Overview](./overview) for the complete workflow:

  install extras → create `.env` → choose providers → handle pruning.
</Info>

## Supported Providers

Cognee supports multiple embedding providers:

* **OpenAI** — Text embedding models via OpenAI API (default)
* **Azure OpenAI** — Text embedding models via Azure OpenAI Service
* **Google Gemini** — Embedding models via Google AI
* **Mistral** — Embedding models via Mistral AI
* **AWS Bedrock** — Embedding models via AWS Bedrock
* **Ollama** — Local embedding models via Ollama
* **LM Studio** — Local embedding models via LM Studio
* **Fastembed** — CPU-friendly local embeddings
* **Custom** — OpenAI-compatible embedding endpoints

<Warning>
  **LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.
</Warning>

## Configuration

<Accordion title="Environment Variables">
  Set these environment variables in your `.env` file:

  * `EMBEDDING_PROVIDER` — The provider to use (openai, gemini, mistral, ollama, fastembed, custom)
  * `EMBEDDING_MODEL` — The specific embedding model to use
  * `EMBEDDING_DIMENSIONS` — The vector dimension size (must match your vector store)
  * `EMBEDDING_API_KEY` — Your API key (falls back to `LLM_API_KEY` if not set)
  * `EMBEDDING_ENDPOINT` — Custom endpoint URL (for Azure, Ollama, or custom providers)
  * `EMBEDDING_API_VERSION` — API version (for Azure OpenAI)
  * `EMBEDDING_MAX_TOKENS` — Maximum tokens per request (optional)
</Accordion>

## Provider Setup Guides

<AccordionGroup>
  <Accordion title="OpenAI (Default)">
    OpenAI provides high-quality embeddings with good performance.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="openai"
    EMBEDDING_MODEL="openai/text-embedding-3-large"
    EMBEDDING_DIMENSIONS="3072"
    # Optional
    # EMBEDDING_API_KEY=sk-...   # falls back to LLM_API_KEY if omitted
    # EMBEDDING_ENDPOINT=https://api.openai.com/v1
    # EMBEDDING_API_VERSION=
    # EMBEDDING_MAX_TOKENS=8191
    ```
  </Accordion>

  <Accordion title="Azure OpenAI Embeddings">
    Use Azure OpenAI Service for embeddings with your own deployment.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="openai"
    EMBEDDING_MODEL="azure/text-embedding-3-large"
    EMBEDDING_ENDPOINT="https://<your-az>.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large"
    EMBEDDING_API_KEY="az-..."
    EMBEDDING_API_VERSION="2023-05-15"
    EMBEDDING_DIMENSIONS="3072"
    ```
  </Accordion>

  <Accordion title="Google Gemini">
    Use Google's embedding models for semantic search.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="gemini"
    EMBEDDING_MODEL="gemini/text-embedding-004"
    EMBEDDING_API_KEY="AIza..."
    EMBEDDING_DIMENSIONS="768"
    ```
  </Accordion>

  <Accordion title="Mistral">
    Use Mistral's embedding models for high-quality vector representations.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="mistral"
    EMBEDDING_MODEL="mistral/mistral-embed"
    EMBEDDING_API_KEY="sk-mis-..."
    EMBEDDING_DIMENSIONS="1024"
    ```

    **Installation**: Install the required dependency:

    ```bash  theme={null}
    pip install mistral-common[sentencepiece]
    ```
  </Accordion>

  <Accordion title="AWS Bedrock">
    Use embedding models provided by the AWS Bedrock service.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="bedrock"
    EMBEDDING_MODEL="<your_model_name>"
    EMBEDDING_DIMENSIONS="<dimensions_of_the_model>"
    EMBEDDING_API_KEY="<your_api_key>"
    EMBEDDING_MAX_TOKENS="<max_tokens_of_your_model>"
    ```
  </Accordion>

  <Accordion title="Ollama (Local)">
    Run embedding models locally with Ollama for privacy and cost control.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="ollama"
    EMBEDDING_MODEL="nomic-embed-text:latest"
    EMBEDDING_ENDPOINT="http://localhost:11434/api/embed"
    EMBEDDING_DIMENSIONS="768"
    HUGGINGFACE_TOKENIZER="nomic-ai/nomic-embed-text-v1.5"
    ```

    **Installation**: Install Ollama from [ollama.ai](https://ollama.ai) and pull your desired embedding model:

    ```bash  theme={null}
    ollama pull nomic-embed-text:latest
    ```
  </Accordion>

  <Accordion title="LM Studio (Local)">
    Run embedding models locally with LM Studio for privacy and cost control.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="custom"
    EMBEDDING_MODEL="lm_studio/text-embedding-nomic-embed-text-1.5"
    EMBEDDING_ENDPOINT="http://127.0.0.1:1234/v1"
    EMBEDDING_API_KEY="."
    EMBEDDING_DIMENSIONS="768"
    ```

    **Installation**: Install LM Studio from [lmstudio.ai](https://lmstudio.ai/) and download your desired model from
    LM Studio's interface.
    Load your model, start the LM Studio server, and Cognee will be able to connect to it.
  </Accordion>

  <Accordion title="Fastembed (Local)">
    Use Fastembed for CPU-friendly local embeddings without GPU requirements.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="fastembed"
    EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS="384"
    ```

    **Installation**: Fastembed is included by default with Cognee.

    **Known Issues**:

    * As of September 2025, Fastembed requires Python \< 3.13 (not compatible with Python 3.13+)
  </Accordion>

  <Accordion title="Custom Providers">
    Use OpenAI-compatible embedding endpoints from other providers.

    ```dotenv  theme={null}
    EMBEDDING_PROVIDER="custom"
    EMBEDDING_MODEL="provider/your-embedding-model"
    EMBEDDING_ENDPOINT="https://your-endpoint.example.com/v1"
    EMBEDDING_API_KEY="provider-..."
    EMBEDDING_DIMENSIONS="<match-your-model>"
    ```
  </Accordion>
</AccordionGroup>

## Advanced Options

<Accordion title="Rate Limiting">
  ```dotenv  theme={null}
  EMBEDDING_RATE_LIMIT_ENABLED="true"
  EMBEDDING_RATE_LIMIT_REQUESTS="10"
  EMBEDDING_RATE_LIMIT_INTERVAL="5"
  ```
</Accordion>

<Accordion title="Testing and Development">
  ```dotenv  theme={null}
  # Mock embeddings for testing (returns zero vectors)
  MOCK_EMBEDDING="true"
  ```
</Accordion>

## Important Notes

* **Dimension Consistency**: `EMBEDDING_DIMENSIONS` must match your vector store collection schema
* **API Key Fallback**: If `EMBEDDING_API_KEY` is not set, Cognee uses `LLM_API_KEY` (except for custom providers)
* **Tokenization**: For Ollama and Hugging Face models, set `HUGGINGFACE_TOKENIZER` for proper token counting
* **Performance**: Local providers (Ollama, Fastembed) are slower but offer privacy and cost benefits

<Columns cols={3}>
  <Card title="LLM Providers" icon="brain" href="/setup-configuration/llm-providers">
    Configure LLM providers for text generation
  </Card>

  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Set up vector databases for embedding storage
  </Card>

  <Card title="Overview" icon="settings" href="/setup-configuration/overview">
    Return to setup configuration overview
  </Card>
</Columns>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/setup-configuration/overview.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Setup Configuration

> Configure Cognee to use your preferred LLM, embedding engine, and storage backends

Configure Cognee to use your preferred LLM, embedding engine, relational database, vector store, and graph store via environment variables in a local `.env` file.

This section provides beginner-friendly guides for setting up different backends, with detailed technical information available in expandable sections.

## What You Can Configure

Cognee uses a flexible architecture that lets you choose the best tools for your needs. We recommend starting with the defaults to get familiar with Cognee, then customizing each component as needed:

* **[LLM Providers](./llm-providers)** — Choose from OpenAI, Azure OpenAI, Google Gemini, Anthropic, Ollama, or custom providers (like vLLM) for text generation and reasoning tasks
* **[Structured Output Backends](./structured-output-backends)** — Configure LiteLLM + Instructor or BAML for reliable data extraction from LLM responses
* **[Embedding Providers](./embedding-providers)** — Select from OpenAI, Azure OpenAI, Google Gemini, Mistral, Ollama, Fastembed, or custom embedding services to create vector representations for semantic search
* **[Relational Databases](./relational-databases)** — Use SQLite for local development or Postgres for production to store metadata, documents, and system state
* **[Vector Stores](./vector-stores)** — Store embeddings in LanceDB, PGVector, Qdrant, Redis, ChromaDB, FalkorDB, or Neptune Analytics for similarity search
* **[Graph Stores](./graph-stores)** — Build knowledge graphs with Kuzu, Kuzu-remote, Neo4j, Neptune, or Neptune Analytics to manage relationships and reasoning
* **[Dataset Separation & Access Control](./permissions)** — Configure dataset-level permissions and isolation
* **[Sessions & Caching](../core-concepts/sessions-and-caching)** — Enable conversational memory with Redis or filesystem cache adapters

<Warning>
  Dataset isolation is not enabled by default; see [how to enable it](../core-concepts/multi-user-mode/permissions-system/datasets#dataset-isolation).
</Warning>

## Observability & Telemetry

Cognee includes built-in telemetry to help you monitor and debug your knowledge graph operations. You can control telemetry behavior with environment variables:

* **`TELEMETRY_DISABLED`** (boolean, optional): Set to `true` to disable all telemetry collection (default: `false`)

When telemetry is enabled, Cognee automatically collects:

* Search query performance metrics
* Processing pipeline execution times
* Error rates and debugging information
* System resource usage

<Info>
  Telemetry data helps improve Cognee's performance and reliability. It's collected anonymously and doesn't include your actual data content.
</Info>

## Configuration Workflow

1. Install Cognee with all optional dependencies:
   * **Local setup**: `uv sync --all-extras`
   * **Library**: `pip install "cognee[all]"`
2. Create a `.env` file in your project root (if you haven't already) — see [Installation](/getting-started/installation) for details
3. Choose your preferred providers and follow the configuration instructions from the guides below

<Warning>
  **Configuration Changes**: If you've already run Cognee with default settings and are now changing your configuration (e.g., switching from SQLite to Postgres, or changing vector stores), you should call pruning operations before the next cognification to ensure data consistency.
</Warning>

<Warning>
  **LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.
</Warning>

<Columns cols={3}>
  <Card title="LLM Providers" icon="brain" href="/setup-configuration/llm-providers">
    Configure OpenAI, Azure, Gemini, Anthropic, Ollama, or custom LLM providers (like vLLM)
  </Card>

  <Card title="Structured Output Backends" icon="code" href="/setup-configuration/structured-output-backends">
    Configure LiteLLM + Instructor or BAML for reliable data extraction
  </Card>

  <Card title="Embedding Providers" icon="layers" href="/setup-configuration/embedding-providers">
    Set up OpenAI, Mistral, Ollama, Fastembed, or custom embedding services
  </Card>
</Columns>

<Columns cols={3}>
  <Card title="Relational Databases" icon="database" href="/setup-configuration/relational-databases">
    Choose between SQLite for local development or Postgres for production
  </Card>

  <Card title="Vector Stores" icon="database" href="/setup-configuration/vector-stores">
    Configure LanceDB, PGVector, Qdrant, Redis, ChromaDB, FalkorDB, or Neptune Analytics
  </Card>

  <Card title="Graph Stores" icon="network" href="/setup-configuration/graph-stores">
    Set up Kuzu, Neo4j, or Neptune for knowledge graph storage
  </Card>
</Columns>

```

