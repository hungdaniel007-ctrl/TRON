# maestro.md - Contenido de: /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples

**Extensiones procesadas:** `.md`

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/code-assistants.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Assistants

## CodeGraph: Enhancing Codebase Understanding with Graphs and LLMs

### Scenario:

Modern software development often involves massive codebases spread across multiple repositories, teams, and services. Engineers and AI-based coding copilots struggle to maintain a clear mental model of how components interrelate. For instance:

* **Large Repositories:** A large software project might have a large of GitHub repository, containing thousands of files.
* **Complex Dependencies:** Services often call each other via APIs, share data models, or rely on specific configuration files. Finding the right function, class, or module can become tedious.
* **Evolving Code:** As code evolves, comments get stale, architectural assumptions shift, and documentation becomes outdated, making it hard for coding copilots to reliably generate correct, context-aware suggestions.

### Challenges:

1. **Fragmented Knowledge:** It’s difficult to piece together the entire dependency graph across the entire repository.
2. **Limited Context for LLMs:** Large Language Models struggle with providing accurate code completions or refactoring suggestions if they lack a broader view of the project’s architecture.
3. **Time Lost:** Developers spend significant time searching through repositories, reading documentation, and attempting to piece together the "big picture" of the codebase.

### Solution: Creating a CodeGraph

A **CodeGraph** is a knowledge graph that models the Python codebase at multiple levels of granularity. It goes beyond just indexing code: it captures entities and relationships within and across repositories.

* **Entities:**
  Functions, classes, modules, services, configuration files, APIs, tests, CI/CD pipelines, and documentation pages.

* **Relationships:**
  Who-calls-what (function call graphs), import dependencies, version histories, code ownership, and semantic links (e.g., "this module implements a particular design pattern" or "this API endpoint is deprecated and replaced by another").

How we constructed a CodeGraph:

* Build chain access direct dependency
* Build init mediated direct dependency
* Define pydantic data structures that describe a single knowledge nodes for all nodes
* Create a knowledge graph
* Write an in-memory retriever that gets the graphs skeletons and extracts triplets

Here is an example graph generated with cognee:
<img src="https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=1a1cef6c6160158111ca4ae7aa4eae56" alt="code_assistants_graph_example" data-og-width="588" width="588" data-og-height="720" height="720" data-path="images/code_assistants_graph_example.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?w=280&fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=1154616669b1f29f9f1dc7bb11586a60 280w, https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?w=560&fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=a1e0e74c2abdae58821f76d629c80ede 560w, https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?w=840&fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=a258e5b1f839a607eef7bdb7eac84a85 840w, https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?w=1100&fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=e5b03b335b7110b7afb270f70acc5b1e 1100w, https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?w=1650&fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=a9a5f5640d0b35fa2b0fb712d87f6a43 1650w, https://mintcdn.com/cognee/of3mX7JsgcxLIPDF/images/code_assistants_graph_example.png?w=2500&fit=max&auto=format&n=of3mX7JsgcxLIPDF&q=85&s=1be7037a7f30be598f352c2fbd5a5257 2500w" />

