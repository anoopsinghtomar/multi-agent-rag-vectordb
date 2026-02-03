# phidata-agentic-rag-pgvector

An **agentic, multi-vector Retrieval-Augmented Generation (RAG) system** built with **phidata** and **pgvector**.

This repository demonstrates how multiple AI agents can collaboratively retrieve, reason, and generate responses over structured and unstructured data using PostgreSQL as the vector store.

---

## ✨ Features

- 🧠 **Multi-Agent Architecture**
  - Specialized agents for retrieval, reasoning, planning, and synthesis
  - Agent coordination using phidata

- 📚 **Multi-Vector RAG**
  - Store and query multiple embeddings per document
  - Support for chunk-level, summary-level, and metadata embeddings

- 🗄️ **PostgreSQL + pgvector**
  - Production-grade vector database
  - ACID compliance, SQL filtering, and hybrid search
  - Easy local and cloud deployment

- 🔍 **Hybrid Retrieval**
  - Vector similarity search
  - Metadata + semantic filtering

- ⚙️ **Extensible Design**
  - Swap models, agents, or embedding strategies
  - Add new tools or data sources with minimal changes

---

## 🏗️ Architecture Overview

User Query
↓
Planner Agent
↓
Retriever Agents (pgvector)
↓
Reasoning Agent
↓
Synthesis Agent
↓
Final Response


Each agent has a focused responsibility, enabling better reasoning, debuggability, and scalability compared to single-agent RAG systems.

---

## 🗂️ Project Structure
```
├── agents/ # Agent definitions (retriever, planner, etc.)
├── db/ # pgvector schema and utilities
├── embeddings/ # Multi-vector embedding strategies
├── ingestion/ # Data loaders and chunking logic
├── rag/ # RAG pipeline orchestration
├── config/ # Model and database configuration
├── scripts/ # Setup and utility scripts
└── main.py # Entry point
