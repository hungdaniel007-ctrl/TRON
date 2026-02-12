Getting Started

# Installation

Copy page

Set up your environment and install Cognee

Set up your environment and install Cognee to start building AI memory.

Python **3.9 – 3.12** is required to run Cognee.

## 

[​

](https://docs.cognee.ai/getting-started/installation#prerequisites)

Prerequisites

Environment Configuration

- We recommend creating a `.env` file in your project root
- Cognee supports many configuration options, and a `.env` file keeps them organized

API Keys & Models

You have two main options for configuring LLM and embedding providers:**Option 1: OpenAI (Simplest)**

- Single API key handles both LLM and embeddings
- Uses gpt-4o-mini for LLM and text-embedding-3-small for embeddings by default
- Works out of the box with minimal configuration

**Option 2: Other Providers**

- Configure both LLM and embedding providers separately
- Supports Gemini, Anthropic, Ollama, and more
- Requires setting both `LLM_*` and `EMBEDDING_*` variables

By default, Cognee uses OpenAI for both LLMs and embeddings. If you change the LLM provider but don’t configure embeddings, it will still default to OpenAI.

Virtual Environment

- We recommend using [uv](https://github.com/astral-sh/uv) for virtual environment management
- Run the following commands to create and activate a virtual environment:

```
uv venv && source .venv/bin/activate
```

Optional

Database

- PostgreSQL database is required if you plan to use PostgreSQL as your relational database (requires `postgres` extra)

## 

[​

](https://docs.cognee.ai/getting-started/installation#setup)

Setup

- OpenAI (Recommended)

- Other Providers (Gemini, Anthropic, etc.)

**Environment:** Add your OpenAI API key to your `.env` file:

```
LLM_API_KEY="your_openai_api_key"
```

**Installation:** Install Cognee with all extras:

```
uv pip install cognee
```

**What this gives you**: Cognee installed with default local databases (SQLite, LanceDB, Kuzu) — no external servers required.

This single API key handles both LLM and embeddings. We use gpt-4o-mini for the LLM model and text-embedding-3-small for embeddings by default.



Getting Started

# Quickstart

Copy page

Get started with Cognee quickly and efficiently

After completing the [installation steps](https://docs.cognee.ai/getting-started/installation) successfully, run your first Cognee example to see AI memory in action.

## 

[​

](https://docs.cognee.ai/getting-started/quickstart#basic-usage)

Basic Usage

This minimal example shows how to add content, process it, and perform a search:

```
import cognee
import asyncio

async def main():

    # Create a clean slate for cognee -- reset data and system state
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # Add sample content
    text = "Cognee turns documents into AI memory."
    await cognee.add(text)

    # Process with LLMs to build the knowledge graph
    await cognee.cognify()

    # Search the knowledge graph
    results = await cognee.search(
        query_text="What does Cognee do?"
    )

    # Print
    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
```

Visualisation

Interactive knowledge graph visualization — drag nodes, zoom, and hover for details. Create your own visualization with 2 additional lines of code [here](https://docs.cognee.ai/guides/graph-visualization).

containscontainscontainsis_part_ofis_aconverts_documents_intois_ais_amade_fromcogneeproductdocumentsconceptai memorytext_document

## 

[​

](https://docs.cognee.ai/getting-started/quickstart#what-just-happened)

What just happened

The code demonstrates Cognee’s three core operations:

- **`.add`** — Adds data to Cognee so they can be cognified. In this case, we added a single string (“Cognee turns documents into AI memory”); from Cognee’s perspective, this string is a document.
- **`.cognify`** — This is where the cognification happens. All documents are chunked, entities are extracted, relationships are made, and summaries are generated. In this case, we can expect entities like Frodo, One Ring, and Mordor.
- **`.search`** — Queries the knowledge graph using vector similarity and graph traversal to find relevant information and return contextual results.

## 

[​

](https://docs.cognee.ai/getting-started/quickstart#about-async-/-await-in-cognee)

About `async` / `await` in Cognee

**Cognee uses asynchronous code extensively.** That means many of its functions are defined with `async` and must be called with `await`. This lets Python handle waiting (e.g. for I/O or network calls) without blocking the rest of your program.

Async basics

This example uses `async` / `await`, Python’s way of doing asynchronous programming. Asynchronous programming is used when functions may block because they are waiting for something (for example, a reply from an API call). By writing `async def`, you define a function that can pause at certain points. The `await` keyword marks those calls that may need to pause. To run such functions, Python provides the `asyncio` library. It uses a loop, called the event loop, which executes your code in order but, whenever a function is waiting, can temporarily run another one. From inside your function, though, everything still runs top-to-bottom: each line after an `await` only executes once the awaited call has finished.

Async resources

- A good starting point is this [guide](https://realpython.com/async-io-python/).
- Official documentation is available [here](https://docs.python.org/3/library/asyncio.html).

## 

[​

](https://docs.cognee.ai/getting-started/quickstart#next-steps)

Next Steps

[

## Cognee core concepts

Learn about Cognee’s core concepts, architecture, building blocks, and main operations.

](https://docs.cognee.ai/core-concepts/overview)



Core Concepts

# Overview

Copy page

Learn about Cognee’s core concepts, architecture, and how to get started

## 

[​

](https://docs.cognee.ai/core-concepts/overview#introduction)

Introduction

Cognee is an open source tool and platform that transforms your raw data into intelligent, searchable memory. It combines vector search with graph databases to make your data both searchable by meaning and connected by relationships.

**Dual storage architecture** gives you both semantic search and structural reasoning

**Modular design** composes [Tasks](https://docs.cognee.ai/core-concepts/building-blocks/tasks), [Pipelines](https://docs.cognee.ai/core-concepts/building-blocks/pipelines), and [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)

**Main operations** handle the complete workflow from ingestion to search: add, cognify, memify, search.

## 

[​

](https://docs.cognee.ai/core-concepts/overview#table-of-contents)

Table of Contents

Architecture

Cognee uses three complementary storage systems, each playing a different role:

- **Relational store** — Tracks documents, chunks, and provenance (where data came from and how it’s linked)
- **Vector store** — Holds embeddings for semantic similarity (numerical representations that find conceptually related content)
- **Graph store** — Captures entities and relationships in a knowledge graph (nodes and edges that show connections between concepts)

This architecture makes your data both **searchable** (via vectors) and **connected** (via graphs). Cognee ships with lightweight defaults that run locally, and you can swap in production-ready backends when needed.For detailed information about the storage architecture, see [Architecture](https://docs.cognee.ai/core-concepts/architecture).

Building Blocks

Cognee’s processing system is built from three fundamental components:

- **[DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)** — Structured data units that become graph nodes, carrying both content and metadata for indexing
- **[Tasks](https://docs.cognee.ai/core-concepts/building-blocks/tasks)** — Individual processing units that transform data, from text analysis to relationship extraction
- **[Pipelines](https://docs.cognee.ai/core-concepts/building-blocks/pipelines)** — Orchestration of Tasks into coordinated workflows, like assembly lines for data transformation

These building blocks work together to create a flexible system where you can:

- Use built-in Tasks for common operations
- Create custom Tasks for domain-specific logic by extending DataPoints
- Compose Tasks into Pipelines that match your workflow

Main Operations

Cognee provides four main operations that users interact with:

- **[Add](https://docs.cognee.ai/core-concepts/main-operations/add)** — Ingest and prepare data for processing, handling various file formats and data sources
- **[Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify)** — Create knowledge graphs from processed data through cognitive processing and entity extraction
- **[Memify](https://docs.cognee.ai/core-concepts/main-operations/memify)** — Optional semantic enrichment of the graph for enhanced understanding *(coming soon)*
- **[Search](https://docs.cognee.ai/core-concepts/main-operations/search)** — Query and retrieve information using semantic similarity, graph traversal, or hybrid approaches

**Note:** Search works great with just the basic Add → Cognify → Search workflow. Memify is an optional enhancement that will provide additional semantic enrichment when available.

Further Concepts

Beyond the core workflow, Cognee offers advanced features for sophisticated knowledge management:

- **[Node Sets](https://docs.cognee.ai/core-concepts/further-concepts/node-sets)** — Tagging and organization system that helps categorize and filter your knowledge base content
- **[Ontologies](https://docs.cognee.ai/core-concepts/further-concepts/ontologies)** — External knowledge grounding through RDF/XML ontologies that connect your data to established knowledge structures

These concepts extend Cognee’s capabilities for:

- **Organization** — Managing growing knowledge bases with systematic tagging
- **Knowledge grounding** — Connecting your data to external, validated knowledge sources
- **Domain expertise** — Leveraging existing ontologies for specialized fields like medicine, finance, or research

## 

[​

](https://docs.cognee.ai/core-concepts/overview#next-steps)

Next steps

A good way to learn Cognee is to start with its [architecture](https://docs.cognee.ai/core-concepts/architecture), move on to [building blocks](https://docs.cognee.ai/core-concepts/building-blocks/datapoints), practice the [main operations](https://docs.cognee.ai/core-concepts/main-operations/add), and finally explore [advanced features](https://docs.cognee.ai/core-concepts/further-concepts/node-sets).

Core Concepts

# Architecture

Copy page

Understanding Cognee’s storage architecture and system components

# 

[​

](https://docs.cognee.ai/core-concepts/architecture#cognee-architecture)

Cognee Architecture

## 

[​

](https://docs.cognee.ai/core-concepts/architecture#why-multiple-stores)

Why multiple stores

No single database can handle all aspects of memory. Cognee combines three complementary storage systems. Each one plays a different role, and together they make your data both **searchable** and **connected**.

- **Relational store** — Tracks your documents, their chunks, and provenance (i.e. where each piece of data came from and how it’s linked to the source).
- **Vector store** — Holds embeddings for semantic similarity (i.e. numerical representations that let Cognee find conceptually related text, even if the wording is different).
- **Graph store** — Captures entities and relationships in a knowledge graph (i.e. nodes and edges that let Cognee understand structure and navigate connections between concepts).

Cognee ships with lightweight defaults that run locally, and you can swap in production-ready backends when needed (see [Setup](https://docs.cognee.ai/getting-started/installation)).

## 

[​

](https://docs.cognee.ai/core-concepts/architecture#what-is-stored-where)

What is stored where

Roughly speaking:

- The **relational store** handles document-level metadata and provenance.
- The **vector store** contains semantic fingerprints of chunks and [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints).
- The **graph store** captures higher-level structure in the form of entities and relationships.

There is some overlap: for efficiency, parts of the same information may be indexed in more than one store.

## 

[​

](https://docs.cognee.ai/core-concepts/architecture#how-they-are-used)

How they are used

The stores play different roles depending on the phase:

- The **relational store** matters most during *cognification*, keeping track of documents, chunks, and where each piece of information comes from.
- The **vector** and **graph** stores come into play during *search and retrieval*:
  - **Semantic searches** (vector): find conceptually related passages based on embeddings
  - **Structural searches** (graph): explore entities and relationships using Cypher directly
  - **Hybrid searches** (vector + graph): combine both perspectives to surface results that are contextually rich and structurally precise.

Building Blocks

# DataPoints

Copy page

Atomic units of knowledge in Cognee

# 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints#datapoints-atomic-units-of-knowledge)

DataPoints: Atomic Units of Knowledge

DataPoints are the smallest building blocks in Cognee.  
They represent **atomic units of knowledge** — carrying both your actual content and the context needed to process, index, and connect it.They’re the reason Cognee can turn raw documents into something that’s both **searchable** (via vectors) and **connected** (via graphs).

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints#what-are-datapoints)

What are DataPoints

- **Atomic** — each DataPoint represents one concept or unit of information.
- **Structured** — implemented as [Pydantic](https://docs.pydantic.dev/) models for validation and serialization.
- **Contextual** — carry provenance, versioning, and indexing hints so every step downstream knows where data came from and how to use it.

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints#core-structure)

Core Structure

A DataPoint is just a Pydantic model with a set of standard fields.

See example class definition

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints#indexing-&-embeddings)

Indexing & Embeddings

The `metadata.index_fields` tells Cognee which fields to embed into the vector store. This is the mechanism behind semantic search.

- Fields in `index_fields` → converted into embeddings
- Each indexed field → its own vector collection (`Class_field`)
- Non-indexed fields → stay as regular properties
- Choosing what to index controls search granularity

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints#from-datapoints-to-the-graph)

From DataPoints to the Graph

When you call `add_data_points()`, Cognee automatically:

- Embeds the indexed fields into vectors
- Converts the object into **nodes** and **edges** in the knowledge graph
- Stores provenance in the relational store

This is how Cognee creates both **semantic similarity** (vector) and **structural reasoning** (graph) from the same unit.

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints#examples-and-details)

Examples and details

Example: indexing only one field

```
class Person(DataPoint):
    name: str
    age: int
    metadata: dict = {"index_fields": ["name"]}
```

Only `"name"` is semantically searchable

Example: Book → Author transformation

```
class Book(DataPoint):
    title: str
    author: Author
    metadata: dict = {"index_fields": ["title"]}

# Produces:
# `Node(Book)` with `{title, type, ...}`
# Node(Author) with {name, type, ...}
# Edge(Book → Author, type="author")
```

Relationship syntax options

```
# Simple relationship
`author: Author`  

# With edge metadata
`has_items: (Edge(weight=0.8), list[Item])`

# List relationship
`chapters: list[Chapter]`
```

Built-in DataPoint types

Cognee ships with several built-in DataPoint types:

- **Documents** — wrappers for source files (Text, PDF, Audio, Image)
  - `Document` (`metadata.index_fields=["name"]`)
- **Chunks** — segmented portions of documents
  - `DocumentChunk` (`metadata.index_fields=["text"]`)
- **Summaries** — generated text or code summaries
  - `TextSummary` / `CodeSummary` (`metadata.index_fields=["text"]`)
- **Entities** — named objects (people, places, concepts)
  - `Entity`, `EntityType` (`metadata.index_fields=["name"]`)
- **Edges** — relationships between DataPoints
  - `Edge` — links between DataPoints

Example: custom DataPoint with best practices

```
class Product(DataPoint):
    name: str
    description: str
    price: float
    category: Category

    # Index name + description for search
    metadata: dict = {"index_fields": ["name", "description"]}
```

**Best Practices:**

- **Keep it small** — one concept per DataPoint
- **Index carefully** — only fields that matter for semantic search
- **Use built-in types first** — extend with custom subclasses when needed
- **Version deliberately** — track changes with `version`
- **Group related points** — with `belongs_to_set`

[

## Tasks

Learn how DataPoints are created and processed

](https://docs.cognee.ai/core-concepts/building-blocks/tasks)[

## Pipelines

See how DataPoints flow through processing workflows

](https://docs.cognee.ai/core-concepts/building-blocks/pipelines)[

## Main Operations

Understand how DataPoints are used in Add, Cognify, and Search

](https://docs.cognee.ai/core-concepts/main-operations/add)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/architecture)[

TasksBuilding blocks of processing that transform data in Cognee pipelines

Next

](https://docs.cognee.ai/core-concepts/building-blocks/tasks)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



Building Blocks

# Tasks

Copy page

Building blocks of processing that transform data in Cognee pipelines

# 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#tasks-smallest-executable-units)

Tasks: Smallest Executable Units

Tasks are Cognee’s **smallest executable units** — they wrap any Python callable and give it a uniform interface for batching, error handling, and logging. While they can work with anything, Tasks are most powerful when creating or enriching [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints).

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#what-are-tasks)

What are Tasks

Tasks are Cognee’s **smallest executable units**.

- They wrap any Python callable (function, coroutine, generator, async generator).
- Give a **uniform interface** for batching, error handling, and logging.
- Can work with anything, but are **most powerful when creating or enriching [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)**.

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#why-tasks-exist)

Why Tasks Exist

- Normalize different kinds of Python functions so they behave consistently.
- Enable **stream-based processing**: outputs flow directly into the next step.
- Provide **batching controls** for efficiency, especially with LLM or I/O-heavy operations.
- Form the **building blocks** of higher-level [Pipelines](https://docs.cognee.ai/core-concepts/building-blocks/pipelines).

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#core-concepts)

Core Concepts

- **Execution**: run functions in a consistent way, regardless of sync/async/gen.
- **Batching**: configurable with `task_config`.
- **Composition**: Tasks can be chained — one Task’s output is the next Task’s input.
- **Flexibility**: Tasks don’t need to handle DataPoints, but Cognee’s defaults encourage it.

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#dependencies-&-ordering)

Dependencies & Ordering

Tasks often assume a certain **input type** and produce an expected **output type**. Example flow (educational, not exhaustive):

- Raw data → Documents
- Documents → Chunks
- Chunks → Entities and relationships
- Entities/Chunks → Summaries
- Any DataPoint → Storage

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#built-in-tasks)

Built-in Tasks

- **Ingestion**: `resolve_data_directories`, `ingest_data`
- **Classification**: `classify_documents`
- **Access control**: `check_permissions_on_dataset`
- **Chunking**: `extract_chunks_from_documents`
- **Graph extraction**: `extract_graph_from_data`
- **Summarization**: `summarize_text`, `summarize_code`
- **Persistence**: `add_data_points`

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/tasks#examples-and-details)

Examples and details

Task API & Constructor

```
Task(executable, *args, task_config={...}, **kwargs)
```

**Key parameters:**

- `executable`: Any Python callable (function, coroutine, generator, async generator)
- `task_config`: Configuration for batching, error handling, and logging
- `default_params`: Parameters that are always passed to the executable

Supported Task Types

Cognee automatically detects and handles different Python function types:

- **Functions**: Standard synchronous functions
- **Coroutines**: Async functions using `async def`
- **Generators**: Functions that yield multiple values
- **Async Generators**: Async functions that yield multiple values

Each type is executed appropriately within Cognee’s task system.

Writing a Custom Task

```
def my_custom_task(data_chunk):
    # Process the data chunk
    processed_data = process_chunk(data_chunk)

    # Create or enrich DataPoints
    datapoint = DataPoint(
        content=processed_data,
        metadata={"source": "custom_task"}
    )

    return datapoint

# Wrap it in a Task
my_task = Task(my_custom_task)
```

**Why idempotent, DataPoint-focused functions are easiest to compose:**

- Predictable inputs and outputs
- Easy to chain together
- Clear data flow between steps

Execution Flow

Tasks execute in sequence within [Pipelines](https://docs.cognee.ai/core-concepts/building-blocks/pipelines), with each Task’s output becoming the next Task’s input. This creates a data transformation pipeline that builds up to the final knowledge graph.

[

## DataPoints

The structured units that Tasks create and process

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)[

## Pipelines

How Tasks are orchestrated into workflows

](https://docs.cognee.ai/core-concepts/building-blocks/pipelines)[

## Main Operations

See Tasks in action during data ingestion and processing

](https://docs.cognee.ai/core-concepts/main-operations/add)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)[

PipelinesOrchestrating tasks into coordinated workflows for data processing

Next

](https://docs.cognee.ai/core-concepts/building-blocks/pipelines)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



Building Blocks

# Pipelines

Copy page

Orchestrating tasks into coordinated workflows for data processing

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/pipelines#what-pipelines-are)

What pipelines are

Pipelines coordinate ordered [Tasks](https://docs.cognee.ai/core-concepts/building-blocks/tasks) into a reproducible workflow. Default Cognee operations like [Add](https://docs.cognee.ai/core-concepts/main-operations/add) and [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify) run on top of the same execution layer. You typically do not call low-level functions directly; you trigger pipelines through these operations.

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/pipelines#prerequisites)

Prerequisites

- **Dataset**: a container (name or UUID) where your data is stored and processed. Every document added to cognee belongs to a dataset.
- **User**: the identity for ownership and access control. A default user is created and used if none is provided.
- More details are available below

## 

[​

](https://docs.cognee.ai/core-concepts/building-blocks/pipelines#how-pipelines-run)

How pipelines run

Somewhat unsurprisingly, the function used to run pipelines is called `run_pipeline`.Cognee uses a **layered execution model**: a single call to `run_pipeline` orchestrates **multi-dataset processing** by running **per-file pipelines** through the sequence of tasks.

- **Statuses** are yielded as the pipeline runs and written to **databases** where appropriate
- **User access** to datasets and files is carefully verified at each layer
- **Pipeline run information** includes dataset IDs, completion status, and error handling
- **Background execution** uses queues to manage status updates and avoid database conflicts

Layered execution

- Innermost layer: individual task execution with telemetry and recursive task running in batches
- Middle layer: per-dataset pipeline management and task orchestration
- Outermost layer: multi-dataset orchestration and overall pipeline execution
- Execution modes: blocking (wait for completion) or background (return immediately with “started” status)

Customization approaches and tips

- [](https://docs.cognee.ai/core-concepts/main-operations/cognify)[](https://docs.cognee.ai/core-concepts/main-operations/add)

Users

- Identity: represents who owns and acts on data. If omitted, a default user is used
- Ownership: every ingested item is tied to a user; content is deduplicated per owner
- Permissions: enforced per dataset (read/write/delete/share) during processing and API access

Datasets

- Container: a named or UUID-scoped collection of related data and derived knowledge
- Scoping: Add writes into a specific dataset; Cognify processes the dataset(s) you pass
- Lifecycle: new names create datasets and grant the calling user permissions; UUIDs let you target existing datasets (given permission)

[

## Tasks

Learn about the individual processing units that make up pipelines

](https://docs.cognee.ai/core-concepts/building-blocks/tasks)[

## DataPoints

Understand the structured outputs that pipelines produce

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)[

## Main Operations

See how pipelines are used in Add, Cognify, and Search workflows

](https://docs.cognee.ai/core-concepts/main-operations/add)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/building-blocks/tasks)[

AddIngesting and preparing data for processing in Cognee

Next

](https://docs.cognee.ai/core-concepts/main-operations/add)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



Main Operations

# Add

Copy page

Ingesting and preparing data for processing in Cognee

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/add#what-is-the-add-operation)

What is the add operation

The `.add` operation is how you bring content into Cognee. It takes your files, directories, or raw text, normalizes them into plain text, and records them into a dataset that Cognee can later expand into vectors and graphs with [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify).

- **Ingestion-only**: no embeddings, no graph yet
- **Flexible input**: raw text, local files, directories, any [Docling](https://github.com/docling-project/docling) supported format or S3 URIs
- **Normalized storage**: everything is turned into text and stored consistently
- **Deduplicated**: Cognee uses content hashes to avoid duplicates
- **Dataset-first**: everything you add goes into a dataset
  - Datasets are how Cognee keeps different collections organized (e.g. “research-papers”, “customer-reports”)
  - Each dataset has its own ID, owner, and permissions for access control
  - You can read more about them below

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/add#where-add-fits)

Where add fits

- First step before you run [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify)
- Use it to **create a dataset** from scratch, or **append new data** over time
- Ideal for both local experiments and programmatic ingestion from storage (e.g. S3)

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/add#what-happens-under-the-hood)

What happens under the hood

1. **Expand your input**
   - Directories are walked, S3 paths are expanded, raw text is passed through
   - Result: a flat list of items (files, text, handles)
2. **Ingest and register**
   - Files are saved into Cognee’s storage and converted to text
   - Cognee computes a stable content hash to prevent duplicates
   - Each item becomes a record in the database and is attached to your dataset
   - **Text extraction**: Converts various file formats into plain text
   - **Metadata preservation**: Keeps file information like source, creation date, and format
   - **Content normalization**: Ensures consistent text encoding and formatting
3. **Return a summary**
   - You get a pipeline run info object that tells you where everything went and which dataset is ready for the next step

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/add#after-add-finishes)

After add finishes

After `.add` completes, your data is ready for the next stage:

- **Files are safely stored** in Cognee’s storage system with metadata preserved
- **Database records** track each ingested item and link it to your dataset
- **Dataset is prepared** for transformation with [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify) — which will chunk, embed, and connect everything

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/add#further-details)

Further details

Input sources

- Mix and match: `["some text", "/path/to/file.pdf", "s3://bucket/data.csv"]`
- Works with directories (recursively), S3 prefixes, and file handles
- Local and cloud sources are normalized into the same format

Supported formats

- **Text**: `.txt, .md, .csv, .json, …`
- **PDF**: `.pdf`
- **Images**: common formats like `.png, .jpg, .gif, .webp, …`
- **Audio**: `.mp3, .wav, .flac, …`
- **Office docs**: `.docx, .pptx, .xlsx, …`
- **Docling**: Cognee can also ingest the `DoclingDocument` format. Any format that [Docling](https://github.com/docling-project/docling) supports as input can be converted, then passed on to Cognee’s add.
- Cognee chooses the right loader for each format under the hood

Datasets

- A dataset is your “knowledge base” — a grouping of related data that makes sense together
- Datasets are **first-class objects in Cognee’s database** with their own ID, name, owner, and permissions
- They provide **scope**: `.add` writes into a dataset, [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify) processes per-dataset
- Think of them as separate shelves in your library — e.g., a “research-papers” dataset and a “customer-reports” dataset
- If you name a dataset that doesn’t exist, Cognee creates it for you; if you don’t specify, a default one is used

Users and ownership

- Every dataset and data item belongs to a user
- If you don’t pass a user, Cognee creates/uses a default one
- Ownership controls who can later read, write, or share that dataset

Node sets

- Optional labels to group or tag data on ingestion
- Example: `node_set=["AI", "FinTech"]`
- Useful later when you want to focus on subgraphs

[

## Cognify

Expand data into chunks, embeddings, and graphs

](https://docs.cognee.ai/core-concepts/main-operations/cognify)[

## DataPoints

The units you’ll see after Cognify

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)[

## Building Blocks

Learn about Tasks and Pipelines behind Add

](https://docs.cognee.ai/core-concepts/building-blocks/tasks)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/building-blocks/pipelines)[

CognifyTransforming ingested data into a knowledge graph with embeddings, chunks, and summaries

Next

](https://docs.cognee.ai/core-concepts/main-operations/cognify)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



Main Operations

# Cognify

Copy page

Transforming ingested data into a knowledge graph with embeddings, chunks, and summaries

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/cognify#what-is-the-cognify-operation)

What is the cognify operation

The `.cognify` operation takes the ingested data with [Add](https://docs.cognee.ai/core-concepts/main-operations/add) and turns plain text into structured knowledge: chunks, embeddings, summaries, nodes, and edges that live in Cognee’s vector and graph stores. It prepares your data for downstream operations like [Search](https://docs.cognee.ai/core-concepts/main-operations/search).

- **Transforms ingested data**: builds chunks, embeddings, and summaries
- **Graph creation**: extracts entities and relationships to form a knowledge graph
- **Vector indexing**: makes everything searchable via embeddings
- **Dataset-scoped**: runs per dataset, respecting ownership and permissions

`.cognify` can be run multiple times as the dataset grows, and Cognee will skip what’s already processed. Read more about **Incremental loading** in **[Examples and details](https://docs.cognee.ai/core-concepts/main-operations/cognify#examples-and-details)**

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/cognify#what-happens-under-the-hood)

What happens under the hood

The `.cognify` pipeline is made of six ordered [Tasks](https://docs.cognee.ai/core-concepts/building-blocks/tasks). Each task takes the output of the previous one and moves your data closer to becoming a searchable knowledge graph.

1. **Classify documents** — wrap each ingested file as a `Document` object with metadata and optional node sets
2. **Check permissions** — enforce that you have write access to the target dataset
3. **Extract chunks** — split documents into smaller pieces (paragraphs, sections)
4. **Extract graph** — use LLMs to identify entities and relationships, inserting them into the graph DB
5. **Summarize text** — generate summaries for each chunk, stored as `TextSummary` [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)
6. **Add data points** — embed nodes and summaries, write them into the vector store, and update graph edges

The result is a fully searchable, structured knowledge graph connected to your data.

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/cognify#after-cognify-finishes)

After cognify finishes

When `.cognify` completes for a dataset:

- **DocumentChunks** exist in memory as the granular breakdown of your files
- **Summaries** are stored and indexed in the vector database for semantic search
- **Knowledge graph nodes and edges** are committed to the graph database
- **Dataset metadata** is updated with token counts and pipeline status
- Your dataset is now **query-ready**: you can run [Search](https://docs.cognee.ai/core-concepts/main-operations/search) or graph queries immediately

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/cognify#examples-and-details)

Examples and details

Pipeline tasks (detailed)

1. **Classify documents**
   - Turns raw `Data` rows into `Document` objects
   - Chooses the right document type (PDF, text, image, audio, etc.)
   - Attaches metadata and optional node sets
2. **Check permissions**
   - Verifies that the user has write access to the dataset
3. **Extract chunks**
   - Splits documents into `DocumentChunk`s using a chunker
   - Updates token counts in the relational DB
4. **Extract graph**
   - Calls the LLM to extract entities and relationships
   - Deduplicates nodes and edges, commits to the graph DB
5. **Summarize text**
   - Generates concise summaries per chunk
   - Stores them as `TextSummary` [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints) for vector search
6. **Add data points**
   - Converts summaries and other [DataPoints](https://docs.cognee.ai/core-concepts/building-blocks/datapoints) into graph + vector nodes
   - Embeds them in the vector store, persists in the graph DB

Datasets and permissions

- Cognify always runs on a dataset
- You must have **write access** to the target dataset
- Permissions are enforced at pipeline start
- Each dataset maintains its own cognify status and token counts

Incremental loading

- By default, `.cognify` processes all data in a dataset
- With `incremental_loading=True`, only new or updated files are processed
- Saves time and compute for large, evolving datasets

Final outcome

- Vector database contains embeddings for summaries and nodes
- Graph database contains entities and relationships
- Relational database tracks token counts and pipeline run status
- Your dataset is now ready for [Search](https://docs.cognee.ai/core-concepts/main-operations/search) (semantic or graph-based)

[

## Add

First bring data into Cognee

](https://docs.cognee.ai/core-concepts/main-operations/add)[

## Search

Query embeddings or graph structures built by Cognify

](https://docs.cognee.ai/core-concepts/main-operations/search)[

## Building Blocks

Learn about DataPoints, Tasks, and Pipelines

](https://docs.cognee.ai/core-concepts/building-blocks/datapoints)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/main-operations/add)[

SearchQuery your AI memory with vectors, graphs, and LLMs

Next

](https://docs.cognee.ai/core-concepts/main-operations/search)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



Main Operations

# Search

Copy page

Query your AI memory with vectors, graphs, and LLMs

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/search#what-is-search)

What is search

`search` lets you ask questions over everything you’ve ingested and cognified.  
Under the hood, Cognee blends **vector similarity**, **graph structure**, and **LLM reasoning** to return answers with context and provenance.

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/search#the-big-picture)

The big picture

- **Dataset-aware**: searches run against one or more datasets you can read *(requires `ENABLE_BACKEND_ACCESS_CONTROL=true`)*
- **Multiple modes**: from simple chunk lookup to graph-aware Q&A
- **Hybrid retrieval**: vectors find relevant pieces; graphs provide structure; LLMs compose answers
- **Conversational memory**: use `session_id` to maintain conversation history across searches *(requires caching enabled)*
- **Safe by default**: permissions are checked before any retrieval
- **Observability**: telemetry is emitted for query start/completion

**Dataset scoping** requires specific configuration. See [permissions system](https://docs.cognee.ai/core-concepts/multi-user-mode/permissions-system/datasets#dataset-isolation) for details on access control requirements and supported database setups.

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/search#where-search-fits)

Where search fits

Use `search` after you’ve run `.add` and `.cognify`. At that point, your dataset has chunks, summaries, embeddings, and a knowledge graph—so queries can leverage both **similarity** and **structure**.

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/search#how-it-works-conceptually)

How it works (conceptually)

1. **Scope & permissions**  
   Resolve target datasets (by name or id) and enforce read access.
2. **Mode dispatch**  
   Pick a search mode (default: **graph-aware completion**) and route to its retriever.
3. **Retrieve → (optional) generate**  
   Collect context via vectors and/or graph traversal; some modes then ask an LLM to compose a final answer.
4. **Return results**  
   Depending on mode: answers, chunks/summaries with metadata, graph records, Cypher results, or code contexts.

For a practical guide to using search with examples and detailed parameter explanations, see [Search Basics](https://docs.cognee.ai/guides/search-basics).

GRAPH_COMPLETION (default)

Graph-aware question answering.

- **What it does**: Finds relevant graph triplets using vector hints across indexed fields, resolves them into readable context, and asks an LLM to answer your question grounded in that context.
- **Why it’s useful**: Combines fuzzy matching (vectors) with precise structure (graph) so answers reflect relationships, not just nearby text.
- **Typical output**: A natural-language answer with references to the supporting graph context.

RAG_COMPLETION

Retrieve-then-generate over text chunks.

- **What it does**: Pulls top-k chunks via vector search, stitches a context window, then asks an LLM to answer.
- **When to use**: You want fast, text-only RAG without graph structure.
- **Output**: An LLM answer grounded in retrieved chunks.

CHUNKS

Direct chunk retrieval.

- **What it does**: Returns the most similar text chunks to your query via vector search.
- **When to use**: You want raw passages/snippets to display or post-process.
- **Output**: Chunk objects with metadata.

SUMMARIES

Search over precomputed summaries.

- **What it does**: Vector search on `TextSummary` content for concise, high-signal hits.
- **When to use**: You prefer short summaries instead of full chunks.
- **Output**: Summary objects with provenance.

GRAPH_SUMMARY_COMPLETION

Graph-aware summary answering.

- **What it does**: Builds graph context like GRAPH_COMPLETION, then condenses it before answering.
- **When to use**: You want a tighter, summary-first response.
- **Output**: A concise answer grounded in graph context.

GRAPH_COMPLETION_COT

Chain-of-thought over the graph.

- **What it does**: Iterative rounds of graph retrieval and LLM reasoning to refine the answer.
- **When to use**: Complex questions that benefit from stepwise reasoning.
- **Output**: A refined answer produced through multiple reasoning steps.

GRAPH_COMPLETION_CONTEXT_EXTENSION

Iterative context expansion.

- **What it does**: Starts with initial graph context, lets the LLM suggest follow-ups, fetches more graph context, repeats.
- **When to use**: Open-ended queries that need broader exploration.
- **Output**: An answer assembled after expanding the relevant subgraph.

NATURAL_LANGUAGE

Natural language to Cypher to execution.

- **What it does**: Infers a Cypher query from your question using the graph schema, runs it, returns the results.
- **When to use**: You want structured graph answers without writing Cypher.
- **Output**: Executed graph results.

CYPHER

Run Cypher directly.

- **What it does**: Executes your Cypher query against the graph database.
- **When to use**: You know the schema and want full control.
- **Output**: Raw query results.

CODE

Code-focused retrieval.

- **What it does**: Interprets your intent (files/snippets), searches code embeddings and related graph nodes, and assembles relevant source.
- **When to use**: Codebases indexed by Cognee.
- **Output**: Structured code contexts and related graph information.

FEELING_LUCKY

Automatic mode selection.

- **What it does**: Uses an LLM to pick the most suitable search mode for your query, then runs it.
- **When to use**: You’re not sure which mode fits best.
- **Output**: Results from the selected mode.

FEEDBACK

Store feedback on recent interactions.

- **What it does**: Records user feedback on recent answers and links it to the associated graph elements for future tuning.
- **When to use**: Closing the loop on quality and relevance.
- **Output**: A feedback record tied to recent interactions.

[

## Add

First bring data into Cognee

](https://docs.cognee.ai/core-concepts/main-operations/add)[

## Cognify

Build the knowledge graph that search queries

](https://docs.cognee.ai/core-concepts/main-operations/cognify)[

## Architecture

Understand how vector and graph stores work together

](https://docs.cognee.ai/core-concepts/architecture)[

## Sessions and Caching

Enable conversational memory with sessions

](https://docs.cognee.ai/core-concepts/sessions-and-caching)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/main-operations/cognify)[

MemifySemantic enrichment of existing knowledge graphs with derived facts

Next

](https://docs.cognee.ai/core-concepts/main-operations/memify)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



Main Operations

# Memify

Copy page

Semantic enrichment of existing knowledge graphs with derived facts

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/memify#what-is-the-memify-operation)

What is the memify operation

The `.memify` operation enriches existing knowledge graphs by extracting derived facts and creating new associations from your already-processed data. Unlike [Add](https://docs.cognee.ai/core-concepts/main-operations/add) and [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify), memify works on existing graph structures to add semantic understanding and deeper contextual relationships.

- **Graph enrichment**: operates on existing knowledge graphs created by [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify)
- **Derived facts**: creates new nodes and edges from existing context without re-ingesting data
- **Semantic enhancement**: adds coding rules, associations, and other derived knowledge
- **Pipeline-based**: uses extraction and enrichment tasks to process subgraphs
- **Incremental**: can be run multiple times to add new derived facts as needed

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/memify#where-memify-fits)

Where memify fits

Use `.memify` after you’ve completed the [Add](https://docs.cognee.ai/core-concepts/main-operations/add) → [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify) workflow:

- **Prerequisites**: requires an existing knowledge graph with chunks, embeddings, and graph structure
- **Enhancement phase**: adds semantic understanding and derived facts to your existing data
- **Optional enrichment**: not required for basic search, but adds valuable context and associations

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/memify#what-happens-under-the-hood)

What happens under the hood

The `.memify` pipeline processes your existing knowledge graph through two main phases:

1. **Extraction phase** — pulls relevant subgraphs or chunks from your existing knowledge graph
2. **Enrichment phase** — applies enrichment tasks to create new nodes and edges from existing context

The default memify tasks include:

- **Extract subgraph chunks**: identifies relevant portions of your graph for processing
- **Add rule associations**: creates coding rules and other derived facts from the extracted context

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/memify#after-memify-finishes)

After memify finishes

When `.memify` completes:

- **New derived facts** are added to your knowledge graph as additional nodes and edges
- **Enhanced searchability**: specialized search types like `SearchType.CODING_RULES` become available
- **Richer context**: your existing data now includes semantic associations and derived knowledge
- **No data re-ingestion**: all enrichment happens on your existing graph structure

## 

[​

](https://docs.cognee.ai/core-concepts/main-operations/memify#examples-and-details)

Examples and details

Default behavior

- **Extraction**: `extract_subgraph_chunks` - pulls relevant chunks from your graph
- **Enrichment**: `add_rule_associations` - creates coding rules and associations
- **Output**: new nodes and edges added to your existing knowledge graph

Custom tasks

- You can specify custom extraction and enrichment tasks
- Extraction tasks determine what parts of the graph to process
- Enrichment tasks define what derived facts to create
- Tasks can be chained together for complex enrichment workflows

Search integration

- Enriched graphs support specialized search types
- `SearchType.CODING_RULES` for finding coding guidelines
- Other search modes can leverage the new derived facts
- Enhanced context improves answer quality and relevance

Incremental processing

- Can be run multiple times on the same dataset
- Only processes new or updated graph elements by default
- Safe to re-run as it adds rather than replaces existing data

[

## Cognify

Build the knowledge graph that memify enriches

](https://docs.cognee.ai/core-concepts/main-operations/cognify)[

## Search

Query the enriched graph with specialized search types

](https://docs.cognee.ai/core-concepts/main-operations/search)[

## Custom Tasks

Learn how to create custom memify tasks

](https://docs.cognee.ai/guides/custom-tasks-pipelines)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/main-operations/search)[

DatasetsProject-level containers for organization, permissions, and processing

Next

](https://docs.cognee.ai/core-concepts/further-concepts/datasets)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)



urther Concepts

# Datasets

Copy page

Project-level containers for organization, permissions, and processing

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/datasets#what-is-a-dataset-in-cognee)

What is a dataset in Cognee?

A dataset is a named container that groups documents and their metadata. It is the main boundary for:

- Organizing content
- Running pipelines
- Applying permissions

**Dataset isolation** requires specific configuration. See [permissions system](https://docs.cognee.ai/core-concepts/multi-user-mode/multi-user-mode-overview) for details on access control requirements and supported database setups.

- **[Add](https://docs.cognee.ai/core-concepts/main-operations/add)**:
  - Direct new content into a specific dataset (by name or ID)
  - If it doesn’t exist, Cognee creates it and associates your permissions
  - Items ingested are linked to that dataset and deduplicated within it
- **[Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify)**:
  - Choose which dataset(s) to transform into a knowledge graph
  - Loads the dataset’s content, checks rights, and runs the pipeline per dataset
  - If none are specified, processes all datasets you’re authorized to use
  - Progress is tracked per dataset for reliable re-runs
- **[Search](https://docs.cognee.ai/core-concepts/main-operations/search)**:
  - Queries can be scoped by dataset
  - Results and metrics remain separated by dataset

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/datasets#access-control)

Access control

- Permissions (read, write, share, delete) are enforced at the dataset level
- Share one dataset with a team, keep another private
- Independently manage who can modify or distribute content

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/datasets#incremental-processing)

Incremental processing

- Processing status is tracked per dataset
- After you add more data, Cognify focuses on new or changed items
- Skips what’s already completed for that dataset

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/datasets#datasets-vs-nodesets)

Datasets vs NodeSets

**Datasets** scope storage, permissions, and pipeline execution; **[NodeSets](https://docs.cognee.ai/core-concepts/further-concepts/node-sets)** are semantic tags within a dataset.

- During Add, you can label items with one or more NodeSet names (e.g., “AI”, “FinTech”)
- Cognify propagates those labels into the graph by creating `NodeSet` nodes and linking derived chunks and entities via `belongs_to_set` relationships
- This lets you slice a single dataset’s graph by topic or team without creating new datasets, while dataset-level permissions still control overall access

Further Concepts

# NodeSets

Copy page

Tagging and grouping data in Cognee

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/node-sets#what-are-nodesets)

What are NodeSets?

A **NodeSet** lets you group parts of your AI memory at the dataset level. You create them as a simple list of tags when adding data to Cognee: await cognee.add(…, node_set=[“projectA”,“finance”]) These tags travel with your data into the knowledge graph, where they become first-class nodes connected with belongs_to_set edges — and you can later filter searches to only those subsets.

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/node-sets#how-they-flow-through-cognee)

How they flow through Cognee

- **[Add](https://docs.cognee.ai/core-concepts/main-operations/add)**:
  - NodeSets are attached as simple tags to datasets or documents
  - This happens when you first ingest data
- **[Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify)**:
  - carried into Documents and Chunks
  - materialized as real `NodeSet` nodes in the graph
  - connected with `belongs_to_set` edges
- **[Search](https://docs.cognee.ai/core-concepts/main-operations/search)**:
  - NodeSets act as entry points into the graph
  - Queries can be scoped to only nodes linked to specific NodeSets
  - This lets you search within a tagged subset of your data

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/node-sets#why-they-matter)

Why they matter

- Provide a lightweight way to organize and tag your data
- Enable graph-based filtering, traversal, and reporting
- Ideal for creating project-, domain-, or user-defined subsets of your knowledge graph

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/node-sets#example)

Example

```
import asyncio
import cognee

async def main():
    # reset Cognee’s memory and metadata for a clean run
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # add a document linked only to the "AI_Memory" node set
    await cognee.add(
        "Cognee builds AI memory from raw documents.",
        node_set=["AI_Memory"]
    )

    # add a document linked to both "AI_Memory" and "Graph_RAG" node sets
    await cognee.add(
        "Cognee combines vector search with graph reasoning.",
        node_set=["AI_Memory", "Graph_RAG"]
    )

    # build the knowledge graph by extracting entities and relationships
    await cognee.cognify()

if __name__ == "__main__":
    asyncio.run(main())
```

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/node-sets#what-just-happened)

What just happened?

- You reset Cognee’s memory so you’re working with a clean graph.
- You added two documents, each tagged with one or more `NodeSet` labels.
  - The first document is only linked to `AI_Memory`.
  - The second document is linked to both `AI_Memory` and `Graph_RAG`.
- When you ran `cognify()`, Cognee:
  - Created `NodeSet` nodes (`AI_Memory`, `Graph_RAG`) in the graph.
  - Attached each document to the corresponding NodeSets.
  - Extracted entities and relationships from the documents, then linked those entities back to the same NodeSets.

This means the tags you add flow down into the extracted entities:

- **“Cognee”** appears in both documents → connects to **both NodeSets**.
- **“AI memory”** appears only in the first → connects only to **AI_Memory**.
- **“Vector search”** appears only in the second → connects to **both** since that document belongs to **AI_Memory** and **Graph_RAG**.

Your NodeSets now unlock powerful search and navigation capabilities:

- You can filter searches by NodeSet.
- You can scope queries to specific NodeSets.
- You can navigate data by project or domain using NodeSets.

Further Concepts

# Ontologies

Copy page

Enrich your knowledge graph with external vocabularies

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/ontologies#what-is-an-ontology-in-cognee)

What is an ontology in Cognee?

An **ontology** is an optional RDF/OWL file you can provide to Cognee. It acts as a **reference vocabulary**, making sure that entity types (“classes”) and entity mentions (“individuals”) extracted from your data are linked to canonical, well-defined concepts.

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/ontologies#how-it-works)

How it works

- You pass `ontology_file_path="my_ontology.owl"` when running [Cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify).
- Cognee parses the file with [RDFLib](https://rdflib.dev/) and loads its classes and relationships.
- During graph extraction, entities and types are checked against the ontology:
  - If a match is found, the node is marked `ontology_valid=True`.
  - Parent classes and object-property links from the ontology are attached as extra edges.
- If no ontology is provided, extraction still works, just without validation or enrichment.

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/ontologies#why-use-an-ontology)

Why use an ontology

- **Consistency**: standardize how entities and types are represented
- **Enrichment**: bring in inherited relationships from a domain schema
- **Control**: align Cognee’s graph with existing enterprise or scientific vocabularies

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/ontologies#where-to-get-ontologies)

Where to get ontologies

Ontologies are an art and science on their own. Cognee works best with **manually curated, focused ontologies** that fit your dataset. The simplest way to start is to **create a small ontology yourself** — just a few classes and relationships that match the entities you expect.Public resources like **Wikidata** or **DBpedia** define millions of classes and entities, which makes them too big to use directly in Cognee. If you are not creating an ontology from scratch, you can start from a public one — but always work with a subset, not the full ontology:

- **Select only the pieces you need** (specific classes, properties, or individuals)
- **Save the subset** in a format Cognee can parse with [`rdflib`](https://rdflib.readthedocs.io/)
- **If needed, enrich the subset manually** by adding extra classes or relationships relevant to your domain
- **Keep it small and relevant** so matching stays precise and performance remains fast

Common sources

Why subsetting is essential

How subsetting works

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/ontologies#supported-formats)

Supported formats

Any format [RDFLib](https://rdflib.readthedocs.io/) can parse:

- RDF/XML (`.owl`, `.rdf`)
- Turtle (`.ttl`)
- N-Triples, JSON-LD, and others

## 

[​

](https://docs.cognee.ai/core-concepts/further-concepts/ontologies#practical-example)

Practical example

Once you have your subset file, integrating it into Cognee is simple:

```
import cognee

await cognee.cognify(
    datasets=["my_dataset"],
    ontology_file_path="subset.owl",  # your curated subset here
)
```

For more detailed examples of working with ontologies in Cognee, check out the demo scripts in the repository:

- [Basic ontology demo](https://github.com/topoteretes/cognee/blob/main/examples/python/ontology_demo_example.py) - Shows fundamental ontology integration
- [Advanced ontology demo](https://github.com/topoteretes/cognee/blob/main/examples/python/ontology_demo_example_2.py) - Demonstrates more complex ontology workflows

Further Concepts

# Sessions and Caching

Copy page

Understanding how Cognee maintains conversational memory through sessions and cache adapters

In Cognee, a session defines the scope for a single conversation or agent run. It maintains a cache of short-term information, including recent queries, responses, and the context used to answer them.

## 

[​

](https://docs.cognee.ai/core-concepts/sessions-and-caching#what-is-a-session)

What Is a Session?

A session is Cognee’s short-term memory for a specific user during search operations. It is identified by `(user_id, session_id)` and stores an ordered list of recent interactions created by calls to `cognee.search()`.Each interaction is stored as a dictionary containing:

- `time` – when the turn was created (UTC, ISO format)
- `question` – the user’s query
- `context` – summarized context Cognee used to answer
- `answer` – the model’s response

Cognee reads from this session memory at the start of a search to recover earlier turns. When the search finishes, it writes a new interaction to the session so the history grows over time.Using the same `session_id` across searches allows Cognee to include previous interactions as conversational history in the LLM prompt, enabling follow-up questions and contextual awareness.

Sessions require caching to be enabled. See the next sections and [Configuration Details](https://docs.cognee.ai/core-concepts/sessions-and-caching#configuration-details) below. If caching is disabled or unavailable, searches still work but without access to previous interactions.

## 

[​

](https://docs.cognee.ai/core-concepts/sessions-and-caching#how-sessions-work)

How Sessions Work

Sessions are used during [search operations](https://docs.cognee.ai/core-concepts/main-operations/search). When you call `cognee.search()` with a `session_id`:

1. **Retrieve context** – Cognee finds relevant graph elements for your query
2. **Load conversation history** – If caching is enabled, previous interactions for `(user_id, session_id)` are loaded
3. **Generate answer** – The LLM receives the query, graph context, and retrieved history
4. **Save interaction** – A new Q&A entry is stored in the session cache

## 

[​

](https://docs.cognee.ai/core-concepts/sessions-and-caching#cache-adapters)

Cache Adapters

Cognee supports two cache adapters for storing sessions. Redis is recommended for distributed or multi-process setups, while Filesystem can be used when you need a simple local cache without network dependencies. Both provide the same functionality; only the storage backend differs. Below are the configuration options for each adapter with additional details.

- Redis

- Filesystem

Add to your `.env` file:

```
CACHING=true
CACHE_BACKEND=redis
CACHE_HOST=localhost
CACHE_PORT=6379
```

**Start Redis:**

```
# Using Docker
docker run -d -p 6379:6379 redis:latest

# Or using local installation
redis-server
```

- Fast in-memory storage with built-in expiration
- Supports shared locks for Kuzu (multi-process coordination)
- Requires a running Redis instance and network connectivity

Session Data Structure

Sessions store interactions as JSON entries in a list. Each entry contains:

- **time**: ISO 8601 timestamp (UTC)
- **question**: The user’s query text
- **context**: Summarized graph context used for the answer
- **answer**: The LLM’s response

Sessions are keyed by: `agent_sessions:{user_id}:{session_id}`Each user can have multiple sessions, each maintaining its own cache of short-term information.

Configuration Details

**Environment Variables:**

- `CACHING` (bool): Enable/disable caching (default: `false`)
- `CACHE_BACKEND` (str): `"redis"` or `"fs"` (default: `"redis"` if `CACHING=true`)
- `CACHE_HOST` (str): Redis hostname (default: `"localhost"`)
- `CACHE_PORT` (int): Redis port (default: `6379`)
- `CACHE_USERNAME` (str, optional): Redis username
- `CACHE_PASSWORD` (str, optional): Redis password

**TTL (Time to Live):**Sessions expire after a configurable TTL (default: 86400 seconds = 24 hours). Expired sessions are automatically cleaned up.

Adapter Comparison

| Feature          | Redis                   | Filesystem             |
| ---------------- | ----------------------- | ---------------------- |
| Storage          | In-memory (Redis)       | Local disk (diskcache) |
| Performance      | Very fast               | Fast (local I/O)       |
| Multi-process    | ✅ Supported             | ❌ Not supported        |
| Shared locks     | ✅ Yes                   | ❌ No                   |
| Network required | ✅ Yes                   | ❌ No                   |
| Setup complexity | Medium                  | Low                    |
| Best for         | Production, distributed | Development, local     |

[

## Search

Learn how sessions integrate with search

](https://docs.cognee.ai/core-concepts/main-operations/search)[

## Sessions Guide

Practical examples with Redis and filesystem

](https://docs.cognee.ai/guides/sessions)[

## Setup Configuration

Configure cache adapters

](https://docs.cognee.ai/setup-configuration/overview)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/core-concepts/further-concepts/ontologies)[

Multi-User Mode OverviewHow Cognee handles multiple users and data isolation between users.

Next

](https://docs.cognee.ai/core-concepts/multi-user-mode/multi-user-mode-overview)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)

Setup Configuration

# Setup Configuration

Copy page

Configure Cognee to use your preferred LLM, embedding engine, and storage backends

Configure Cognee to use your preferred LLM, embedding engine, relational database, vector store, and graph store via environment variables in a local `.env` file.This section provides beginner-friendly guides for setting up different backends, with detailed technical information available in expandable sections.

## 

[​

](https://docs.cognee.ai/setup-configuration/overview#what-you-can-configure)

What You Can Configure

Cognee uses a flexible architecture that lets you choose the best tools for your needs. We recommend starting with the defaults to get familiar with Cognee, then customizing each component as needed:

- **[LLM Providers](https://docs.cognee.ai/setup-configuration/llm-providers)** — Choose from OpenAI, Azure OpenAI, Google Gemini, Anthropic, Ollama, or custom providers (like vLLM) for text generation and reasoning tasks
- **[Structured Output Backends](https://docs.cognee.ai/setup-configuration/structured-output-backends)** — Configure LiteLLM + Instructor or BAML for reliable data extraction from LLM responses
- **[Embedding Providers](https://docs.cognee.ai/setup-configuration/embedding-providers)** — Select from OpenAI, Azure OpenAI, Google Gemini, Mistral, Ollama, Fastembed, or custom embedding services to create vector representations for semantic search
- **[Relational Databases](https://docs.cognee.ai/setup-configuration/relational-databases)** — Use SQLite for local development or Postgres for production to store metadata, documents, and system state
- **[Vector Stores](https://docs.cognee.ai/setup-configuration/vector-stores)** — Store embeddings in LanceDB, PGVector, Qdrant, Redis, ChromaDB, FalkorDB, or Neptune Analytics for similarity search
- **[Graph Stores](https://docs.cognee.ai/setup-configuration/graph-stores)** — Build knowledge graphs with Kuzu, Kuzu-remote, Neo4j, Neptune, or Neptune Analytics to manage relationships and reasoning
- **[Dataset Separation & Access Control](https://docs.cognee.ai/setup-configuration/permissions)** — Configure dataset-level permissions and isolation
- **[Sessions & Caching](https://docs.cognee.ai/core-concepts/sessions-and-caching)** — Enable conversational memory with Redis or filesystem cache adapters

Dataset isolation is not enabled by default; see [how to enable it](https://docs.cognee.ai/core-concepts/multi-user-mode/permissions-system/datasets#dataset-isolation).

## 

[​

](https://docs.cognee.ai/setup-configuration/overview#observability-&-telemetry)

Observability & Telemetry

Cognee includes built-in telemetry to help you monitor and debug your knowledge graph operations. You can control telemetry behavior with environment variables:

- **`TELEMETRY_DISABLED`** (boolean, optional): Set to `true` to disable all telemetry collection (default: `false`)

When telemetry is enabled, Cognee automatically collects:

- Search query performance metrics
- Processing pipeline execution times
- Error rates and debugging information
- System resource usage

Telemetry data helps improve Cognee’s performance and reliability. It’s collected anonymously and doesn’t include your actual data content.

## 

[​

](https://docs.cognee.ai/setup-configuration/overview#configuration-workflow)

Configuration Workflow

1. Install Cognee with all optional dependencies:
   - **Local setup**: `uv sync --all-extras`
   - **Library**: `pip install "cognee[all]"`
2. Create a `.env` file in your project root (if you haven’t already) — see [Installation](https://docs.cognee.ai/getting-started/installation) for details
3. Choose your preferred providers and follow the configuration instructions from the guides below

**Configuration Changes**: If you’ve already run Cognee with default settings and are now changing your configuration (e.g., switching from SQLite to Postgres, or changing vector stores), you should call pruning operations before the next cognification to ensure data consistency.

**LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.



Setup Configuration

# LLM Providers

Copy page

Configure LLM providers for text generation and reasoning in Cognee

LLM (Large Language Model) providers handle text generation, reasoning, and structured output tasks in Cognee. You can choose from cloud providers like OpenAI and Anthropic, or run models locally with Ollama.

**New to configuration?**See the [Setup Configuration Overview](https://docs.cognee.ai/setup-configuration/overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## 

[​

](https://docs.cognee.ai/setup-configuration/llm-providers#supported-providers)

Supported Providers

Cognee supports multiple LLM providers:

- **OpenAI** — GPT models via OpenAI API (default)
- **Azure OpenAI** — GPT models via Azure OpenAI Service
- **Google Gemini** — Gemini models via Google AI
- **Anthropic** — Claude models via Anthropic API
- **AWS Bedrock** — Models available via AWS Bedrock
- **Ollama** — Local models via Ollama
- **LM Studio** — Local models via LM Studio
- **Custom** — OpenAI-compatible endpoints (like vLLM)

**LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.

## 

[​

](https://docs.cognee.ai/setup-configuration/llm-providers#configuration)

Configuration

Environment Variables

Set these environment variables in your `.env` file:

- `LLM_PROVIDER` — The provider to use (openai, gemini, anthropic, ollama, custom)
- `LLM_MODEL` — The specific model to use
- `LLM_API_KEY` — Your API key for the provider
- `LLM_ENDPOINT` — Custom endpoint URL (for Azure, Ollama, or custom providers)
- `LLM_API_VERSION` — API version (for Azure OpenAI)
- `LLM_MAX_TOKENS` — Maximum tokens per request (optional)

## 

[​

](https://docs.cognee.ai/setup-configuration/llm-providers#provider-setup-guides)

Provider Setup Guides

OpenAI (Default)

OpenAI is the default provider and works out of the box with minimal configuration.

```
LLM_PROVIDER="openai"
LLM_MODEL="gpt-4o-mini"
LLM_API_KEY="sk-..."
# Optional overrides
# LLM_ENDPOINT=https://api.openai.com/v1
# LLM_API_VERSION=
# LLM_MAX_TOKENS=16384
```

Azure OpenAI

Use Azure OpenAI Service with your own deployment.

```
LLM_PROVIDER="openai"
LLM_MODEL="azure/gpt-4o-mini"
LLM_ENDPOINT="https://<your-resource>.openai.azure.com/openai/deployments/gpt-4o-mini"
LLM_API_KEY="az-..."
LLM_API_VERSION="2024-12-01-preview"
```

Google Gemini

Use Google’s Gemini models for text generation.

```
LLM_PROVIDER="gemini"
LLM_MODEL="gemini/gemini-2.0-flash"
LLM_API_KEY="AIza..."
# Optional
# LLM_ENDPOINT=https://generativelanguage.googleapis.com/
# LLM_API_VERSION=v1beta
```

Anthropic

Use Anthropic’s Claude models for reasoning tasks.

```
LLM_PROVIDER="anthropic"
LLM_MODEL="claude-3-5-sonnet-20241022"
LLM_API_KEY="sk-ant-..."
```

AWS Bedrock

Use models available on AWS Bedrock for various tasks. For Bedrock specifically, you will need to also specify some information regarding AWS.

```
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

There are **multiple ways of connecting** to Bedrock models:

1. Using an API key and region. Simply generate you key on AWS, and put it in the `LLM_API_KEY` env variable.
2. Using AWS Credentials. You can only specify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, no need for the `LLM_API_KEY`. In this case, if you are using temporary credentials (e.g. `AWS_ACCESS_KEY_ID` starting with `ASIA...`), then you also must specify the `AWS_SESSION_TOKEN`.
3. Using AWS profiles. Create a file called something like `/.aws/credentials`, and store your credentials inside it.

**Installation**: Install the required dependency:

```
pip install cognee[aws]
```

**Model Name** The name of the model might differ based on the region (the name begins with **eu** for Europe, **us** of USA, etc.)

Ollama (Local)

Run models locally with Ollama for privacy and cost control.

```
LLM_PROVIDER="ollama"
LLM_MODEL="llama3.1:8b"
LLM_ENDPOINT="http://localhost:11434/v1"
LLM_API_KEY="ollama"
```

**Installation**: Install Ollama from [ollama.ai](https://ollama.ai/) and pull your desired model:

```
ollama pull llama3.1:8b
```

### 

[​

](https://docs.cognee.ai/setup-configuration/llm-providers#known-issues)

Known Issues

- **Requires `HUGGINGFACE_TOKENIZER`**: Ollama currently needs this env var set even when used only as LLM. Fix in progress.
- **`NoDataError` with mixed providers**: Using Ollama as LLM and OpenAI as embedding provider may fail with `NoDataError`. Workaround: use the same provider for both.

LM Studio (Local)

Run models locally with LM Studio for privacy and cost control.

```
LLM_PROVIDER="custom"
LLM_MODEL="lm_studio/magistral-small-2509"
LLM_ENDPOINT="http://127.0.0.1:1234/v1"
LLM_API_KEY="."
LLM_INSTRUCTOR_MODE="json_schema_mode"
```

**Installation**: Install LM Studio from [lmstudio.ai](https://lmstudio.ai/) and download your desired model from LM Studio’s interface. Load your model, start the LM Studio server, and Cognee will be able to connect to it.

**Set up instructor mode** The `LLM_INSTRUCTOR_MODE` env variable controls the LiteLLM instructor [mode](https://python.useinstructor.com/modes-comparison/), i.e. the model’s response type. This may vary depending on the model, and you would need to change it accordingly.

Custom Providers

Use OpenAI-compatible endpoints like OpenRouter or other services.

```
LLM_PROVIDER="custom"
LLM_MODEL="openrouter/google/gemini-2.0-flash-lite-preview-02-05:free"
LLM_ENDPOINT="https://openrouter.ai/api/v1"
LLM_API_KEY="or-..."
# Optional fallback chain
# FALLBACK_MODEL=
# FALLBACK_ENDPOINT=
# FALLBACK_API_KEY=
```

**Custom Provider Prefixes**: When using `LLM_PROVIDER="custom"`, you must include the correct provider prefix in your model name. Cognee forwards requests to [LiteLLM](https://docs.litellm.ai/docs/providers), which uses these prefixes to route requests correctly.Common prefixes include:

- `hosted_vllm/` — vLLM servers
- `openrouter/` — OpenRouter
- `lm_studio/` — LM Studio
- `openai/` — OpenAI-compatible APIs

See the [LiteLLM providers documentation](https://docs.litellm.ai/docs/providers) for the full list of supported prefixes.Below is an example for vLLm:

vLLM

Use vLLM for high-performance model serving with OpenAI-compatible API.

```
LLM_PROVIDER="custom"
LLM_MODEL="hosted_vllm/<your-model-name>"
LLM_ENDPOINT="https://your-vllm-endpoint/v1"
LLM_API_KEY="."
```

**Example with Gemma:**

```
LLM_PROVIDER="custom"
LLM_MODEL="hosted_vllm/gemma-3-12b"
LLM_ENDPOINT="https://your-vllm-endpoint/v1"
LLM_API_KEY="."
```

**Important**: The `hosted_vllm/` prefix is required for LiteLLM to correctly route requests to your vLLM server. The model name after the prefix should match the model ID returned by your vLLM server’s `/v1/models` endpoint.

To find the correct model name, see [their documentation](https://docs.litellm.ai/docs/providers/vllm).

## 

[​

](https://docs.cognee.ai/setup-configuration/llm-providers#advanced-options)

Advanced Options

Rate Limiting

Control client-side throttling for LLM calls to manage API usage and costs.**Configuration (in .env):**

```
LLM_RATE_LIMIT_ENABLED="true"
LLM_RATE_LIMIT_REQUESTS="60"
LLM_RATE_LIMIT_INTERVAL="60"
```

**How it works:**

- **Client-side limiter**: Cognee paces outbound LLM calls before they reach the provider
- **Moving window**: Spreads allowance across the time window for smoother throughput
- **Per-process scope**: In-memory limits don’t share across multiple processes/containers
- **Auto-applied**: Works with all providers (OpenAI, Gemini, Anthropic, Ollama, Custom)

**Example**: `60` requests per `60` seconds ≈ 1 request/second average rate.

## 

[​

](https://docs.cognee.ai/setup-configuration/llm-providers#notes)

Notes

- If `EMBEDDING_API_KEY` is not set, Cognee falls back to `LLM_API_KEY` for embeddings
- Rate limiting helps manage API usage and costs
- Structured output frameworks ensure consistent data extraction from LLM responses
- If you are using `Instructor` as the structured output framework, you can control the response type of the LLM through the `LLM_INSTRUCTOR_MODE` env variable, which sets the corresponding instructor [mode](https://python.useinstructor.com/modes-comparison/) (e.g. `json_mode` for JSON output)

Setup Configuration

# Structured Output Backends

Copy page

Configure structured output frameworks for reliable data extraction in Cognee

Structured output backends ensure reliable data extraction from LLM responses. Cognee supports two frameworks that convert LLM text into structured Pydantic models for knowledge graph extraction and other tasks.

**New to configuration?**See the [Setup Configuration Overview](https://docs.cognee.ai/setup-configuration/overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## 

[​

](https://docs.cognee.ai/setup-configuration/structured-output-backends#supported-frameworks)

Supported Frameworks

Cognee supports two structured output approaches:

- **LiteLLM + Instructor** — Provider-agnostic client with Pydantic coercion (default)
- **BAML** — DSL-based framework with type registry and guardrails

Both frameworks produce the same Pydantic-validated outputs, so your application code remains unchanged regardless of which backend you choose.

## 

[​

](https://docs.cognee.ai/setup-configuration/structured-output-backends#how-it-works)

How It Works

Cognee uses a unified interface that abstracts the underlying framework:

```
from cognee.infrastructure.llm.LLMGateway import LLMGateway
await LLMGateway.acreate_structured_output(text, system_prompt, response_model)
```

The `STRUCTURED_OUTPUT_FRAMEWORK` environment variable determines which backend processes your requests, but the API remains identical.

## 

[​

](https://docs.cognee.ai/setup-configuration/structured-output-backends#configuration)

Configuration

- LiteLLM + Instructor (Default)

- BAML

```
STRUCTURED_OUTPUT_FRAMEWORK=instructor
```

## 

[​

](https://docs.cognee.ai/setup-configuration/structured-output-backends#important-notes)

Important Notes

- **Unified Interface**: Your application code uses the same `acreate_structured_output()` call regardless of framework
- **Provider Flexibility**: Both frameworks support the same LLM providers
- **Output Consistency**: Both produce identical Pydantic-validated results
- **Performance**: Framework choice doesn’t significantly impact performance

[

](https://docs.cognee.ai/setup-configuration/llm-providers)



Setup Configuration

# Embedding Providers

Copy page

Configure embedding providers for semantic search in Cognee

Embedding providers convert text into vector representations that enable semantic search. These vectors capture the meaning of text, allowing Cognee to find conceptually related content even when the wording is different.

**New to configuration?**See the [Setup Configuration Overview](https://docs.cognee.ai/setup-configuration/overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## 

[​

](https://docs.cognee.ai/setup-configuration/embedding-providers#supported-providers)

Supported Providers

Cognee supports multiple embedding providers:

- **OpenAI** — Text embedding models via OpenAI API (default)
- **Azure OpenAI** — Text embedding models via Azure OpenAI Service
- **Google Gemini** — Embedding models via Google AI
- **Mistral** — Embedding models via Mistral AI
- **AWS Bedrock** — Embedding models via AWS Bedrock
- **Ollama** — Local embedding models via Ollama
- **LM Studio** — Local embedding models via LM Studio
- **Fastembed** — CPU-friendly local embeddings
- **Custom** — OpenAI-compatible embedding endpoints

**LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.

## 

[​

](https://docs.cognee.ai/setup-configuration/embedding-providers#configuration)

Configuration

Environment Variables

Set these environment variables in your `.env` file:

- `EMBEDDING_PROVIDER` — The provider to use (openai, gemini, mistral, ollama, fastembed, custom)
- `EMBEDDING_MODEL` — The specific embedding model to use
- `EMBEDDING_DIMENSIONS` — The vector dimension size (must match your vector store)
- `EMBEDDING_API_KEY` — Your API key (falls back to `LLM_API_KEY` if not set)
- `EMBEDDING_ENDPOINT` — Custom endpoint URL (for Azure, Ollama, or custom providers)
- `EMBEDDING_API_VERSION` — API version (for Azure OpenAI)
- `EMBEDDING_MAX_TOKENS` — Maximum tokens per request (optional)

## 

[​

](https://docs.cognee.ai/setup-configuration/embedding-providers#provider-setup-guides)

Provider Setup Guides

OpenAI (Default)

OpenAI provides high-quality embeddings with good performance.

```
EMBEDDING_PROVIDER="openai"
EMBEDDING_MODEL="openai/text-embedding-3-large"
EMBEDDING_DIMENSIONS="3072"
# Optional
# EMBEDDING_API_KEY=sk-...   # falls back to LLM_API_KEY if omitted
# EMBEDDING_ENDPOINT=https://api.openai.com/v1
# EMBEDDING_API_VERSION=
# EMBEDDING_MAX_TOKENS=8191
```

Azure OpenAI Embeddings

Use Azure OpenAI Service for embeddings with your own deployment.

```
EMBEDDING_PROVIDER="openai"
EMBEDDING_MODEL="azure/text-embedding-3-large"
EMBEDDING_ENDPOINT="https://<your-az>.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large"
EMBEDDING_API_KEY="az-..."
EMBEDDING_API_VERSION="2023-05-15"
EMBEDDING_DIMENSIONS="3072"
```

Google Gemini

Use Google’s embedding models for semantic search.

```
EMBEDDING_PROVIDER="gemini"
EMBEDDING_MODEL="gemini/text-embedding-004"
EMBEDDING_API_KEY="AIza..."
EMBEDDING_DIMENSIONS="768"
```

Mistral

Use Mistral’s embedding models for high-quality vector representations.

```
EMBEDDING_PROVIDER="mistral"
EMBEDDING_MODEL="mistral/mistral-embed"
EMBEDDING_API_KEY="sk-mis-..."
EMBEDDING_DIMENSIONS="1024"
```

**Installation**: Install the required dependency:

```
pip install mistral-common[sentencepiece]
```

AWS Bedrock

Use embedding models provided by the AWS Bedrock service.

```
EMBEDDING_PROVIDER="bedrock"
EMBEDDING_MODEL="<your_model_name>"
EMBEDDING_DIMENSIONS="<dimensions_of_the_model>"
EMBEDDING_API_KEY="<your_api_key>"
EMBEDDING_MAX_TOKENS="<max_tokens_of_your_model>"
```

Ollama (Local)

Run embedding models locally with Ollama for privacy and cost control.

```
EMBEDDING_PROVIDER="ollama"
EMBEDDING_MODEL="nomic-embed-text:latest"
EMBEDDING_ENDPOINT="http://localhost:11434/api/embed"
EMBEDDING_DIMENSIONS="768"
HUGGINGFACE_TOKENIZER="nomic-ai/nomic-embed-text-v1.5"
```

**Installation**: Install Ollama from [ollama.ai](https://ollama.ai/) and pull your desired embedding model:

```
ollama pull nomic-embed-text:latest
```

LM Studio (Local)

Run embedding models locally with LM Studio for privacy and cost control.

```
EMBEDDING_PROVIDER="custom"
EMBEDDING_MODEL="lm_studio/text-embedding-nomic-embed-text-1.5"
EMBEDDING_ENDPOINT="http://127.0.0.1:1234/v1"
EMBEDDING_API_KEY="."
EMBEDDING_DIMENSIONS="768"
```

**Installation**: Install LM Studio from [lmstudio.ai](https://lmstudio.ai/) and download your desired model from LM Studio’s interface. Load your model, start the LM Studio server, and Cognee will be able to connect to it.

Fastembed (Local)

Use Fastembed for CPU-friendly local embeddings without GPU requirements.

```
EMBEDDING_PROVIDER="fastembed"
EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS="384"
```

**Installation**: Fastembed is included by default with Cognee.**Known Issues**:

- As of September 2025, Fastembed requires Python < 3.13 (not compatible with Python 3.13+)

Custom Providers

Use OpenAI-compatible embedding endpoints from other providers.

```
EMBEDDING_PROVIDER="custom"
EMBEDDING_MODEL="provider/your-embedding-model"
EMBEDDING_ENDPOINT="https://your-endpoint.example.com/v1"
EMBEDDING_API_KEY="provider-..."
EMBEDDING_DIMENSIONS="<match-your-model>"
```

## 

[​

](https://docs.cognee.ai/setup-configuration/embedding-providers#advanced-options)

Advanced Options

Rate Limiting

```
EMBEDDING_RATE_LIMIT_ENABLED="true"
EMBEDDING_RATE_LIMIT_REQUESTS="10"
EMBEDDING_RATE_LIMIT_INTERVAL="5"
```

Testing and Development

```
# Mock embeddings for testing (returns zero vectors)
MOCK_EMBEDDING="true"
```

## 

[​

](https://docs.cognee.ai/setup-configuration/embedding-providers#important-notes)

Important Notes

- **Dimension Consistency**: `EMBEDDING_DIMENSIONS` must match your vector store collection schema
- **API Key Fallback**: If `EMBEDDING_API_KEY` is not set, Cognee uses `LLM_API_KEY` (except for custom providers)
- **Tokenization**: For Ollama and Hugging Face models, set `HUGGINGFACE_TOKENIZER` for proper token counting
- **Performance**: Local providers (Ollama, Fastembed) are slower but offer privacy and cost benefits



Setup Configuration

# Relational Databases

Copy page

Configure relational databases for metadata and state storage in Cognee

Relational databases store metadata, document information, and system state in Cognee. They track documents, chunks, and provenance (where data came from and how it’s linked).

**New to configuration?**See the [Setup Configuration Overview](https://docs.cognee.ai/setup-configuration/overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## 

[​

](https://docs.cognee.ai/setup-configuration/relational-databases#supported-providers)

Supported Providers

Cognee supports two relational database options:

- **SQLite** — File-based database, works out of the box (default)
- **Postgres** — Production-ready database for multi-process concurrency

## 

[​

](https://docs.cognee.ai/setup-configuration/relational-databases#configuration)

Configuration

Environment Variables

Set these environment variables in your `.env` file:

- `DB_PROVIDER` — The database provider (sqlite, postgres)
- `DB_NAME` — Database name
- `DB_HOST` — Database host (Postgres only)
- `DB_PORT` — Database port (Postgres only)
- `DB_USERNAME` — Database username (Postgres only)
- `DB_PASSWORD` — Database password (Postgres only)

## 

[​

](https://docs.cognee.ai/setup-configuration/relational-databases#setup-guides)

Setup Guides

SQLite (Default)

SQLite is file-based and requires no additional setup. It’s perfect for local development and single-user scenarios.

```
DB_PROVIDER="sqlite"
DB_NAME="cognee_db"
```

**Installation**: SQLite is included by default with Cognee. No additional installation required.**Data Location**: Data is stored under the Cognee system directory. You can override the root with `SYSTEM_ROOT_DIRECTORY` in your `.env` file.

Postgres

Postgres is recommended for production environments, multi-process concurrency, or when you need external hosting.

```
DB_PROVIDER="postgres"
DB_NAME="cognee_db"
DB_HOST="127.0.0.1"            # use host.docker.internal when running inside Docker
DB_PORT="5432"
DB_USERNAME="cognee"
DB_PASSWORD="cognee"
```

**Installation**: Install the Postgres extras:

```
pip install "cognee[postgres]"
# or for binary version
pip install "cognee[postgres-binary]"
```

**Docker Setup**: Use the built-in Postgres service:

```
docker compose --profile postgres up -d
```

**Docker Networking**: When running Cognee in Docker and Postgres on your host, set:

```
DB_HOST="host.docker.internal"
```

## 

[​

](https://docs.cognee.ai/setup-configuration/relational-databases#advanced-options)

Advanced Options

Migration Configuration

Use migration settings to extract data from a relational database and load it into the graph store.

```
MIGRATION_DB_PROVIDER="sqlite"   # or postgres
MIGRATION_DB_PATH="/path/to/migration/directory"
MIGRATION_DB_NAME="migration_database.sqlite"
# For Postgres migrations
# MIGRATION_DB_HOST=127.0.0.1
# MIGRATION_DB_PORT=5432
# MIGRATION_DB_USERNAME=cognee
# MIGRATION_DB_PASSWORD=cognee
```

Backend Access Control

Enable per-user dataset isolation for multi-tenant scenarios.

```
ENABLE_BACKEND_ACCESS_CONTROL="true"
```

This feature is available for both SQLite and Postgres.

## 

[​

](https://docs.cognee.ai/setup-configuration/relational-databases#troubleshooting)

Troubleshooting

Common Issues

**Postgres Connectivity**: Verify the database is listening on `DB_HOST:DB_PORT` and credentials are correct:

```
psql -h 127.0.0.1 -U cognee -d cognee_db
```

**Docker Networking**: Use `host.docker.internal` for host-to-container access on macOS/Windows.**SQLite Concurrency**: SQLite has limited write concurrency; prefer Postgres for heavy multi-user workloads.

## 

[​

](https://docs.cognee.ai/setup-configuration/relational-databases#when-to-use-each)

When to Use Each

- **SQLite**: Local development, single-user applications, simple deployments
- **Postgres**: Production environments, multi-user applications, external hosting, co-location with pgvector



Setup Configuration

# Vector Stores

Copy page

Configure vector databases for embedding storage and semantic search in Cognee

Vector stores hold embeddings for semantic similarity search. They enable Cognee to find conceptually related content based on meaning rather than exact text matches.

**New to configuration?**See the [Setup Configuration Overview](https://docs.cognee.ai/setup-configuration/overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## 

[​

](https://docs.cognee.ai/setup-configuration/vector-stores#supported-providers)

Supported Providers

Cognee supports multiple vector store options:

- **LanceDB** — File-based vector store, works out of the box (default)
- **PGVector** — Postgres-backed vector storage with pgvector extension
- **Qdrant** — High-performance vector database and similarity search engine
- **Redis** — Fast vector similarity search via Redis Search module
- **ChromaDB** — HTTP server-based vector database
- **FalkorDB** — Hybrid graph + vector database
- **Neptune Analytics** — Amazon Neptune Analytics hybrid solution

## 

[​

](https://docs.cognee.ai/setup-configuration/vector-stores#configuration)

Configuration

Environment Variables

## 

[​

](https://docs.cognee.ai/setup-configuration/vector-stores#setup-guides)

Setup Guides

LanceDB (Default)

LanceDB is file-based and requires no additional setup. It’s perfect for local development and single-user scenarios.

```
VECTOR_DB_PROVIDER="lancedb"
# Optional, can be a path or URL. Defaults to <SYSTEM_ROOT_DIRECTORY>/databases/cognee.lancedb
# VECTOR_DB_URL=/absolute/or/relative/path/to/cognee.lancedb
```

**Installation**: LanceDB is included by default with Cognee. No additional installation required.**Data Location**: Vectors are stored in a local directory. Defaults under the Cognee system path if `VECTOR_DB_URL` is empty.

PGVector

PGVector stores vectors inside your Postgres database using the pgvector extension.

```
VECTOR_DB_PROVIDER="pgvector"
# Uses the same Postgres connection as your relational DB (DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD)
```

**Installation**: Install the Postgres extras:

```
pip install "cognee[postgres]"
# or for binary version
pip install "cognee[postgres-binary]"
```

**Docker Setup**: Use the built-in Postgres with pgvector:

```
docker compose --profile postgres up -d
```

**Note**: If using your own Postgres, ensure `CREATE EXTENSION IF NOT EXISTS vector;` is available in the target database.

Qdrant

Qdrant requires a running instance of the Qdrant server.

```
VECTOR_DB_PROVIDER="qdrant"
VECTOR_DB_URL="http://localhost:6333"
```

**Installation**: Since Qdrant is a community adapter, you have to install the community package:

```
pip install cognee-community-vector-adapter-qdrant
```

**Configuration**: To make sure Cognee uses Qdrant, you have to register it beforehand with the following line:

```
from cognee_community_vector_adapter_qdrant import register
```

For more details on setting up Qdrant, visit the [more detailed description](https://docs.cognee.ai/setup-configuration/community-maintained/qdrant) of this adapter.**Docker Setup**: Start the Qdrant service:

```
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

**Access**: Default port is 6333 for the database, and you can access the Qdrant dashboard at “localhost:6333/dashboard”.

Redis

Redis can be used as a vector store through the Redis Search module, providing fast vector similarity search capabilities.

```
VECTOR_DB_PROVIDER="redis"
VECTOR_DB_URL="redis://localhost:6379"
# VECTOR_DB_KEY is optional and not used by Redis
```

**Installation**: Since Redis is a community adapter, you have to install the community package:

```
pip install cognee-community-vector-adapter-redis
```

**Configuration**: To make sure Cognee uses Redis, you have to register it beforehand with the following line:

```
from cognee_community_vector_adapter_redis import register
```

You can also configure Redis programmatically:

```
from cognee import config

config.set_vector_db_config({
    "vector_db_provider": "redis",
    "vector_db_url": "redis://localhost:6379",
})
```

For more details on setting up Redis, visit the [more detailed description](https://docs.cognee.ai/setup-configuration/community-maintained/redis) of this adapter.**Docker Setup**: Start a Redis instance with Search module enabled:

```
docker run -d --name redis -p 6379:6379 redis:8.0.2
```

Or use **Redis Cloud** with the Search module enabled: [Redis Cloud](https://redis.io/try-free)**Connection URL Examples**:

- Local: `redis://localhost:6379`
- With authentication: `redis://user:password@localhost:6379`
- With SSL: `rediss://localhost:6380`

ChromaDB

ChromaDB requires a running Chroma server and authentication token.

```
VECTOR_DB_PROVIDER="chromadb"
VECTOR_DB_URL="http://localhost:3002"
VECTOR_DB_KEY="<your_token>"
```

**Installation**: Install ChromaDB extras:

```
pip install "cognee[chromadb]"
# or directly
pip install chromadb
```

**Docker Setup**: Start the bundled ChromaDB server:

```
docker compose --profile chromadb up -d
```

FalkorDB

FalkorDB can serve as both graph and vector store, providing a hybrid solution.

```
VECTOR_DB_PROVIDER="falkordb"
VECTOR_DB_URL="localhost"
VECTOR_DB_PORT="6379"
```

**Installation**: Since FalkorDB is a community adapter, you have to install the community package:

```
pip install cognee-community-hybrid-adapter-falkor
```

**Configuration**: To make sure Cognee uses FalkorDB, you have to register it beforehand with the following line:

```
from cognee_community_hybrid_adapter_falkor import register
```

For more details on setting up FalkorDB, visit the [more detailed description](https://docs.cognee.ai/setup-configuration/community-maintained/falkordb) of this adapter.**Docker Setup**: Start the FalkorDB service:

```
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge
```

**Access**: Default ports are 6379 (DB) and 3000 (UI).

Neptune Analytics

Use Amazon Neptune Analytics as a hybrid vector + graph backend.

```
VECTOR_DB_PROVIDER="neptune_analytics"
VECTOR_DB_URL="neptune-graph://<GRAPH_ID>"
# AWS credentials via environment or default SDK chain
```

**Installation**: Install Neptune extras:

```
pip install "cognee[neptune]"
```

**Note**: URL must start with `neptune-graph://` and AWS credentials should be configured via environment variables or AWS SDK.

## 

[​

](https://docs.cognee.ai/setup-configuration/vector-stores#important-considerations)

Important Considerations

Dimension Consistency

Ensure `EMBEDDING_DIMENSIONS` matches your vector store collection/table schemas:

- PGVector column size
- LanceDB Vector size
- ChromaDB collection schema

Changing dimensions requires recreating collections.

Provider Comparison

| Provider          | Setup             | Performance | Use Case                       |
| ----------------- | ----------------- | ----------- | ------------------------------ |
| LanceDB           | Zero setup        | Good        | Local development              |
| PGVector          | Postgres required | Excellent   | Production with Postgres       |
| Qdrant            | Server required   | Excellent   | High-performance vector search |
| Redis             | Server required   | Excellent   | Low-latency in-memory search   |
| ChromaDB          | Server required   | Good        | Dedicated vector store         |
| FalkorDB          | Server required   | Good        | Hybrid graph + vector          |
| Neptune Analytics | AWS required      | Excellent   | Cloud hybrid solution          |

## 

[​

](https://docs.cognee.ai/setup-configuration/vector-stores#community-maintained-providers)

Community-Maintained Providers

Additional vector stores are available through community-maintained adapters:

- **[Qdrant](https://docs.cognee.ai/setup-configuration/community-maintained/qdrant)** — Vector search engine with cloud and self-hosted options
- **[Redis](https://docs.cognee.ai/setup-configuration/community-maintained/redis)** — Fast vector similarity search
- **[FalkorDB](https://docs.cognee.ai/setup-configuration/community-maintained/falkordb)** — Hybrid vector and graph store
- **Milvus, Pinecone, Weaviate, and more** — See [all community adapters](https://docs.cognee.ai/setup-configuration/community-maintained/overview)

## 

[​

](https://docs.cognee.ai/setup-configuration/vector-stores#notes)

Notes

- **Embedding Integration**: Vector stores use your embedding engine from the Embeddings section
- **Dimension Matching**: Keep `EMBEDDING_DIMENSIONS` consistent between embedding provider and vector store
- **Performance**: Local providers (LanceDB) are simpler but cloud providers offer better scalability



Setup Configuration

# Graph Stores

Copy page

Configure graph databases for knowledge graph storage and relationship reasoning in Cognee

Graph stores capture entities and relationships in knowledge graphs. They enable Cognee to understand structure and navigate connections between concepts, providing powerful reasoning capabilities.

**New to configuration?**See the [Setup Configuration Overview](https://docs.cognee.ai/setup-configuration/overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#supported-providers)

Supported Providers

Cognee supports multiple graph store options:

- **Kuzu** — Local file-based graph database (default)
- **Kuzu-remote** — Kuzu with HTTP API access
- **Neo4j** — Production-ready graph database
- **Neptune** — Amazon Neptune cloud graph database
- **Neptune Analytics** — Amazon Neptune Analytics hybrid solution

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#configuration)

Configuration

Environment Variables

Set these environment variables in your `.env` file:

- `GRAPH_DATABASE_PROVIDER` — The graph store provider (kuzu, kuzu-remote, neo4j, neptune, neptune_analytics)
- `GRAPH_DATABASE_URL` — Database URL or connection string
- `GRAPH_DATABASE_USERNAME` — Database username (optional)
- `GRAPH_DATABASE_PASSWORD` — Database password (optional)
- `GRAPH_DATABASE_NAME` — Database name (optional)

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#setup-guides)

Setup Guides

Kuzu (Default)

Kuzu is file-based and requires no network setup. It’s perfect for local development and single-user scenarios.

```
GRAPH_DATABASE_PROVIDER="kuzu"
# Optional: override location
# SYSTEM_ROOT_DIRECTORY=/absolute/path/.cognee_system
# The graph file will default to <SYSTEM_ROOT_DIRECTORY>/databases/cognee_graph_kuzu
```

**Installation**: Kuzu is included by default with Cognee. No additional installation required.**Data Location**: The graph is stored on disk. Path defaults under the Cognee system directory and is created automatically.

**Concurrency Limitation**: Kuzu uses file-based locking and is not suitable for concurrent use from different agents or processes. For multi-agent scenarios, use Neo4j instead.

Kuzu (Remote API)

Use Kuzu with an HTTP API when you need remote access or want to run Kuzu as a service.

```
GRAPH_DATABASE_PROVIDER="kuzu-remote"
GRAPH_DATABASE_URL="http://localhost:8000"
GRAPH_DATABASE_USERNAME="<optional>"
GRAPH_DATABASE_PASSWORD="<optional>"
```

**Installation**: Requires a running Kuzu service exposing an HTTP API.

Neo4j

Neo4j is recommended for production environments and multi-user scenarios.

```
ENABLE_BACKEND_ACCESS_CONTROL="true"
GRAPH_DATABASE_PROVIDER="neo4j"
GRAPH_DATABASE_URL="bolt://localhost:7687"
GRAPH_DATABASE_NAME="neo4j"
GRAPH_DATABASE_USERNAME="neo4j"
GRAPH_DATABASE_PASSWORD="pleaseletmein"
```

**Installation**: Install Neo4j extras:

```
pip install "cognee[neo4j]"
```

**Docker Setup**: Start the bundled Neo4j service with APOC + GDS plugins:

```
docker compose --profile neo4j up -d
```

Neptune (Graph-only)

Use Amazon Neptune for cloud-based graph storage.

```
GRAPH_DATABASE_PROVIDER="neptune"
GRAPH_DATABASE_URL="neptune://<GRAPH_ID>"
# AWS credentials via environment or default SDK chain
```

**Installation**: Install Neptune extras:

```
pip install "cognee[neptune]"
```

**Note**: AWS credentials should be configured via environment variables or AWS SDK.

Neptune Analytics (Hybrid)

Use Amazon Neptune Analytics as a hybrid vector + graph backend.

```
GRAPH_DATABASE_PROVIDER="neptune_analytics"
GRAPH_DATABASE_URL="neptune-graph://<GRAPH_ID>"
# AWS credentials via environment or default SDK chain
```

**Installation**: Install Neptune extras:

```
pip install "cognee[neptune]"
```

**Note**: This is the same as the vector store configuration. Neptune Analytics serves both purposes.

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#advanced-options)

Advanced Options

Backend Access Control

Enable per-user dataset isolation for multi-tenant scenarios.

```
ENABLE_BACKEND_ACCESS_CONTROL="true"
```

This feature is available for Kuzu and other supported graph stores.

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#provider-comparison)

Provider Comparison

Graph Store Comparison

| Provider          | Setup           | Performance | Use Case              |
| ----------------- | --------------- | ----------- | --------------------- |
| Kuzu              | Zero setup      | Good        | Local development     |
| Kuzu-remote       | Server required | Good        | Remote access         |
| Neo4j             | Server required | Excellent   | Production            |
| Neptune           | AWS required    | Excellent   | Cloud solution        |
| Neptune Analytics | AWS required    | Excellent   | Hybrid cloud solution |

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#important-considerations)

Important Considerations

Data Location

- **Local providers** (Kuzu): Graph files are created automatically under `SYSTEM_ROOT_DIRECTORY`
- **Remote providers** (Neo4j, Neptune): Require running services or cloud setup
- **Path management**: Local graphs are managed automatically, no manual path configuration needed

Performance Notes

- **Kuzu**: Single-file storage with good local performance
- **Neo4j**: Excellent for production workloads with proper indexing
- **Neptune**: Cloud-scale performance with managed infrastructure
- **Hybrid solutions**: Combine graph and vector capabilities in one system

## 

[​

](https://docs.cognee.ai/setup-configuration/graph-stores#notes)

Notes

- **Backend Access Control**: When enabled, Kuzu supports per-user dataset isolation
- **Path Management**: Local Kuzu databases are created automatically under the system directory
- **Cloud Integration**: Neptune providers require AWS credentials and proper IAM permissions





Setup Configuration

# Permissions Setup

Copy page

Configure Cognee’s permission system and access control

Enable Cognee’s permission system for data isolation and access control. For detailed concepts, see [Cognee Permissions System](https://docs.cognee.ai/core-concepts/multi-user-mode/permissions-system/overview).

## 

[​

](https://docs.cognee.ai/setup-configuration/permissions#enable-permission-system)

Enable Permission System

Set the environment variable to enable access control:

```
ENABLE_BACKEND_ACCESS_CONTROL=true
REQUIRE_AUTHENTICATION=true
```

**Database Override**: Permission mode enforces Kùzu (graph) and LanceDB (vector). Custom providers are ignored.

## 

[​

](https://docs.cognee.ai/setup-configuration/permissions#database-setup)

Database Setup

Choose your relational database:

- **SQLite** — Local development (auto-creates files)
- **Postgres** — Production (requires manual setup)

See [Relational Databases](https://docs.cognee.ai/setup-configuration/relational-databases) for detailed configuration.

## 

[​

](https://docs.cognee.ai/setup-configuration/permissions#authentication)

Authentication

### 

[​

](https://docs.cognee.ai/setup-configuration/permissions#api-server)

API Server

Start the server with authentication:

```
uvicorn cognee.api.client:app --host 0.0.0.0 --port 8000
```

**Default credentials (development only):**

- Username: `default_user@example.com`
- Password: `default_password`

### 

[​

](https://docs.cognee.ai/setup-configuration/permissions#programmatic-access)

Programmatic Access

See [Permission Snippets](https://docs.cognee.ai/guides/permission-snippets) for complete programmatic examples.

## 

[​

](https://docs.cognee.ai/setup-configuration/permissions#data-organization)

Data Organization

Data is automatically organized by user and dataset. Each user gets isolated storage:

```
.cognee_system/databases/<user_uuid>/
├── <dataset_uuid>.pkl         # Kùzu graph database
└── <dataset_uuid>.lance.db/   # LanceDB vector database
```

## 

[​

](https://docs.cognee.ai/setup-configuration/permissions#troubleshooting)

Troubleshooting

**Permission Denied**: Verify user has required permission on the dataset.**Data Isolation**: Check per-user database files exist:

```
ls -la .cognee_system/databases/<user_uuid>/
```

**Database Conflicts**: Custom providers are ignored in permission mode.





# Search Basics

Copy page

Step-by-step guide to running your first Cognee search and understanding core parameters

A minimal guide to using `cognee.search()` to ask questions against your processed datasets. This guide shows the basic call and what each parameter does so you know which knob to turn.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/setup-configuration/llm-providers) configured for LLM-backed search types
- Run `cognee.cognify(...)` to build the graph before searching
- Keep at least one dataset with `read` permission for the user running the search

## 

[​

](https://docs.cognee.ai/guides/search-basics#code-in-action)

Code in Action

```
import asyncio
import cognee

async def main():
    # Make sure you've already run cognee.cognify(...) so the graph has content
    answers = await cognee.search(
        query_text="What are the main themes in my data?"
    )
    for answer in answers:
        print(answer)

asyncio.run(main())
```

`SearchType.GRAPH_COMPLETION` is the default, so you get an LLM-backed answer plus supporting context as soon as you have data in your graph.

## 

[​

](https://docs.cognee.ai/guides/search-basics#what-just-happened)

What Just Happened

The search call uses the default `SearchType.GRAPH_COMPLETION` mode to provide LLM-backed answers with supporting context from your knowledge graph. The results are returned as a list that you can iterate through and process as needed.

## 

[​

](https://docs.cognee.ai/guides/search-basics#parameters-reference)

Parameters Reference

Most examples below assume you are inside an async function. Import helpers when you need them:

```
from cognee import SearchType
from cognee.modules.engine.models.node_set import NodeSet
```

Core Parameters

- **`query_text`** (str, required): The question or phrase you want answered.
  
  ```
  answers = await cognee.search(query_text="Who owns the rollout plan?")
  ```

- **`query_type`** (SearchType, optional, default: `SearchType.GRAPH_COMPLETION`): Switch search modes without changing your code flow. See [Search Types](https://docs.cognee.ai/core-concepts/main-operations/search) for the complete list.
  
  ```
  await cognee.search(
      query_text="List coding guidelines",
      query_type=SearchType.CODING_RULES,
  )
  ```

- **`top_k`** (int, optional, default: 10): Cap how many ranked results you want back.
  
  ```
  await cognee.search(query_text="Summaries please", top_k=3)
  ```

Prompt & Generation Parameters

- **`system_prompt_path`** (str, optional, default: `"answer_simple_question.txt"`): Point to a prompt file packaged with your project.
  
  ```
  await cognee.search(
      query_text="Explain the roadmap in bullet points",
      system_prompt_path="prompts/bullets.txt",
  )
  ```

- **`system_prompt`** (Optional[str]): Inline override for experiments or dynamically generated prompts.
  
  ```
  await cognee.search(
      query_text="Give me a confident answer",
      system_prompt="Answer succinctly and state confidence at the end.",
  )
  ```

- **`only_context`** (bool, optional, default: False): Skip LLM generation and just fetch supporting context chunks.
  
  ```
  context = await cognee.search(
      query_text="What did we promise the client?",
      only_context=True,
  )
  ```

- **`use_combined_context`** (bool, optional, default: False): Collapse results into a single combined response when you query multiple datasets.
  
  ```
  combined = await cognee.search(
      query_text="Quarterly financial highlights",
      datasets=["finance_q1", "finance_q2"],
      use_combined_context=True,
  )
  ```

`use_combined_context` should only be set when `ENABLE_BACKEND_ACCESS_CONTROL` is turned on. When access control is disabled, this parameter has no meaningful effect on dataset scoping.

Node Sets & Filtering Parameters

These options filter the graph down to the node sets you care about. In most workflows you set **both**: keep `node_type=NodeSet` and pass one or more set names in `node_name`—the same labels you used when calling `cognee.add(..., node_set=[...])`.

- **`node_type`** (Optional[Type], optional, default: `NodeSet`): Controls which graph model to search. Leave this as `NodeSet` unless you’ve built a custom node model.

- **`node_name`** (Optional[List[str]]): Names of the node sets to include. Cognee treats each string as a logical bucket of memories.
  
  ```
  await cognee.search(
      query_text="What discounts did TechSupply offer?",
      node_type=NodeSet,
      node_name=["vendor_conversations"],
  )
  ```
  
  ```
  await cognee.search(
      query_text="Summarize procurement rules",
      node_type=NodeSet,
      node_name=["procurement_policies", "purchase_history"],
  )
  ```
  
  Interaction & History Parameters

- **`session_id`** (Optional[str]): Maintain conversation history across searches. When you use the same `session_id`, Cognee includes previous interactions in the LLM prompt, enabling contextual follow-up questions.
  
  ```
  await cognee.search(
      query_text="Where does Alice live?",
      session_id="conversation_1"
  )
  # Later, same session remembers previous context
  await cognee.search(
      query_text="What does she do for work?",
      session_id="conversation_1"  # "she" refers to Alice
  )
  ```
  
  See [Sessions Guide](https://docs.cognee.ai/guides/sessions) for complete examples.

- **`save_interaction`** (bool, optional, default: False): Persist the Q&A as a graph interaction for auditing or later review.
  
  ```
  await cognee.search(
      query_text="Draft the release note",
      save_interaction=True,
  )
  ```

- **`last_k`** (Optional[int], optional, default: 1): When using `SearchType.FEEDBACK`, choose how many recent interactions to update with your feedback.
  
  ```
  await cognee.search(
      query_text="Please improve the last answer",
      query_type=SearchType.FEEDBACK,
      last_k=3,
  )
  ```

Datasets & Users

- **`datasets`** (Optional[Union[list[str], str]]): Limit search to dataset names you already know.
  
  ```
  await cognee.search(
      query_text="Key risks",
      datasets=["risk_register", "exec_summary"],
  )
  ```

- **`dataset_ids`** (Optional[Union[list[UUID], UUID]]): Same as `datasets`, but with explicit UUIDs when names collide.
  
  ```
  from uuid import UUID
  await cognee.search(
      query_text="Customer feedback",
      dataset_ids=[UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")],
  )
  ```

- **`user`** (Optional[User]): Provide a user object when running multi-tenant flows or background jobs.
  
  ```
  from cognee.modules.users.methods import get_user
  user = await get_user(user_id)
  await cognee.search(query_text="Team OKRs", user=user)
  ```
  
  **When** `ENABLE_BACKEND_ACCESS_CONTROL=true`:
  
  - **Result shape**: Searches run only on datasets the user can access and return either:
    - **Per dataset**: list of `{dataset_name, dataset_id, search_result}`
    - **Combined**: single `CombinedSearchResult` with merged snippets (`use_combined_context=True`)
  - If no `user` is given, `get_default_user()` is used (created if missing); errors only if this user lacks dataset permissions.
  - If `datasets` is not set, all datasets readable by the user are searched; errors if none are accessible or if requested datasets are forbidden.
  
  `PermissionDeniedError` will be raised unless you search with the same user that added the data or grant access to the default user.
  
  **When** `ENABLE_BACKEND_ACCESS_CONTROL=false`
  
  - Dataset filters (`datasets`, `dataset_ids`) are ignored — everything is searched.
  - Results normally come back as a plain list (`["answer1", "answer2"]`).
  - Setting `use_combined_context=True` here just wraps the same results in a `CombinedSearchResult` without changing them.

## 

[​

](https://docs.cognee.ai/guides/search-basics#additional-examples)

Additional examples

Full python script that expands the previous example can be found underneath.

Expanded example

```
  import asyncio
  import cognee

  async def main():
      # Start clean (optional in your app)
      await cognee.prune.prune_data()
      await cognee.prune.prune_system(metadata=True)
      # Prepare knowledge base
      await cognee.add([
          "Alice moved to Paris in 2010. She works as a software engineer.",
          "Bob lives in New York. He is a data scientist.",
          "Alice and Bob met at a conference in 2015."
      ])

      await cognee.cognify()

      # Make sure you've already run cognee.cognify(...) so the graph has content
      answers = await cognee.search(
          query_text="What are the main themes in my data?"
      )
      for answer in answers:
          print(answer)

  asyncio.run(main())
```

Additional examples about Search Basics are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).







Essentials

# Deploy REST API Server

Copy page

Deploy Cognee as a REST API server using Docker or Python

Deploy Cognee as a REST API server to expose its functionality via HTTP endpoints.

## 

[​

](https://docs.cognee.ai/guides/deploy-rest-api-server#setup)

Setup

```
# Clone repository
git clone https://github.com/topoteretes/cognee.git
cd cognee

# Configure environment
cp .env.template .env
```

Edit `.env` with your preferred configuration. See [Setup Configuration](https://docs.cognee.ai/setup-configuration/overview) guides for all available options.

## 

[​

](https://docs.cognee.ai/guides/deploy-rest-api-server#deployment-methods)

Deployment Methods

- Docker

- Python (Local)

### 

[​

](https://docs.cognee.ai/guides/deploy-rest-api-server#start-server)

Start Server

```
# Start API server
docker compose up --build cognee

# Check status
docker compose ps
```

## 

[​

](https://docs.cognee.ai/guides/deploy-rest-api-server#access-api)

Access API

- **API:** [http://localhost:8000](http://localhost:8000/)
- **Documentation:** http://localhost:8000/docs

## 

[​

](https://docs.cognee.ai/guides/deploy-rest-api-server#authentication)

Authentication

If `REQUIRE_AUTHENTICATION=true` in your `.env` file:

1. **Register:** `POST /api/v1/auth/register`
2. **Login:** `POST /api/v1/auth/login`
3. **Use token:** Include `Authorization: Bearer <token>` header or use cookies

## 

[​

](https://docs.cognee.ai/guides/deploy-rest-api-server#api-examples)

API Examples

Authentication

**Register a user:**

```
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@example.com", "password": "strong_password"}'
```

**Login and get token:**

```
TOKEN="$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user1@example.com&password=strong_password' | jq -r .access_token)"
```

Dataset Management

**Create a dataset:**

```
curl -X POST http://localhost:8000/api/v1/datasets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "project_docs"}'
```

**List datasets:**

```
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/datasets
```

Data Operations

**Add data (upload file):**

```
curl -X POST http://localhost:8000/api/v1/add \
  -H "Authorization: Bearer $TOKEN" \
  -F "data=@/absolute/path/to/file.pdf" \
  -F "datasetName=project_docs"
```

**Build knowledge graph:**

```
curl -X POST http://localhost:8000/api/v1/cognify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"datasets": ["project_docs"]}'
```

**Search data:**

```
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "What are the main topics?", "datasets": ["project_docs"], "top_k": 10}'
```

Multi-tenant Operations

**Create tenant:**

```
curl -X POST "http://localhost:8000/api/v1/permissions/tenants?tenant_name=acme" \
  -H "Authorization: Bearer $TOKEN"
```

**Add user to tenant:**

```
curl -X POST "http://localhost:8000/api/v1/permissions/users/<user_id>/tenants?tenant_id=<tenant_id>" \
  -H "Authorization: Bearer $TOKEN"
```

**Create role:**

```
curl -X POST "http://localhost:8000/api/v1/permissions/roles?role_name=editor" \
  -H "Authorization: Bearer $TOKEN"
```

**Assign user to role:**

```
curl -X POST "http://localhost:8000/api/v1/permissions/users/<user_id>/roles?role_id=<role_id>" \
  -H "Authorization: Bearer $TOKEN"
```

**Grant dataset permissions:**

```
curl -X POST "http://localhost:8000/api/v1/permissions/datasets/<principal_id>?permission_name=read&dataset_ids=<ds_uuid_1>&dataset_ids=<ds_uuid_2>" \
  -H "Authorization: Bearer $TOKEN"
```

[

## API Reference

Explore all API endpoints

](https://docs.cognee.ai/api-reference/introduction)[

## Setup Configuration

Configure providers and databases

](https://docs.cognee.ai/setup-configuration/overview)[

## MCP Integration

Set up AI assistant integration

](https://docs.cognee.ai/cognee-mcp/mcp-overview)

Was this page helpful?

YesNo

[Previous](https://docs.cognee.ai/guides/sessions)[

Temporal CognifyStep-by-step guide to using temporal mode for time-aware queries

Next

](https://docs.cognee.ai/guides/time-awareness)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=cognee)





Essentials

# Temporal Cognify

Copy page

Step-by-step guide to using temporal mode for time-aware queries

A minimal guide to Cognee’s temporal mode. If you already know the regular add → cognify → search flow, this adds one switch at cognify time and one search type for time-aware questions.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have data that contains dates/times (years or full dates)

## 

[​

](https://docs.cognee.ai/guides/time-awareness#what-temporal-mode-does)

What Temporal Mode Does

- Builds events and timestamps from your text during cognify
- Lets you ask time-based questions like “before 1980”, “after 2010”, or “between 2000 and 2006”
- Uses `SearchType.TEMPORAL` to retrieve the most relevant events and answer with temporal context

## 

[​

](https://docs.cognee.ai/guides/time-awareness#step-1-add-data)

Step 1: Add Data

Add data with temporal information using the standard `add` function.

```
import cognee

text = """
In 1998 the project launched. In 2001 version 1.0 shipped. In 2004 the team merged
with another group. In 2010 support for v1 ended.
"""

await cognee.add(text, dataset_name="timeline_demo")
```

This simple example uses one string that gets treated as a single document. In practice, you can add multiple documents, files, or entire datasets - the temporal processing works the same way across all your data.

## 

[​

](https://docs.cognee.ai/guides/time-awareness#step-2-cognify-with-temporal-mode)

Step 2: Cognify with Temporal Mode

Set `temporal_cognify=True` to extract events/timestamps instead of the default entity-graph pipeline.

```
await cognee.cognify(datasets=["timeline_demo"], temporal_cognify=True)
```

Only datasets you pass (or all by default) are processed. Temporal mode runs an event/timestamp pipeline and stores temporal nodes in the graph.

This example uses a single dataset for simplicity. In practice, you can process multiple datasets simultaneously by passing a list of dataset names, or omit the `datasets` parameter to process all available datasets.

## 

[​

](https://docs.cognee.ai/guides/time-awareness#step-3-ask-time-aware-questions)

Step 3: Ask Time-aware Questions

Use `SearchType.TEMPORAL` and phrase your query with time hints.

```
from cognee.api.v1.search import SearchType

# Before / after queries
await cognee.search(
    query_type=SearchType.TEMPORAL, 
    query_text="What happened before 2000?", 
    top_k=10
)

await cognee.search(
    query_type=SearchType.TEMPORAL, 
    query_text="What happened after 2010?", 
    top_k=10
)

# Between queries
await cognee.search(
    query_type=SearchType.TEMPORAL, 
    query_text="Events between 2001 and 2004", 
    top_k=10
)

# Scoped descriptions
await cognee.search(
    query_type=SearchType.TEMPORAL, 
    query_text="Key project milestones between 1998 and 2010", 
    top_k=10
)
```

- If the query has clear dates, the retriever filters events by time and ranks them
- If no dates are detected, it falls back to event/entity graph retrieval and still answers
- Increase `top_k` to inspect more candidate events

## 

[​

](https://docs.cognee.ai/guides/time-awareness#optional-limit-to-specific-datasets)

Optional: Limit to Specific Datasets

```
await cognee.search(
    query_type=SearchType.TEMPORAL,
    query_text="What happened after 2004?",
    datasets=["timeline_demo"],
    top_k=10,
)
```

## 

[​

](https://docs.cognee.ai/guides/time-awareness#using-the-http-api)

Using the HTTP API

If your server is running, you can run temporal search via the API by setting `search_type` to `"TEMPORAL"`:

```
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  ${TOKEN:+-H "Authorization: Bearer $TOKEN"} \
  -d '{
        "search_type": "TEMPORAL",
        "query": "What happened between 2001 and 2004?",
        "top_k": 10
      }'
```

For now, enabling temporal processing at cognify time is easiest in Python with `temporal_cognify=True`.

## 

[​

](https://docs.cognee.ai/guides/time-awareness#additional-examples)

Additional examples

Additional examples about Temporal awareness are available at our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).





# Ontology Quickstart

Copy page

Step-by-step guide to using OWL ontologies to ground Cognee knowledge graphs

A minimal guide to using OWL ontologies to ground Cognee’s knowledge graphs. You’ll point Cognee at an ontology file during cognify and then ask ontology-aware questions.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Read [Ontologies](https://docs.cognee.ai/core-concepts/further-concepts/ontologies) to understand the concepts
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have an OWL ontology file (`.owl`) in RDF/XML format
- Have some text or files relevant to the ontology’s domain

## 

[​

](https://docs.cognee.ai/guides/ontology-support#what-ontology-support-does)

What Ontology Support Does

- Grounds entities and relations to your OWL ontology (classes, individuals, properties)
- Validates types via ontology domains/ranges and class hierarchy
- Improves graph completion answers for domain-specific queries

## 

[​

](https://docs.cognee.ai/guides/ontology-support#step-1-prepare-an-ontology-file)

Step 1: Prepare an Ontology File

Start from a simple OWL file. Minimal ingredients:

- Classes (e.g., `TechnologyCompany`, `Car`)
- Individuals (e.g., `Apple`, `Audi`)
- Object properties with domain/range (e.g., `produces` with `domain=CarManufacturer`, `range=Car`)

Example ontology files:

- `examples/python/ontology_input_example/basic_ontology.owl`
- `examples/python/ontology_input_example/enriched_medical_ontology_with_classes.owl`

Use any RDF/OWL editor (Protégé) to edit .owl files.

This example uses a simple ontology for demonstration. In practice, you can work with larger, more complex ontologies - the same approach works regardless of ontology size or complexity.

## 

[​

](https://docs.cognee.ai/guides/ontology-support#step-2-add-your-data)

Step 2: Add Your Data

Add either raw text or a directory. Keep it relevant to your ontology.

```
import cognee

texts = [
    "Audi produces the R8 and e-tron.",
    "Apple develops iPhone and MacBook."
]

await cognee.add(texts)
# or: await cognee.add("/path/to/folder/of/files")
```

This simple example uses a list of strings for demonstration. In practice, you can add multiple documents, files, or entire datasets - the ontology processing works the same way across all your data.

## 

[​

](https://docs.cognee.ai/guides/ontology-support#step-3-cognify-your-data-+-ontologies)

Step 3: Cognify Your Data + Ontologies

Create the `config` which contains the information about the ontology, to ground extracted entities/relations to the ontology. Then, simply pass the `config` to the `cognify` operation.

```
import os
from cognee.modules.ontology.ontology_config import Config
from cognee.modules.ontology.rdf_xml.RDFLibOntologyResolver import RDFLibOntologyResolver

ontology_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ontology_input_example/basic_ontology.owl"
)

# Create full config structure manually
config: Config = {
    "ontology_config": {
        "ontology_resolver": RDFLibOntologyResolver(ontology_file=ontology_path)
    }
}

await cognee.cognify(config=config)
```

If omitted, Cognee builds a graph without ontology grounding. With an ontology, Cognee aligns nodes to classes/individuals and enforces property domain/range.

## 

[​

](https://docs.cognee.ai/guides/ontology-support#step-4-ask-ontology-aware-questions)

Step 4: Ask Ontology-aware Questions

Use `SearchType.GRAPH_COMPLETION` to get answers that leverage ontology structure.

```
from cognee.api.v1.search import SearchType

result = await cognee.search(
    query_type=SearchType.GRAPH_COMPLETION,
    query_text="What cars and their types are produced by Audi?",
)
print(result)
```

Phrase questions using ontology terms (class names, individual names, property language like “produces”, “develops”). If results feel generic, check that the ontology contains the expected classes/individuals and that your data mentions them.

## 

[​

](https://docs.cognee.ai/guides/ontology-support#code-in-action)

Code in Action

- Small cars/tech demo: `examples/python/ontology_demo_example.py`
- Medical comparison demo: `examples/python/ontology_demo_example_2.py`



    Essentials

# Code Graph

Copy page

Step-by-step guide to building code-level graphs from repositories

A minimal guide to building a code-level graph from a repository and searching it. The pipeline parses your repo, extracts code entities and dependencies, and optionally processes non-code docs alongside.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have a local repository path (absolute or relative)

## 

[​

](https://docs.cognee.ai/guides/code-graph#what-code-graph-does)

What Code Graph Does

- Scans a repo for supported languages and builds code nodes/edges (files, symbols, imports, call/dependency links)
- Optional: includes non-code files (markdown, docs) as a standard knowledge graph
- Enables `SearchType.CODE` for code-aware queries

## 

[​

](https://docs.cognee.ai/guides/code-graph#code-in-action)

Code in Action

```
import asyncio
import cognee
from cognee import SearchType
from cognee.api.v1.cognify.code_graph_pipeline import run_code_graph_pipeline

async def main():
    repo_path = "/path/to/your/repo"  # folder root

    # Build the code graph (code only)
    async for _ in run_code_graph_pipeline(repo_path, include_docs=False):
        pass

    # Ask a code question
    results = await cognee.search(query_type=SearchType.CODE, query_text="Where is Foo used?")
    print(results)

asyncio.run(main())
```

This simple example uses a basic repository for demonstration. In practice, you can process large codebases with multiple languages and complex dependency structures.

## 

[​

](https://docs.cognee.ai/guides/code-graph#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/code-graph#step-1-build-the-code-graph)

Step 1: Build the Code Graph

```
async for _ in run_code_graph_pipeline(repo_path, include_docs=False):
    pass
```

This scans your repository for supported languages and builds code nodes/edges. The pipeline handles file parsing, symbol extraction, and dependency analysis automatically.

### 

[​

](https://docs.cognee.ai/guides/code-graph#step-2-search-your-code)

Step 2: Search Your Code

```
results = await cognee.search(query_type=SearchType.CODE, query_text="Where is Foo used?")
```

Use `SearchType.CODE` to ask code-aware questions about your repository. This searches through the extracted code structure, not just text content.

## 

[​

](https://docs.cognee.ai/guides/code-graph#include-documentation-optional)

Include Documentation (Optional)

Also process non-code files from the repo (slower, uses LLM for text):

```
async for _ in run_code_graph_pipeline(repo_path, include_docs=True):
    pass
```

This processes markdown files, documentation, and other text files alongside your code, creating a comprehensive knowledge graph.

## 

[​

](https://docs.cognee.ai/guides/code-graph#advanced-options)

Advanced Options

```
async for _ in run_code_graph_pipeline(
    repo_path,
    include_docs=False,
    excluded_paths=["**/node_modules/**", "**/dist/**"],
    supported_languages=["python", "typescript"],
):
    pass
```

- **`excluded_paths`**: List of paths (globs) to skip, e.g., tests, build folders
- **`supported_languages`**: Narrow to certain languages to speed up processing

## 

[​

](https://docs.cognee.ai/guides/code-graph#visualize-your-graph-optional)

Visualize Your Graph (Optional)

```
from cognee.api.v1.visualize.visualize import visualize_graph
await visualize_graph("./graph_code.html")
```

Generate an HTML visualization of your code graph to explore the structure and relationships.

## 

[​

](https://docs.cognee.ai/guides/code-graph#what-happens-under-the-hood)

What Happens Under the Hood

`run_code_graph_pipeline(...)` automatically handles:

- Repository scanning and file parsing
- Code entity extraction (functions, classes, imports, calls)
- Dependency analysis and relationship mapping
- Database initialization and setup
- Optional documentation processing with LLM

Once complete, your code graph is ready for search and analysis.







Essentials

# Graph Visualization

Copy page

Step-by-step guide to rendering interactive knowledge graphs

A minimal guide to rendering your current knowledge graph to an interactive HTML file with one call.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Have some data processed with `cognify` (knowledge graph exists)

## 

[​

](https://docs.cognee.ai/guides/graph-visualization#what-graph-visualization-shows)

What Graph Visualization Shows

- Nodes (entities, types, chunks, summaries) with color coding
- Edges with labels and weights; tooltips show extra edge properties
- Interactive features: drag nodes, zoom/pan, hover edges for details

## 

[​

](https://docs.cognee.ai/guides/graph-visualization#code-in-action)

Code in Action

```
import asyncio
import cognee
from cognee.api.v1.visualize.visualize import visualize_graph

async def main():
    await cognee.add(["Alice knows Bob.", "NLP is a subfield of CS."])
    await cognee.cognify()

    await visualize_graph("./graph_after_cognify.html")

asyncio.run(main())
```

This simple example uses basic text data for demonstration. In practice, you can visualize complex knowledge graphs with thousands of nodes and relationships.

## 

[​

](https://docs.cognee.ai/guides/graph-visualization#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/graph-visualization#step-1-create-your-knowledge-graph)

Step 1: Create Your Knowledge Graph

```
await cognee.add(["Alice knows Bob.", "NLP is a subfield of CS."])
await cognee.cognify()
```

First, create your knowledge graph using the standard add → cognify workflow. The visualization works on existing graphs.

### 

[​

](https://docs.cognee.ai/guides/graph-visualization#step-2-generate-visualization)

Step 2: Generate Visualization

```
await visualize_graph("./graph_after_cognify.html")
```

This creates an interactive HTML file with your knowledge graph. You can specify a custom path or use the default location.

## 

[​

](https://docs.cognee.ai/guides/graph-visualization#quick-options)

Quick Options

### 

[​

](https://docs.cognee.ai/guides/graph-visualization#default-location)

Default Location

```
from cognee.api.v1.visualize.visualize import visualize_graph

# Writes HTML to your home directory by default
await visualize_graph()
```

### 

[​

](https://docs.cognee.ai/guides/graph-visualization#custom-path)

Custom Path

```
from cognee.api.v1.visualize.visualize import visualize_graph

# Writes to the provided file path (created/overwritten)
await visualize_graph("./my_graph.html")
```

## 

[​

](https://docs.cognee.ai/guides/graph-visualization#tips)

Tips

- **Large graphs**: Rendering a very big graph can be slow. Consider building subsets (e.g., smaller datasets) before visualizing
- **Edge weights**: If present, control line thickness; multiple weights are summarized and shown in tooltips
- **Static HTML**: Files are static HTML; you can open them in any modern browser or share them as artifacts

## 

[​

](https://docs.cognee.ai/guides/graph-visualization#additional-examples)

Additional examples

Additional examples about Graph visualization are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).





ssentials

# Low-Level LLM

Copy page

Step-by-step guide to using acreate_structured_output for direct LLM interaction

A minimal guide to the one function you can call directly to get Pydantic-validated structured output from an LLM.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have some text to process

## 

[​

](https://docs.cognee.ai/guides/low-level-llm#what-it-is)

What It Is

- Single entrypoint: `LLMGateway.acreate_structured_output(text, system_prompt, response_model)`
- Returns an instance of your Pydantic `response_model` filled by the LLM
- Backend-agnostic: uses BAML or LiteLLM+Instructor under the hood based on config — your code doesn’t change

This function is used by default during cognify via the extractor. The backend switch lives in `cognee/infrastructure/llm/LLMGateway.py`.

## 

[​

](https://docs.cognee.ai/guides/low-level-llm#code-in-action)

Code in Action

```
import asyncio

from pydantic import BaseModel
from typing import List
from cognee.infrastructure.llm.LLMGateway import LLMGateway

class MiniEntity(BaseModel):
    name: str
    type: str

class MiniGraph(BaseModel):
    nodes: List[MiniEntity]

async def main():

    system_prompt = (
        "Extract entities as nodes with name and type. "
        "Use concise, literal values present in the text."
    )

    text = "Apple develops iPhone; Audi produces the R8."

    result = await LLMGateway.acreate_structured_output(text, system_prompt, MiniGraph)
    print(result)
    # MiniGraph(nodes=[MiniEntity(name='Apple', type='Organization'), ...])

if __name__ == "__main__":
    asyncio.run(main())
```

This simple example uses a basic schema for demonstration. In practice, you can define complex Pydantic models with nested structures, validation rules, and custom types.

## 

[​

](https://docs.cognee.ai/guides/low-level-llm#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/low-level-llm#step-1-define-your-schema)

Step 1: Define Your Schema

```
class MiniEntity(BaseModel):
    name: str
    type: str

class MiniGraph(BaseModel):
    nodes: List[MiniEntity]
```

Create Pydantic models that define the structure you want the LLM to return. The LLM will fill these models with data extracted from your text.

### 

[​

](https://docs.cognee.ai/guides/low-level-llm#step-2-write-a-system-prompt)

Step 2: Write a System Prompt

```
system_prompt = (
    "Extract entities as nodes with name and type. "
    "Use concise, literal values present in the text."
)
```

Write a clear prompt that tells the LLM what to extract and how to structure it. Short, explicit prompts work best.

### 

[​

](https://docs.cognee.ai/guides/low-level-llm#step-3-call-the-llm)

Step 3: Call the LLM

```
result = await LLMGateway.acreate_structured_output(text, system_prompt, MiniGraph)
```

This calls the LLM with your text and prompt, returning a Pydantic model instance with the extracted data.

A sync variant exists: `LLMGateway.create_structured_output(...)`.

## 

[​

](https://docs.cognee.ai/guides/low-level-llm#custom-tasks)

Custom Tasks

This function is often used when creating custom tasks for processing data with structured output. You’ll see it in action when we cover custom task creation in a future guide.

## 

[​

](https://docs.cognee.ai/guides/low-level-llm#backend-doesn%E2%80%99t-matter)

Backend Doesn’t Matter

The config decides the engine:

- `STRUCTURED_OUTPUT_FRAMEWORK=instructor` → LiteLLM + Instructor
- `STRUCTURED_OUTPUT_FRAMEWORK=baml` → BAML client/registry

Both paths return the same Pydantic model instance to your code.





Essentials

# Memify Quickstart

Copy page

Step-by-step guide to enriching existing knowledge graphs with derived facts

A minimal guide to running a small enrichment pass over your existing knowledge graph to add useful derived facts (e.g., coding rules) without re-ingesting data.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have an existing knowledge graph (add → cognify completed)

## 

[​

](https://docs.cognee.ai/guides/memify-quickstart#what-memify-does)

What Memify Does

- Pulls a subgraph (or whole graph) into a mini-pipeline
- Applies enrichment tasks to create new nodes/edges from existing context
- Defaults: extracts relevant chunks and adds coding rule associations

## 

[​

](https://docs.cognee.ai/guides/memify-quickstart#code-in-action)

Code in Action

```
import asyncio
import cognee
from cognee import SearchType

async def main():
    # 1) Add two short chats and build a graph
    await cognee.add([
        "We follow PEP8. Add type hints and docstrings.",
        "Releases should not be on Friday. Susan must review PRs.",
    ], dataset_name="rules_demo")
    await cognee.cognify(datasets=["rules_demo"])  # builds graph

    # 2) Enrich the graph (uses default memify tasks)
    await cognee.memify(dataset="rules_demo")

    # 3) Query the new coding rules
    rules = await cognee.search(
        query_type=SearchType.CODING_RULES,
        query_text="List coding rules",
        node_name=["coding_agent_rules"],
    )
    print("Rules:", rules)

asyncio.run(main())
```

This simple example uses basic text data for demonstration. In practice, you can enrich large knowledge graphs with complex derived facts and associations.

## 

[​

](https://docs.cognee.ai/guides/memify-quickstart#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/memify-quickstart#step-1-build-your-knowledge-graph)

Step 1: Build Your Knowledge Graph

```
await cognee.add([
    "We follow PEP8. Add type hints and docstrings.",
    "Releases should not be on Friday. Susan must review PRs.",
], dataset_name="rules_demo")
await cognee.cognify(datasets=["rules_demo"])
```

First, create your knowledge graph using the standard add → cognify workflow. Memify works on existing graphs, so you need this foundation first.

### 

[​

](https://docs.cognee.ai/guides/memify-quickstart#step-2-enrich-with-memify)

Step 2: Enrich with Memify

```
await cognee.memify(dataset="rules_demo")
```

This runs the default memify tasks on your existing graph. No data parameter means it processes the existing graph, optionally filtering with `node_name` and `node_type`.

### 

[​

](https://docs.cognee.ai/guides/memify-quickstart#step-3-query-enriched-data)

Step 3: Query Enriched Data

```
rules = await cognee.search(
    query_type=SearchType.CODING_RULES,
    query_text="List coding rules",
    node_name=["coding_agent_rules"],
)
```

Search for the newly created derived facts using specialized search types like `SearchType.CODING_RULES`.

## 

[​

](https://docs.cognee.ai/guides/memify-quickstart#customizing-tasks-optional)

Customizing Tasks (Optional)

```
from cognee.modules.pipelines.tasks.task import Task
from cognee.tasks.memify.extract_subgraph_chunks import extract_subgraph_chunks
from cognee.tasks.codingagents.coding_rule_associations import add_rule_associations

await cognee.memify(
    extraction_tasks=[Task(extract_subgraph_chunks)],
    enrichment_tasks=[Task(add_rule_associations, rules_nodeset_name="coding_agent_rules")],
    dataset="rules_demo",
)
```

You can customize the memify pipeline by specifying your own extraction and enrichment tasks.

## 

[​

](https://docs.cognee.ai/guides/memify-quickstart#what-happens-under-the-hood)

What Happens Under the Hood

The default memify tasks are equivalent to:

- **Extraction**: `Task(extract_subgraph_chunks)` - pulls relevant chunks from your graph
- **Enrichment**: `Task(add_rule_associations, rules_nodeset_name="coding_agent_rules")` - creates new associations and rules

This creates derived knowledge without re-processing your original data.

## 

[​

](https://docs.cognee.ai/guides/memify-quickstart#additional-examples)

Additional examples

Additional examples about Memify are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).





Essentials

# Distributed Execution

Copy page

Step-by-step guide to running Cognee pipelines across Modal containers

A minimal guide to running Cognee pipelines across [Modal](https://modal.com/docs) containers with a one-line toggle. Good fit for large batches or slow tasks.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have a Modal account and tokens configured locally (`modal setup`)
- Create a Modal Secret named `distributed_cognee` with your environment variables

## 

[​

](https://docs.cognee.ai/guides/distributed-execution#what-distributed-execution-does)

What Distributed Execution Does

- Distributes per-item task execution to Modal functions
- Keeps your code unchanged; you can keep using `add` → `cognify` → `search` or custom pipelines
- Scales processing across multiple containers for large datasets

## 

[​

](https://docs.cognee.ai/guides/distributed-execution#what-is-modal)

What is Modal?

[Modal](https://modal.com/docs) is a serverless cloud platform that provides compute-intensive applications without thinking about infrastructure. It’s perfect for running generative AI models, large-scale batch workflows, and job queues at scale.When you enable distributed execution, Cognee automatically uses Modal to run your processing tasks across multiple containers, making it much faster for large datasets.

## 

[​

](https://docs.cognee.ai/guides/distributed-execution#prerequisites)

Prerequisites

Install extras with Modal support and configure your environment:

```
# Install with distributed support
pip install cognee[distributed]

# Configure Modal (creates account if needed)
modal setup

# Create Modal Secret with your environment variables
modal secret create distributed_cognee
```

Add your environment variables to the Modal Secret (e.g., `LLM_API_KEY`, DB configs, S3 creds if used).

## 

[​

](https://docs.cognee.ai/guides/distributed-execution#code-in-action)

Code in Action

```
import asyncio
import cognee
from cognee import SearchType

async def main():
    # COGNEE_DISTRIBUTED=true is picked up implicitly
    # 1) Add data (text, files, or S3 URIs)
    await cognee.add([
        "Alice knows Bob. Bob works at ACME.",
        "NLP is a subfield of computer science.",
    ], dataset_name="dist_demo")

    # 2) Build the knowledge graph (runs distributed)
    await cognee.cognify(datasets=["dist_demo"]) 

    # 3) Query
    answers = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="Who does Alice know?",
        top_k=5,
    )
    print(answers)

asyncio.run(main())
```

This simple example uses basic text data for demonstration. In practice, you can process large datasets, files, or S3 URIs - the distributed execution scales automatically across Modal containers.

## 

[​

](https://docs.cognee.ai/guides/distributed-execution#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/distributed-execution#step-1-enable-distribution)

Step 1: Enable Distribution

```
export COGNEE_DISTRIBUTED=true
python your_script.py
```

Set the environment variable and run your code as usual. Internally, pipelines switch from `run_tasks` to `run_tasks_distributed` (Modal) via this toggle.

### 

[​

](https://docs.cognee.ai/guides/distributed-execution#step-2-add-your-data)

Step 2: Add Your Data

```
await cognee.add([
    "Alice knows Bob. Bob works at ACME.",
    "NLP is a subfield of computer science.",
], dataset_name="dist_demo")
```

Add your data using the standard `add` function. The same approach works with files, S3 URIs, or large datasets.

### 

[​

](https://docs.cognee.ai/guides/distributed-execution#step-3-process-distributed)

Step 3: Process Distributed

```
await cognee.cognify(datasets=["dist_demo"])
```

The `cognify` operation automatically runs distributed across Modal containers when `COGNEE_DISTRIBUTED=true` is set.

### 

[​

](https://docs.cognee.ai/guides/distributed-execution#step-4-search-your-data)

Step 4: Search Your Data

```
answers = await cognee.search(
    query_type=SearchType.GRAPH_COMPLETION,
    query_text="Who does Alice know?",
    top_k=5,
)
```

Search your processed data using the standard search methods. The results are the same whether processed locally or distributed.

## 

[​

](https://docs.cognee.ai/guides/distributed-execution#what-happens-under-the-hood)

What Happens Under the Hood

When `COGNEE_DISTRIBUTED=true`:

- Tasks are distributed to Modal functions automatically
- Each task runs in its own container
- Results are collected and merged back
- Database schemas are created on first run
- Costs are tracked in your Modal workspace

Start small and confirm costs in your Modal workspace. For non-pipeline first calls that write to DBs, call `await setup()` once.



Customizing Cognee

# Custom Data Models

Copy page

Step-by-step guide to creating custom data models and using add_data_points

A minimal guide to creating custom data models and inserting them directly into the knowledge graph using `add_data_points`.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have some structured data you want to model

## 

[​

](https://docs.cognee.ai/guides/custom-data-models#what-custom-data-models-do)

What Custom Data Models Do

- Define your own Pydantic models that inherit from `DataPoint`
- Insert structured data directly into the knowledge graph without `cognify`
- Create relationships between data points programmatically
- Control exactly what gets indexed and how

## 

[​

](https://docs.cognee.ai/guides/custom-data-models#code-in-action)

Code in Action

```
import asyncio
from typing import Any
from pydantic import SkipValidation

import cognee
from cognee.infrastructure.engine import DataPoint
from cognee.infrastructure.engine.models.Edge import Edge
from cognee.tasks.storage import add_data_points

class Person(DataPoint):
    name: str
    # Keep it simple for forward refs / mixed values
    knows: SkipValidation[Any] = None  # single Person or list[Person]
    # Recommended: specify which fields to index for search
    metadata: dict = {"index_fields": ["name"]}

async def main():
    # Start clean (optional in your app)
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    alice = Person(name="Alice")
    bob = Person(name="Bob")
    charlie = Person(name="Charlie")

    # Create relationships - field name becomes edge label
    alice.knows = bob
    # You can also do lists: alice.knows = [bob, charlie]

    # Optional: add weights and custom relationship types
    bob.knows = (Edge(weight=0.9, relationship_type="friend_of"), charlie)

    await add_data_points([alice, bob, charlie])

asyncio.run(main())
```

This example shows the complete workflow with metadata for indexing and optional edge weights. In practice, you can create complex nested models with multiple relationships and sophisticated data structures.

## 

[​

](https://docs.cognee.ai/guides/custom-data-models#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/custom-data-models#step-1-define-your-data-model)

Step 1: Define Your Data Model

```
class Person(DataPoint):
    name: str
    knows: SkipValidation[Any] = None
    # Recommended: specify which fields to index for search
    metadata: dict = {"index_fields": ["name"]}
```

Create a Pydantic model that inherits from `DataPoint`. Use `SkipValidation[Any]` for fields that will hold other DataPoints to avoid forward reference issues. **Metadata is recommended** - it tells Cognee which fields to embed and store in the vector database for search.

### 

[​

](https://docs.cognee.ai/guides/custom-data-models#step-2-create-data-instances)

Step 2: Create Data Instances

```
alice = Person(name="Alice")
bob = Person(name="Bob")
charlie = Person(name="Charlie")
```

Instantiate your models with the data you want to store. Each instance becomes a node in the knowledge graph.

### 

[​

](https://docs.cognee.ai/guides/custom-data-models#step-3-create-relationships)

Step 3: Create Relationships

```
alice.knows = bob
# Optional: add weights and custom relationship types
bob.knows = (Edge(weight=0.9, relationship_type="friend_of"), charlie)
```

Assign DataPoint instances to fields to create edges. The field name becomes the relationship label by default. **Weights are optional** - you can use `Edge` to add weights, custom relationship types, or other metadata to your relationships.

### 

[​

](https://docs.cognee.ai/guides/custom-data-models#step-4-insert-into-graph)

Step 4: Insert into Graph

```
await add_data_points([alice, bob, charlie])
```

This converts your DataPoint instances into nodes and edges in the knowledge graph, automatically handling the graph structure and indexing. The `name` field gets embedded and stored in the vector database for search.

## 

[​

](https://docs.cognee.ai/guides/custom-data-models#use-in-custom-tasks-and-pipelines)

Use in Custom Tasks and Pipelines

This approach is particularly useful when creating custom tasks and pipelines where you need to:

- Insert structured data programmatically
- Define specific relationships between known entities
- Control exactly what gets indexed and how
- Integrate with external data sources or APIs

You can combine this with `cognify` to extract knowledge from unstructured text, then add your own structured data on top.

## 

[​

](https://docs.cognee.ai/guides/custom-data-models#additional-examples)

Additional examples

Additional examples about Custom data models are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).





Customizing Cognee

# Custom Tasks and Pipelines

Copy page

Step-by-step guide to creating custom tasks and pipelines

A minimal guide to creating custom tasks and pipelines. You’ll build a two-step pipeline: the LLM extracts People directly, then you insert them into the knowledge graph.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have some text data to process

## 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#what-custom-tasks-and-pipelines-do)

What Custom Tasks and Pipelines Do

- Define custom processing steps using `Task` objects
- Chain multiple operations together in a pipeline
- Use LLMs to extract structured data from text
- Insert structured data directly into the knowledge graph
- Control the entire data processing workflow

## 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#code-in-action)

Code in Action

```
import asyncio
from typing import Any, Dict, List
from pydantic import BaseModel, SkipValidation

import cognee
from cognee.modules.engine.operations.setup import setup
from cognee.infrastructure.llm.LLMGateway import LLMGateway
from cognee.infrastructure.engine import DataPoint
from cognee.tasks.storage import add_data_points
from cognee.modules.pipelines import Task, run_pipeline

class Person(DataPoint):
    name: str
    # Optional relationships (we'll let the LLM populate this)
    knows: List["Person"] = []
    # Make names searchable in the vector store
    metadata: Dict[str, Any] = {"index_fields": ["name"]}

class People(BaseModel):
    persons: List[Person]

async def extract_people(text: str) -> List[Person]:
    system_prompt = (
        "Extract people mentioned in the text. "
        "Return as `persons: Person[]` with each Person having `name` and optional `knows` relations. "
        "If the text says someone knows someone set `knows` accordingly. "
        "Only include facts explicitly stated."
    )
    people = await LLMGateway.acreate_structured_output(text, system_prompt, People)
    return people.persons

async def main():
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    await setup()

    text = "Alice knows Bob."

    tasks = [
        Task(extract_people),  # input: text -> output: list[Person]
        Task(add_data_points)  # input: list[Person] -> output: list[Person]
    ]

    async for _ in run_pipeline(tasks=tasks, data=text, datasets=["people_demo"]):
        pass



if __name__ == "__main__":
    asyncio.run(main())
```

This simple example uses a two-step pipeline for demonstration. In practice, you can create complex pipelines with multiple custom tasks, data transformations, and processing steps.

## 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#step-1-define-your-data-models)

Step 1: Define Your Data Models

```
class Person(DataPoint):
    name: str
    knows: SkipValidation[Any] = None
    metadata: Dict[str, Any] = {"index_fields": ["name"]}

class People(BaseModel):
    persons: List[Person]
```

Create Pydantic models for your data. `Person` inherits from `DataPoint` for graph insertion, while `People` is a simple container for the LLM output. **Metadata is recommended** to make fields searchable in the vector database.

### 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#step-2-create-your-custom-task)

Step 2: Create Your Custom Task

```
async def extract_people(text: str) -> List[Person]:
    system_prompt = (
        "Extract people mentioned in the text. "
        "Return as `persons: Person[]` with each Person having `name` and optional `knows` relations. "
        "If the text says someone knows someone set `knows` accordingly. "
        "Only include facts explicitly stated."
    )
    people = await LLMGateway.acreate_structured_output(text, system_prompt, People)
    return people.persons
```

This task uses the LLM to extract structured data from text. The LLM fills `People` objects with `Person` instances, including relationships via the `knows` field.

`acreate_structured_output` is backend-agnostic (BAML or LiteLLM+Instructor). Configure via `STRUCTURED_OUTPUT_FRAMEWORK` in `.env`.

### 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#step-3-build-your-pipeline)

Step 3: Build Your Pipeline

```
tasks = [
    Task(extract_people),  # input: text -> output: list[Person]
    Task(add_data_points)  # input: list[Person] -> output: list[Person]
]

async for _ in run_pipeline(tasks=tasks, data=text, datasets=["people_demo"]):
    pass
```

Chain your tasks together in a pipeline. The first task extracts people from text, the second inserts them into the knowledge graph. `add_data_points` automatically creates nodes and edges from the `knows` relationships.Under the hood, `run_pipeline(...)` automatically initializes databases and checks LLM/embeddings configuration, so you don’t need to worry about setup. Once the pipeline completes, your Cognee memory with graph and embeddings is created and ready for interaction.You can now search your data using the standard search methods:

```
from cognee.api.v1.search import SearchType

# Search the processed data
results = await cognee.search(
    query_type=SearchType.GRAPH_COMPLETION,
    query_text="Who does Alice know?",
    datasets=["people_demo"]
)
print(results)
```

## 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#use-cases)

Use Cases

This approach is particularly useful when you need to:

- Extract structured data from unstructured text
- Process data through multiple custom steps
- Control the entire data processing workflow
- Combine LLM extraction with programmatic data insertion
- Build complex data processing pipelines

## 

[​

](https://docs.cognee.ai/guides/custom-tasks-pipelines#additional-examples)

Additional examples

Additional examples about Custom tasks and pipelines are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).







Customizing Cognee

# Custom Prompts

Copy page

Step-by-step guide to using custom prompts to control graph extraction

A minimal guide to shaping graph extraction with a custom LLM prompt. You’ll pass your prompt via `custom_prompt` to `cognee.cognify()` to control entity types, relationship labels, and extraction rules.**Before you start:**

- Complete [Quickstart](https://docs.cognee.ai/guides/getting-started/quickstart) to understand basic operations
- Ensure you have [LLM Providers](https://docs.cognee.ai/guides/setup-configuration/llm-providers) configured
- Have some text or files to process

## 

[​

](https://docs.cognee.ai/guides/custom-prompts#code-in-action)

Code in Action

```
import asyncio
import cognee
from cognee.api.v1.search import SearchType

custom_prompt = """
Extract only people and cities as entities.
Connect people to cities with the relationship "lives_in".
Ignore all other entities.
"""

async def main():
    await cognee.add([
        "Alice moved to Paris in 2010, while Bob has always lived in New York.",
        "Andreas was born in Venice, but later settled in Lisbon.",
        "Diana and Tom were born and raised in Helsingy. Diana currently resides in Berlin, while Tom never moved."
    ])
    await cognee.cognify(custom_prompt=custom_prompt)

    res = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="Where does Alice live?",
    )
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
```

This simple example uses a few strings for demonstration. In practice, you can add multiple documents, files, or entire datasets - the custom prompt processing works the same way across all your data.

## 

[​

](https://docs.cognee.ai/guides/custom-prompts#what-just-happened)

What Just Happened

### 

[​

](https://docs.cognee.ai/guides/custom-prompts#step-1-add-your-data)

Step 1: Add Your Data

```
await cognee.add([
    "Alice moved to Paris in 2010, while Bob has always lived in New York.",
    "Andreas was born in Venice, but later settled in Lisbon.",
    "Diana and Tom were born and raised in Helsingy. Diana currently resides in Berlin, while Tom never moved."
])
```

This adds text data to Cognee using the standard `add` function. The same approach works with multiple documents, files, or entire datasets.

### 

[​

](https://docs.cognee.ai/guides/custom-prompts#step-2-write-a-custom-prompt)

Step 2: Write a Custom Prompt

```
custom_prompt = """
Extract only people and cities as entities.
Connect people to cities with the relationship "lives_in".
Ignore all other entities.
"""
```

The custom prompt overrides the default system prompt used during entity/relationship extraction. It constrains node types, enforces relationship naming, and reduces noise.

`custom_prompt` is ignored when `temporal_cognify=True`.

### 

[​

](https://docs.cognee.ai/guides/custom-prompts#step-3-cognify-with-your-custom-prompt)

Step 3: Cognify with Your Custom Prompt

```
await cognee.cognify(custom_prompt=custom_prompt)
```

This processes your data using the custom prompt to control extraction behavior. You can also scope to specific datasets by passing the `datasets` parameter.

### 

[​

](https://docs.cognee.ai/guides/custom-prompts#step-4-ask-questions)

Step 4: Ask Questions

```
res = await cognee.search(
    query_type=SearchType.GRAPH_COMPLETION,
    query_text="Where does Alice live?",
)
```

Use `SearchType.GRAPH_COMPLETION` to get answers that leverage your custom extraction rules.

## 

[​

](https://docs.cognee.ai/guides/custom-prompts#additional-examples)

Additional examples

Additional examples about Custom prompts are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).







Use Cases

# Vertical AI Agents

Copy page

The future of AI is autonomous agents that execute complex, multi-step tasks in specialized domains. But agents without memory are agents without context. They can’t learn from past interactions, can’t understand organizational nuances, and can’t improve over time.Cognee provides the memory layer that makes agentic AI actually work.

## 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#the-problem-agents-that-forget)

The Problem: Agents That Forget

Consider an AI agent designed to automate legal contract review. Without persistent memory, every document is a blank slate:

- The agent doesn’t remember that your company uses specific non-standard clauses
- It can’t recall that the counterparty had issues with similar terms last quarter
- It has no context about your organization’s risk tolerance or negotiation patterns

## 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#why-memory-matters-for-agents-and-what-cognee-brings)

Why Memory Matters for Agents and What Cognee Brings

Agentic AI systems need three capabilities that standard RAG cannot provide:

### 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#1-domain-understanding)

1. Domain Understanding

The agent must understand how your enterprise works instead of only generic industry knowledge, in terms of your specific organizational structure, terminology, and processes.

### 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#2-personalization)

2. Personalization

Each user, client, or session can have tailored context. The agent adapts its responses based on individual preferences, history, and past interactions stored in memory.

### 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#3-dynamically-evolving-memory)

3. Dynamically Evolving Memory

As the agent operates, it should learn and improve. Patterns from successful task completions should inform future actions.Our memory layer provides:**Structured Context for Reasoning** Rather than raw text chunks, agents receive graph-structured knowledge that captures relationships, hierarchies, and domain logic.**Continuous Learning** Through `memify()`, feedback mechanism and many more advanced features, agents consolidate experiences into persistent memory, improving task execution over time.**Advanced Retrieval** Multiple search types—graph completion, semantic chunks, summaries—let agents retrieve exactly the context they need for each decision.

### 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#example-contract-review-agent-with-memory)

Example: Contract Review Agent with Memory

Define tools that give your agent persistent memory:

```
import cognee
from cognee.api.v1.search import SearchType

# Tool 1: Remember information
async def remember(text: str):
    """Store information in long-term memory."""
    await cognee.add(text)
    await cognee.cognify()
    return "Saved to memory"

# Tool 2: Recall information  
async def recall(query: str) -> str:
    """Search memory for relevant context."""
    results = await cognee.search(
        query_text=query,
        search_type=SearchType.GRAPH_COMPLETION
    )
    return results
```

Wire them into your agent:

```
tools = [remember, recall]

agent = Agent(
    model="gpt-4o",
    system_prompt="You are a contract analyst. Use remember() to store important details and recall() to retrieve past context.",
    tools=tools
)
```

Now the agent has memory:

```
# Session 1: Learn client preferences
agent.run("Remember: Acme Corp requires 30-day payment terms and California arbitration.")

# Session 2: Use memory for analysis
agent.run("Review this contract for Acme Corp: 60-day terms, New York jurisdiction.")
# Agent calls recall() → flags mismatches with stored preferences
```

## 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#integration-with-agentic-frameworks)

Integration with Agentic Frameworks

Cognee integrates with the frameworks you’re already using:

- LangGraph, CrewAI, LlamaIndex, Agent Development Kit, etc.
- **Custom implementations**: Direct SDK integration with any agent framework

## 

[​

](https://docs.cognee.ai/examples/vertical-ai-agents#next-steps)

Next Steps

Learn more about [Core Concepts](https://docs.cognee.ai/core-concepts/overview) or review [Integrations](https://docs.cognee.ai/integrations) for available options. If we don’t have your favorite agent framework yet, let us know by [opening an issue on GitHub](https://github.com/topoteretes/cognee/issues).





# 

Data Silos

Copy page

## 

[​

](https://docs.cognee.ai/examples/data-silos#enterprise-data-unification)

Enterprise Data Unification

Every enterprise has the same problem: valuable data locked in silos. Your CRM doesn’t talk to your ERP. Your knowledge base doesn’t connect to your support tickets. Your strategic documents live in SharePoint while operational data lives in Snowflake.Cognee creates a unified memory layer that connects these silos without replacing them.

## 

[​

](https://docs.cognee.ai/examples/data-silos#the-siloed-data-problem)

The Siloed Data Problem

When someone asks “What’s the full context on the Acme Corp relationship?”, the answer requires piecing together:

- CRM opportunity and contact data
- Support ticket history and resolution patterns
- Contract terms and renewal dates
- Invoice and payment history
- Relevant Slack conversations and email threads

No single system has the complete picture. Neither does traditional RAG.

## 

[​

](https://docs.cognee.ai/examples/data-silos#why-standard-rag-fails-here)

Why Standard RAG Fails Here

Vector search treats each chunk independently. It might find a support ticket mentioning Acme Corp and a contract with their name, but it doesn’t understand that:

- The support ticket was about a feature that the contract specifically excludes
- The escalation pattern matches a trend you’re seeing with other enterprise customers
- The contract renewal is approaching and the recent ticket volume is a risk signal

Relationships matter as much as content. Cognee captures both.

## 

[​

](https://docs.cognee.ai/examples/data-silos#implementation-connect-cognify-query)

Implementation: Connect, Cognify, Query

The Cognee Memory Layer sits on top of your existing data infrastructure:

### 

[​

](https://docs.cognee.ai/examples/data-silos#step-1-connect-your-sources)

Step 1: Connect Your Sources

Cognee supports 30+ data sources out of the box:

```
import cognee

# Connect structured data
await migrate_relational_database(graph, schema=schema)

# Connect unstructured documents
await cognee.add("s3://bucket/product-docs/")
await cognee.add("www.your-website.com")

# Connect semi-structured data
await cognee.add("path-to-your-folders")
...
```

### 

[​

](https://docs.cognee.ai/examples/data-silos#step-2-cognify)

Step 2: Cognify

Build the knowledge graph that connects entities across sources:

```
# Process all sources into a unified memory layer
await cognee.cognify()
```

Cognee automatically:

- Extracts entities (customers, products, people, concepts)
- Identifies relationships between entities
- Creates semantic embeddings for content
- Resolves entity references across sources (e.g., “Acme Corp” = “Acme Corporation” = “ACME”)

### 

[​

](https://docs.cognee.ai/examples/data-silos#step-3-query-with-context)

Step 3: Query with Context

Now queries return connected knowledge, not isolated chunks:

```
results = await cognee.search(
    query_text="Full context on Acme Corp",
    search_type=SearchType.GRAPH_COMPLETION
)
```

Ready to unify your data silos? [Start with the open-source SDK](https://github.com/topoteretes/cognee) or [talk to our team](https://calendly.com/vasilije-topoteretes/) about enterprise deployment.





Tutorials

# Cognee Walkthrough

Copy page

From Data to Interactive Memory: End-to-end tutorial with nodesets, ontologies, memify, graph visualization, and feedback system using a coding assistant example

Cognee gives you the tools to **build smarter AI agents** with context-aware memory.Use it to create a **queryable knowledge graph** powered by embeddings from your data. When retrieving data, your agent can reach up to **92.5% accuracy**.

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#what-you%E2%80%99ll-learn)

What You’ll Learn

In this tutorial, you’ll:

- **Organize memory** with [nodesets](https://docs.cognee.ai/core-concepts/further-concepts/node-sets) and apply filters during retrieval
- **Define your data model** using [ontology support](https://docs.cognee.ai/guides/ontology-support)
- **Enhance memory** with contextual enrichment layers
- **Visualize your graph** with [graph visualization](https://docs.cognee.ai/guides/graph-visualization) to explore stored knowledge
- **Search smarter** by combining vector similarity with graph traversal
- **Refine results** through interactive search and [feedback](https://docs.cognee.ai/guides/feedback-system)

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#example-use-case)

Example Use Case

In this example, you will use a **Cognee-powered [Coding Assistant](https://docs.cognee.ai/examples/code-assistants)** to get context-aware coding help.You can open [this example on a Google Colab Notebook](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing) and run the steps shown below to build your cognee memory interactively.

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#prerequisites)

Prerequisites

- OpenAI API key (or another supported LLM provider)

> Cognee uses OpenAI’s GPT-5 model as default. Note that the OpenAI free tier does not satisfy the rate limit requirements. Please refer to our [LLM providers documentation](https://docs.cognee.ai/setup-configuration/llm-providers) to use another provider.

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#setup)

Setup

First, let’s set up the environment and import necessary modules.

Utility Functions Setup

Install Cognee using pip:

```
!pip install cognee==0.3.4

# Create artifacts directory for storing visualization outputs
artifacts_path = utils.create_notebook_artifacts_directory()

import cognee
```

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#create-sample-data-to-ingest-into-memory)

Create Sample Data to Ingest into Memory

In this example, we’ll use a **Python developer** scenario. The data sources we’ll ingest into Cognee include:

- A short introduction about the developer (`developer_intro`)
- A conversation between the developer and a coding agent (`human_agent_conversations`)
- The Zen of Python principles (`python_zen_principles`)
- A basic ontology file with structured data about common technologies (`ontology`)

### 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#prepare-the-sample-data)

Prepare the Sample Data

```
# Define the developer introduction to simulate personal context
developer_intro = (
    "Hi, I'm an AI/Backend engineer. "
    "I build FastAPI services with Pydantic, heavy asyncio/aiohttp pipelines, "
    "and production testing via pytest-asyncio. "
    "I've shipped low-latency APIs on AWS, Azure, and GoogleCloud."
)

# Download additional datasets from the Cognee repository
asset_paths = utils.download_remote_assets()
human_agent_conversations = asset_paths["human_agent_conversations"]
python_zen_principles = asset_paths["python_zen_principles"]
ontology_path = asset_paths["ontology"]
```

The `download_remote_assets()` function:

- Handles multiple file types (JSON, Markdown, ontology)
- Creates the required folders automatically
- Prevents redundant downloads

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#review-the-structure-and-content-of-downloaded-data)

Review the Structure and Content of Downloaded Data

Next, let’s inspect the data we just downloaded.  
Use `preview_downloaded_assets()` to quickly summarize and preview each file’s structure and contents before Cognee processes them.

```
# Preview each file's structure and contents
utils.preview_downloaded_assets(asset_paths)
```

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#reset-memory-and-add-structured-data)

Reset Memory and Add Structured Data

Start by resetting Cognee’s memory using `prune()` to ensure a clean, reproducible run.  
Then, use [`add()`](https://docs.cognee.ai/core-concepts/main-operations/add) to load your data into dedicated node sets for organized memory management.

```
await cognee.prune.prune_data()
await cognee.prune.prune_system(metadata=True)

await cognee.add(developer_intro, node_set=["developer_data"])
await cognee.add(human_agent_conversations, node_set=["developer_data"])
await cognee.add(python_zen_principles, node_set=["principles_data"])
```

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#configure-the-ontology-and-build-a-knowledge-graph)

Configure the Ontology and Build a Knowledge Graph

Set the ontology file path, then run [`cognify()`](https://docs.cognee.ai/core-concepts/main-operations/cognify) to transform all data into a **knowledge graph** backed by embeddings.  
Cognee automatically loads the ontology configuration from the `ONTOLOGY_FILE_PATH` environment variable.

```
# Configure ontology file path for structured data processing
os.environ["ONTOLOGY_FILE_PATH"] = ontology_path

# Transform all data into a knowledge graph backed by embeddings
await cognee.cognify()
```

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#visualize-and-inspect-the-graph-before-and-after-enrichment)

Visualize and Inspect the Graph Before and After Enrichment

Generate HTML visualizations of your knowledge graph to see how Cognee processed the data.First, visualize the initial graph structure. Then, use [`memify()`](https://docs.cognee.ai/core-concepts/main-operations/memify) to enhance the knowledge graph adding deeper semantic connections and improves relationships between concepts. Finally, generate a second visualization to compare the enriched graph.

```
# Generate initial graph visualization showing nodesets and ontology structure
initial_graph_visualization_path = str(artifacts_path / "graph_visualization_nodesets_and_ontology.html")
await cognee.visualize_graph(initial_graph_visualization_path)

# Enhance the knowledge graph with memory consolidation for improved connections
await cognee.memify()

# Generate second graph visualization after memory enhancement
enhanced_graph_visualization_path = str(artifacts_path / "graph_visualization_after_memify.html")
await cognee.visualize_graph(enhanced_graph_visualization_path)
```

The generated HTML files can be opened in your browser to explore and inspect the graph structure.

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#query-cognee-memory-with-natural-language)

Query Cognee Memory with Natural Language

Run cross-document [searches](https://docs.cognee.ai/core-concepts/main-operations/search) to connect information across multiple data sources.  
Then, perform filtered searches within specific node sets to focus on targeted context.

```
# Cross-document knowledge retrieval from multiple data sources
results = await cognee.search(
    query_text="How does my AsyncWebScraper implementation align with Python's design principles?",
    query_type=cognee.SearchType.GRAPH_COMPLETION,
)
print("Python Pattern Analysis:", results)

# Filtered search using NodeSet to query only specific subsets of memory
from cognee.modules.engine.models.node_set import NodeSet

results = await cognee.search(
    query_text="How should variables be named?",
    query_type=cognee.SearchType.GRAPH_COMPLETION,
    node_type=NodeSet,
    node_name=["principles_data"],
)
print("Filtered search result:", results)
```

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#provide-interactive-feedback-for-continuous-learning)

Provide Interactive Feedback for Continuous Learning

Run a search with `save_interaction=True` to capture user feedback.  
Then, use the `FEEDBACK` query type to refine future retrievals and improve Cognee’s performance over time.

```
# Interactive search with feedback mechanism for continuous improvement
answer = await cognee.search(
    query_type=cognee.SearchType.GRAPH_COMPLETION,
    query_text="What is the most zen thing about Python?",
    save_interaction=True,
)
print("Initial answer:", answer)

# Provide feedback on the previous search result
# The last_k parameter specifies which previous answer to give feedback about
feedback = await cognee.search(
    query_type=cognee.SearchType.FEEDBACK,
    query_text="Last result was useful, I like code that complies with best practices.",
    last_k=1,
)
```

## 

[​

](https://docs.cognee.ai/examples/getting-started-with-cognee#visualize-the-graph-after-feedback)

Visualize the Graph After Feedback

Generate a final visualization to see how the feedback mechanism improved the knowledge graph.

```
feedback_enhanced_graph_visualization_path = str(
    artifacts_path / "graph_visualization_after_feedback.html"
)

await cognee.visualize_graph(feedback_enhanced_graph_visualization_path)
```

This view highlights the enhanced connections and learning captured from user feedback.





# Cognee CLI Overview

Copy page

Command line interface for Cognee AI memory operations

The `cognee-cli` command lets you run Cognee from the terminal so you can add data, build the knowledge graph, and ask questions without opening a Python file. The commands are designed to be short, use friendly defaults, and are safe for people who are just starting out.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#setup)

Setup

Before using the CLI, you need to configure your API key. The recommended approach is to store it in a `.env` file:

```
# Create a .env file in your project root
echo "LLM_API_KEY=your_openai_api_key" > .env
```

Alternatively, you can export it in your terminal session:

```
export LLM_API_KEY=your_openai_api_key
```

Use the `cognee-cli config set` command only for temporary tweaks during a long-running session. For persistent configuration, use `.env` files or environment variables.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#quick-tour-of-commands)

Quick Tour of Commands

- `cognee-cli add <data>` loads documents or text into a dataset
- `cognee-cli cognify` turns datasets into a knowledge graph
- `cognee-cli search "question"` asks the graph for answers
- `cognee-cli delete` removes stored data when you no longer need it
- `cognee-cli config` reads and updates saved settings
- `cognee-cli -ui` launches the local web app

Add `--help` after any command (for example, `cognee-cli search --help`) to see every option.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#add-data)

Add Data

Start by loading something the graph can learn from. You can add files, folders, URLs, or even plain text.

```
# Add a single file to the default dataset
cognee-cli add docs/company-handbook.pdf

# Pick a dataset name so you can separate topics later
cognee-cli add docs/policies.docx --dataset-name onboarding

# Add multiple files at once
cognee-cli add docs/policies.docx docs/faq.md --dataset-name onboarding

# Add a short text note (wrap the note in quotes)
cognee-cli add "Kickoff call notes: customer wants faster onboarding" --dataset-name sales_calls
```

Add Command Options

- `data`: One or more file paths, URLs, or text strings. Mix and match as needed
- `--dataset-name` (`-d`): Defaults to `main_dataset`. Use clear names so the team remembers what each dataset holds

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#cognify-data)

Cognify Data

Cognify builds the knowledge graph. Run it whenever you add new data or change the ontology.

```
# Process every dataset
cognee-cli cognify

# Process specific datasets only
cognee-cli cognify --datasets onboarding sales_calls

# Increase chunk size and show more logs
cognee-cli cognify --datasets onboarding --chunk-size 1500 --chunker TextChunker --verbose

# Kick off a long job and return immediately
cognee-cli cognify --datasets onboarding --background
```

Cognify Command Options

- `--datasets` (`-d`): Space-separated list. Skip it to process everything
- `--chunk-size`: Token limit for each chunk. Leave blank to let Cognee choose
- `--chunker`: `TextChunker` (default) or `LangchainChunker` if installed
- `--background` (`-b`): Handy for large datasets; the CLI exits while the job keeps running
- `--verbose` (`-v`): Prints progress messages
- `--ontology-file`: Path to a custom ontology (`.owl`, `.rdf`, etc.)

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#search-the-graph)

Search the Graph

Once cognify finishes, you can question the graph. Start with a simple natural-language question, then experiment with search types.

```
# Default search (GRAPH_COMPLETION)
cognee-cli search "Who owns the rollout plan?"

# Limit the scope to one dataset
cognee-cli search "What is the onboarding timeline?" --datasets onboarding

# Return three answers at most
cognee-cli search "List the key risks" --top-k 3

# Save a JSON response for another tool
cognee-cli search "Which documents mention security?" --output-format json
```

Search Types

Try these quick examples to feel the differences:

```
# Conversational answer with reasoning (default)
cognee-cli search "Give me a summary of onboarding" --query-type GRAPH_COMPLETION

# Shorter answer based on chunks
cognee-cli search "Show the onboarding steps" --query-type RAG_COMPLETION

# Highlight relationships and insights
cognee-cli search "How do onboarding tasks connect?" --query-type INSIGHTS

# Raw text passages you can copy
cognee-cli search "Find security requirements" --query-type CHUNKS --top-k 5

# Summaries only (great for reviews)
cognee-cli search "Summarise the onboarding handbooks" --query-type SUMMARIES

# Code-aware search for repos
cognee-cli search "Where is the email parser?" --query-type CODE

# Advanced graph query (requires Cypher skills)
cognee-cli search "MATCH (n) RETURN COUNT(n)" --query-type CYPHER
```

Search Command Options

- `--query-type`: Choose from GRAPH_COMPLETION, RAG_COMPLETION, INSIGHTS, CHUNKS, SUMMARIES, CODE, or CYPHER
- `--datasets`: Limit search to specific datasets
- `--top-k`: Maximum number of results to return
- `--system-prompt`: Point to a custom prompt file for LLM-backed modes
- `--output-format` (`-f`): `pretty` (friendly layout), `simple` (minimal text), or `json` (structured output for scripts)

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#delete-data)

Delete Data

Clean up when a dataset is outdated or when you reset the environment.

```
# Remove one dataset (asks for confirmation)
cognee-cli delete --dataset-name onboarding

# Remove everything for a specific user
cognee-cli delete --user-id 123e4567

# Wipe all data (add --force to skip the question)
cognee-cli delete --all --force
```

Delete Command Options

- `--dataset-name`: Remove a specific dataset
- `--user-id`: Remove all data for a specific user
- `--all`: Remove all data (use with caution)
- `--force`: Skip confirmation prompts

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#manage-configuration)

Manage Configuration

The CLI stores its settings so you do not have to repeat them. Configuration updates line up with the Python API.

```
# See the list of supported keys
cognee-cli config list

# Check one value (if implemented)
cognee-cli config get llm_model

# Update your LLM provider and model
cognee-cli config set llm_provider openai
cognee-cli config set llm_model gpt-4o-mini

# Store an API key (quotes are optional)
cognee-cli config set llm_api_key sk-yourkey

# Reset a key back to its default value
cognee-cli config unset chunk_size
```

Config Command Options

- `list`: Print the common keys
- `get [key]`: Show the saved value; omit the key to list everything
- `set <key> <value>`: Save a new value. JSON strings such as `{}` or `true` are parsed automatically
- `unset <key>`: Reset to the default. Add `--force` to skip confirmation
- `reset`: Placeholder for a future “reset everything” command

Useful Configuration Keys

- Language model: `llm_provider`, `llm_model`, `llm_api_key`, `llm_endpoint`
- Storage: `graph_database_provider`, `vector_db_provider`, `vector_db_url`, `vector_db_key`
- Chunking: `chunk_size`, `chunk_overlap`

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#launch-the-ui)

Launch the UI

Prefer a browser view? Launch the UI with one flag.

```
cognee-cli -ui
```

The CLI starts the backend on `http://localhost:8000` and the React app on `http://localhost:3000`. Leave the window open and press `Ctrl+C` to stop everything.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#next-steps)