Read more about our approach in our [blog](https://www.cognee.ai/blog/deep-dives/repo_to_knowledge_graph).

**Enriching CodeGraph with LLMs:**
To make this knowledge even more actionable, integrate Large Language Models that understand code semantics and developer documentation. The LLM can:

1. **Ingest the Graph:**
   The LLM has access to structured context from the CodeGraph, so when a developer asks, *"Where is the function that parses user inputs for our search engine?"*, the LLM can quickly locate that function by following the graph’s relationships rather than brute-forcing file searches.

2. **Provide Context-Rich Suggestions:**
   When the coding copilot suggests a code snippet, it can reference related modules, highlight deprecations, or warn about known compatibility issues. For example, *"You might want to call `FunctionParseUserInput` from `Utils/InputProcessor.js`. It's used in `SearchEngine.js` and depends on `InputSchema.json`."*

3. **Explain Architectural Decisions:**
   Developers can query the LLM about architectural choices: *"Why does `ServiceD` depend on `ServiceE`?"*. The LLM, using the CodeGraph, responds: *"ServiceD calls `ServiceE`'s authentication endpoint to validate tokens, as documented in `ServiceE/docs/auth.md`."*

4. **Link to Documentation and Commit Histories:**
   The LLM can connect a piece of code to its associated design docs, recent commit messages, or open pull requests. If a developer asks, *"How has `UserProfileAPI.js` changed over the last quarter?"* the LLM can summarize major refactoring steps, point to relevant issues that were closed, and link to architectural decision records.

### Outcomes:

* **Improved Developer Productivity:**
  Instead of wading through multiple repositories, developers get immediate, context-aware guidance, saving countless hours of manual searching and guesswork.

* **More Accurate Code Suggestions:**
  Coding copilots armed with a CodeGraph context deliver more reliable and secure code completions, better refactoring strategies, and insightful recommendations.

* **Evolving with the Codebase:**
  As repositories grow, the CodeGraph and the LLM continuously update. This ensures that as code evolves, the memory and context available to developers—and their automated assistants—stays fresh and relevant.

#### Run a Demo Yourself!

Curious about how this works with cognee? Try it out in our notebook [here](https://github.com/topoteretes/cognee/blob/291f1c5a55abacdef3356fabd37ee0a677db34e1/notebooks/cognee_code_graph_demo.ipynb).

#### Join the Conversation!

Have questions? Join our community now to connect with professionals, share insights, and get your questions answered!

<br />

<a href="https://discord.gg/m63hxKsp4p" target="_blank" rel="noopener noreferrer">
  <button className="button cta-button">
    Join the community
  </button>
</a>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/maestro.md

```

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/getting-started-with-cognee.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Cognee Walkthrough

> From Data to Interactive Memory: End-to-end tutorial with nodesets, ontologies, memify, graph visualization, and feedback system using a coding assistant example

Cognee gives you the tools to **build smarter AI agents** with context-aware memory.

Use it to create a **queryable knowledge graph** powered by embeddings from your data. When retrieving data, your agent can reach up to **92.5% accuracy**.

## What You'll Learn

In this tutorial, you'll:

* **Organize memory** with [nodesets](/core-concepts/further-concepts/node-sets) and apply filters during retrieval
* **Define your data model** using [ontology support](/guides/ontology-support)
* **Enhance memory** with contextual enrichment layers
* **Visualize your graph** with [graph visualization](/guides/graph-visualization) to explore stored knowledge
* **Search smarter** by combining vector similarity with graph traversal
* **Refine results** through interactive search and [feedback](/guides/feedback-system)

## Example Use Case

In this example, you will use a **Cognee-powered [Coding Assistant](/examples/code-assistants)** to get context-aware coding help.

You can open [this example on a Google Colab Notebook](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing) and run the steps shown below to build your cognee memory interactively.

## Prerequisites

* OpenAI API key (or another supported LLM provider)

> Cognee uses OpenAI's GPT-5 model as default. Note that the OpenAI free tier does not satisfy the rate limit requirements. Please refer to our [LLM providers documentation](https://docs.cognee.ai/setup-configuration/llm-providers) to use another provider.

## Setup

First, let's set up the environment and import necessary modules.

<Accordion title="Utility Functions Setup">
  Create a utility class to handle file downloads and visualization helpers:

  ```python  theme={null}
  class NotebookUtils:
      """Utility class for cognee demo - helper methods to keep the main notebook clean and focused."""
      
      def __init__(self):
          """Initialize the NotebookUtils with default configurations."""
          self.artifacts_dir = None
          self.assets_config = self._initialize_assets_config()
      
      def _initialize_assets_config(self) -> Dict[str, Tuple[str, str]]:
          """Initialize configuration mapping for remote assets to download from cognee repository."""
          return {
              "human_agent_conversations": (
                  "/content/copilot_conversations.json",
                  "https://raw.githubusercontent.com/topoteretes/cognee/main/notebooks/data/copilot_conversations.json",
              ),
              "python_zen_principles": (
                  "/content/zen_principles.md",
                  "https://raw.githubusercontent.com/topoteretes/cognee/main/notebooks/data/zen_principles.md",
              ),
              "ontology": (
                  "/content/basic_ontology.owl",
                  "https://raw.githubusercontent.com/topoteretes/cognee/main/examples/python/ontology_input_example/basic_ontology.owl",
              ),
          }
      
      def download_remote_file_if_not_exists(self, local_path: str, remote_url: str) -> str:
          """Download remote file if it doesn't exist locally to avoid unnecessary re-downloads."""
          file_path = Path(local_path)
          if not file_path.exists():
              file_path.parent.mkdir(parents=True, exist_ok=True)
              urllib.request.urlretrieve(remote_url, file_path)
              print(f"Downloaded: {file_path.name}")
          else:
              print(f"File already exists: {file_path.name}")
          return str(file_path)
      
      def load_json_file_content(self, file_path: str) -> Dict[str, Any]:
          """Load and parse JSON file content into a Python dictionary."""
          with open(file_path, "r", encoding="utf-8") as file:
              return json.load(file)
      
      def load_text_file_content(self, file_path: str) -> str:
          """Load and return raw text content from a text file."""
          with open(file_path, "r", encoding="utf-8") as file:
              return file.read()
      
      def preview_json_structure(self, json_data: Dict[str, Any], max_keys: int = 3) -> None:
          """Display formatted preview of JSON data structure and sample content."""
          print("JSON Structure Preview:")
          pprint.pp(list(json_data.keys())[:max_keys])
          if "conversations" in json_data and json_data["conversations"]:
              print("Sample conversation:")
              pprint.pp(json_data["conversations"][0])
      
      def preview_text_content(self, text_content: str, max_chars: int = 200) -> None:
          """Display formatted preview of text content to show its format."""
          print("Text Content Preview:")
          print(text_content[:max_chars])
          if len(text_content) > max_chars:
              print(f"... (truncated, total length: {len(text_content)} characters)")
      
      def create_notebook_artifacts_directory(self, dir_name: str = "artifacts") -> Path:
          """Create and return artifacts directory for storing notebook outputs like graph visualizations."""
          notebook_dir = Path.cwd()
          self.artifacts_dir = notebook_dir / dir_name
          self.artifacts_dir.mkdir(exist_ok=True)
          print(f"Artifacts directory created/verified at: {self.artifacts_dir}")
          return self.artifacts_dir
      
      def download_remote_assets(self) -> Dict[str, str]:
          """Download all remote assets from cognee repository and return their local file paths."""
          downloaded_assets = {}
          
          print("Downloading remote assets...")
          print("-" * 40)
          
          for asset_name, (local_path, remote_url) in self.assets_config.items():
              downloaded_assets[asset_name] = self.download_remote_file_if_not_exists(
                  local_path, remote_url
              )
          
          print("-" * 40)
          print(f"Successfully processed {len(downloaded_assets)} assets")
          return downloaded_assets
      
      def preview_downloaded_assets(self, asset_paths: Dict[str, str]) -> None:
          """Display comprehensive preview of all downloaded assets."""
          print("=== ASSET PREVIEWS ===\n")
          
          # Preview JSON files
          for asset_name, file_path in asset_paths.items():
              if file_path.endswith('.json'):
                  print(f"--- {asset_name.upper()} ---")
                  json_data = self.load_json_file_content(file_path)
                  self.preview_json_structure(json_data)
                  print()
          
          # Preview text files
          for asset_name, file_path in asset_paths.items():
              if file_path.endswith(('.md', '.txt')):
                  print(f"--- {asset_name.upper()} ---")
                  text_content = self.load_text_file_content(file_path)
                  self.preview_text_content(text_content)
                  print()
          
          # Preview OWL files
          for asset_name, file_path in asset_paths.items():
              if file_path.endswith('.owl'):
                  print(f"--- {asset_name.upper()} ---")
                  print(f"OWL ontology file: {Path(file_path).name}")
                  text_content = self.load_text_file_content(file_path)
                  self.preview_text_content(text_content, max_chars=300)
                  print()

  # Initialize the utility class
  utils = NotebookUtils()
  ```
</Accordion>

Install Cognee using pip:

```bash  theme={null}
!pip install cognee==0.3.4

# Create artifacts directory for storing visualization outputs
artifacts_path = utils.create_notebook_artifacts_directory()

import cognee
```

## Create Sample Data to Ingest into Memory

In this example, we'll use a **Python developer** scenario. The data sources we'll ingest into Cognee include:

* A short introduction about the developer (`developer_intro`)
* A conversation between the developer and a coding agent (`human_agent_conversations`)
* The Zen of Python principles (`python_zen_principles`)
* A basic ontology file with structured data about common technologies (`ontology`)

### Prepare the Sample Data

```python  theme={null}
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

The `download_remote_assets()` function:

* Handles multiple file types (JSON, Markdown, ontology)
* Creates the required folders automatically
* Prevents redundant downloads

## Review the Structure and Content of Downloaded Data

Next, let’s inspect the data we just downloaded.\
Use `preview_downloaded_assets()` to quickly summarize and preview each file’s structure and contents before Cognee processes them.

```python  theme={null}
# Preview each file's structure and contents
utils.preview_downloaded_assets(asset_paths)
```

## Reset Memory and Add Structured Data

Start by resetting Cognee's memory using `prune()` to ensure a clean, reproducible run.\
Then, use [`add()`](/core-concepts/main-operations/add) to load your data into dedicated node sets for organized memory management.

```python  theme={null}
await cognee.prune.prune_data()
await cognee.prune.prune_system(metadata=True)

await cognee.add(developer_intro, node_set=["developer_data"])
await cognee.add(human_agent_conversations, node_set=["developer_data"])
await cognee.add(python_zen_principles, node_set=["principles_data"])
```

## Configure the Ontology and Build a Knowledge Graph

Set the ontology file path, then run [`cognify()`](/core-concepts/main-operations/cognify) to transform all data into a **knowledge graph** backed by embeddings.\
Cognee automatically loads the ontology configuration from the `ONTOLOGY_FILE_PATH` environment variable.

```python  theme={null}
# Configure ontology file path for structured data processing
os.environ["ONTOLOGY_FILE_PATH"] = ontology_path

# Transform all data into a knowledge graph backed by embeddings
await cognee.cognify()
```

## Visualize and Inspect the Graph Before and After Enrichment

Generate HTML visualizations of your knowledge graph to see how Cognee processed the data.

First, visualize the initial graph structure. Then, use [`memify()`](/core-concepts/main-operations/memify) to enhance the knowledge graph adding deeper semantic connections and improves relationships between concepts. Finally, generate a second visualization to compare the enriched graph.

```python  theme={null}
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

## Query Cognee Memory with Natural Language

Run cross-document [searches](/core-concepts/main-operations/search) to connect information across multiple data sources.\
Then, perform filtered searches within specific node sets to focus on targeted context.

```python  theme={null}
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

## Provide Interactive Feedback for Continuous Learning

Run a search with `save_interaction=True` to capture user feedback.\
Then, use the `FEEDBACK` query type to refine future retrievals and improve Cognee’s performance over time.

```python  theme={null}
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

## Visualize the Graph After Feedback

Generate a final visualization to see how the feedback mechanism improved the knowledge graph.

```python  theme={null}
feedback_enhanced_graph_visualization_path = str(
    artifacts_path / "graph_visualization_after_feedback.html"
)

await cognee.visualize_graph(feedback_enhanced_graph_visualization_path)
```

This view highlights the enhanced connections and learning captured from user feedback.

## Next Steps

<CardGroup cols={2}>
  <Card title="Join the Community" href="https://discord.gg/cqF6RhDYWz" icon="discord">
    **Cognee Discord**

    Join over 1,000 builders to ask questions and share insights.
  </Card>

  <Card title="Explore Examples" href="https://github.com/topoteretes/cognee" icon="github">
    **GitHub Repository**

    Star our repo ⭐ and try additional examples to deepen your knowledge.
  </Card>
</CardGroup>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/data-silos.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Data Silos

## Enterprise Data Unification

Every enterprise has the same problem: valuable data locked in silos. Your CRM doesn't talk to your ERP. Your knowledge base doesn't connect to your support tickets. Your strategic documents live in SharePoint while operational data lives in Snowflake.

Cognee creates a unified memory layer that connects these silos without replacing them.

## The Siloed Data Problem

When someone asks "What's the full context on the Acme Corp relationship?", the answer requires piecing together:

* CRM opportunity and contact data
* Support ticket history and resolution patterns
* Contract terms and renewal dates
* Invoice and payment history
* Relevant Slack conversations and email threads

No single system has the complete picture. Neither does traditional RAG.

## Why Standard RAG Fails Here

Vector search treats each chunk independently. It might find a support ticket mentioning Acme Corp and a contract with their name, but it doesn't understand that:

* The support ticket was about a feature that the contract specifically excludes
* The escalation pattern matches a trend you're seeing with other enterprise customers
* The contract renewal is approaching and the recent ticket volume is a risk signal

Relationships matter as much as content. Cognee captures both.

## Implementation: Connect, Cognify, Query

The Cognee Memory Layer sits on top of your existing data infrastructure:

### Step 1: Connect Your Sources

Cognee supports 30+ data sources out of the box:

```python  theme={null}
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

### Step 2: Cognify

Build the knowledge graph that connects entities across sources:

```python  theme={null}
# Process all sources into a unified memory layer
await cognee.cognify()
```

Cognee automatically:

* Extracts entities (customers, products, people, concepts)
* Identifies relationships between entities
* Creates semantic embeddings for content
* Resolves entity references across sources (e.g., "Acme Corp" = "Acme Corporation" = "ACME")

### Step 3: Query with Context

Now queries return connected knowledge, not isolated chunks:

```python  theme={null}
results = await cognee.search(
    query_text="Full context on Acme Corp",
    search_type=SearchType.GRAPH_COMPLETION
)
```

Ready to unify your data silos? [Start with the open-source SDK](https://github.com/topoteretes/cognee) or [talk to our team](https://calendly.com/vasilije-topoteretes/) about enterprise deployment.

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/vertical-ai-agents.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Vertical AI Agents

The future of AI is autonomous agents that execute complex, multi-step tasks in specialized domains. But agents without memory are agents without context. They can't learn from past interactions, can't understand organizational nuances, and can't improve over time.

Cognee provides the memory layer that makes agentic AI actually work.

## The Problem: Agents That Forget

Consider an AI agent designed to automate legal contract review. Without persistent memory, every document is a blank slate:

* The agent doesn't remember that your company uses specific non-standard clauses
* It can't recall that the counterparty had issues with similar terms last quarter
* It has no context about your organization's risk tolerance or negotiation patterns

## Why Memory Matters for Agents and What Cognee Brings

Agentic AI systems need three capabilities that standard RAG cannot provide:

### 1. Domain Understanding

The agent must understand how your enterprise works instead of only generic industry knowledge, in terms of your specific organizational structure, terminology, and processes.

### 2. Personalization

Each user, client, or session can have tailored context. The agent adapts its responses based on individual preferences, history, and past interactions stored in memory.

### 3. Dynamically Evolving Memory

As the agent operates, it should learn and improve. Patterns from successful task completions should inform future actions.

Our memory layer provides:

**Structured Context for Reasoning**
Rather than raw text chunks, agents receive graph-structured knowledge that captures relationships, hierarchies, and domain logic.

**Continuous Learning**
Through `memify()`, feedback mechanism and many more advanced features, agents consolidate experiences into persistent memory, improving task execution over time.

**Advanced Retrieval**
Multiple search types—graph completion, semantic chunks, summaries—let agents retrieve exactly the context they need for each decision.

### Example: Contract Review Agent with Memory

Define tools that give your agent persistent memory:

```python  theme={null}
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

```python  theme={null}
tools = [remember, recall]

agent = Agent(
    model="gpt-4o",
    system_prompt="You are a contract analyst. Use remember() to store important details and recall() to retrieve past context.",
    tools=tools
)
```

Now the agent has memory:

```python  theme={null}
# Session 1: Learn client preferences
agent.run("Remember: Acme Corp requires 30-day payment terms and California arbitration.")

# Session 2: Use memory for analysis
agent.run("Review this contract for Acme Corp: 60-day terms, New York jurisdiction.")
# Agent calls recall() → flags mismatches with stored preferences
```

## Integration with Agentic Frameworks

Cognee integrates with the frameworks you're already using:

* LangGraph, CrewAI, LlamaIndex, Agent Development Kit, etc.
* **Custom implementations**: Direct SDK integration with any agent framework

## Next Steps

Learn more about [Core Concepts](/core-concepts/overview) or review [Integrations](/integrations) for available options. If we don't have your favorite agent framework yet, let us know by [opening an issue on GitHub](https://github.com/topoteretes/cognee/issues).

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/edge-ai.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Edge AI

## Edge AI & On-Device Memory

Cognee is bringing AI memory to the edge with **cognee-RS**, our Rust-based SDK designed for resource-constrained devices. Run the full memory pipeline (ingestion, semantic organization, retrieval) directly on-device, sub-100ms recall and data stay local.

## The Edge AI Opportunity

Picture this: Your smart glasses capture a conversation during a run, instantly recall your to-do list, and feed you directions - all offline, with zero data uploaded. Or your smart-home hub analyzes your evening routine, suggests energy optimizations for better sleep, and monitors wellness patterns without sending a single byte to the cloud.

This is the future and the promise of edge AI memory.

## cognee-RS: Rust-Powered Memory for Devices

cognee-RS is our experimental Rust SDK. It is a port of cognee's proven memory architecture to edge devices like phones, smartwatches, glasses, and smart-home hubs.

It combines:

* A lean retrieval engine optimized for constrained resources
* Support for on-device LLMs
* Seamless hybrid switching to cloud when needed
* Full multimodal support (text, images, audio)

### Core Capabilities

**Fully Offline Operation**
Run with Phi-4-class LLMs and local embeddings—no internet required for queries or retrieval. Toggle to hosted models with a single config flag when you have connectivity and need more power.

**High Accuracy**
We're targeting 90%+ answer accuracy, matching our Python SDK. The local semantic layer ensures retrieval fidelity even with smaller models. Graph-aware retrieval boosts accuracy 15-25% through structural cues.

**Hybrid Execution**
Route tasks intelligently: local for embeddings, cloud for heavy entity extraction, or split dynamically based on connectivity, battery, and latency requirements.

**Multimodal Fusion**
Handles text, images, audio, and sensor data. Real-time fusion from device inputs (mic + camera) creates holistic context that a cloud-only approach can't match.

**Resource Orchestration**
Dynamic scheduling caps memory and CPU usage. Heavy processing doesn't interrupt core device functions—retrieval stays prioritized while batch ingestion happens during idle time.

## Use Cases: Where Edge Memory Excels

### Personal Voice Assistants

Smart earbuds and wearables that remember your conversations, preferences, and context—without uploading your private discussions to the cloud.

> "What did Sarah say about the project deadline during our walk yesterday?"

Local conversation memory enables instant recall. Sync only opt-in summaries, never raw audio.

### Smart Home & Wellness

Baby monitors, vital-sign wearables, and home hubs that analyze patterns locally—complying with GDPR and HIPAA by design.

* Sleep pattern analysis without cloud dependency
* Anomaly detection that works during internet outages
* Behavioral insights that stay on your network

Your health data stays yours.

### Robotics & Autonomous Systems

Drones, robots, and autonomous vehicles need real-time memory access for navigation and decision-making—especially in dead zones.

```
Robot enters new environment
    │
    ▼
cognee-RS builds local context map
    │
    ▼
Real-time retrieval: "Have I seen this obstacle type before?"
    │
    ▼
Decision without connectivity delay
```

No connectivity? No problem. Local context drives decisions.

### Industrial IoT

Factory-floor sensors, offline kiosks, and field equipment often operate in network-constrained environments.

Edge AI enables:

* 24/7 local reasoning without persistent connection
* Anomaly detection at the source
* Bandwidth savings—only critical events sync to cloud
* Continued operation during network outages

## Trade-Offs and Mitigations

Edge isn't effortless. Smaller models have tighter context windows. Devices have limited compute and battery budgets. Complex reasoning may exceed local capabilities.

cognee-RS addresses these constraints:

| Challenge              | Mitigation                               |
| ---------------------- | ---------------------------------------- |
| Limited context window | Graph-aware retrieval for precision      |
| Complex reasoning      | Hybrid execution—offload when needed     |
| Battery constraints    | Dynamic scheduling, idle-time processing |
| Storage limits         | Semantic compression, smart eviction     |
| Model size             | Support for Phi-4 class, upgradeable     |

cognee-RS is currently experimental. Early conversations with partners are giving promising results.

## The Vision: Memory Everywhere

The future isn't cloud-only AI. It's AI that runs where you are: on your phone, your glasses, your watch, your car. AI that remembers your context without uploading your life to someone else's servers.

cognee-RS is how we get there: the same semantic memory layer that powers enterprise deployments, compiled to run on the devices in your pocket.

Privacy-first. Real-time. Offline-capable. Memory-enabled.

***

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/examples/overview.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Overview

AI systems still struggle with the messy realities of data.

**The core challenges:**

* **Complex Data at Scale**: Databases spanning hundreds of tables, documents in dozens of formats, knowledge scattered across systems
* **Lack of Business Context**: Without domain ontologies and relationships, even advanced LLMs produce hallucinations
* **Stale Knowledge**: Static RAG doesn't evolve as your organization and data change

Cognee solves these problems by creating a unified memory layer, combining knowledge graphs with vector search to give AI systems true understanding of your data.

***

## Example Use Cases

### [Vertical AI Agents](./vertical-ai-agents)

The memory layer that makes autonomous agents actually work. Agents without memory can't learn, can't understand organizational context, and can't improve over time. Cognee provides the missing piece.

**Key capabilities:**

* Persistent memory across agent sessions
* Domain-specific reasoning context
* Continuous learning and improvement

***

### [Enterprise Data Unification](./data-silos)

Connect data silos without replacing your existing systems. When the answer requires CRM + support tickets + contracts + operational data, Cognee provides the unified view.

**Key capabilities:**

* 30+ data source connectors
* Entity resolution across systems
* Granular access control by user, team, or organization

***

### [Edge AI & On-Device Memory](./edge-ai)

Bring AI memory to resource-constrained devices with cognee-RS, our Rust-based SDK. Run the full memory pipeline directly on phones, smartwatches, glasses, and smart-home hubs—sub-100ms recall, data stays local.

**Key capabilities:**

* Fully offline operation with on-device LLMs
* Hybrid execution—local or cloud based on connectivity
* Privacy-first architecture for sensitive data

***

## Common Patterns Across Use Cases

### Memory Enrichment

All use cases benefit from Cognee's ability to consolidate information over time, not just at ingestion, but continuously as new data arrives and patterns emerge.

### Ontology Management

Whether it's financial instrument definitions, research taxonomies, or codebase architecture, Cognee aligns your domain-specific terminology into a coherent knowledge structure.

### Hybrid Search

Every query leverages both graph traversal (understanding relationships) and vector similarity (semantic matching) for complete, accurate results.

### Modular Customization

Cognee provides building blocks such as chunkers, loaders, retrievers, ontology definitions that you can customize for your specific domain without building from scratch.

***

## Dive Deeper in Use Cases:

* [Vertical AI Agents](./vertical-ai-agents) - The memory layer that makes autonomous agents actually work
* [Enterprise Data Unification](./data-silos) - Connect data silos without replacing your existing systems
* [Edge AI & On-Device Memory](./edge-ai) - Rust-powered AI memory for phones, wearables, and IoT devices

```

