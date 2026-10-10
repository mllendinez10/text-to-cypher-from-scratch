# text-to-cypher-from-scratch

This project focuses on learning how Text-to-Cypher works by building the complete pipeline from scratch in Python.

It intentionally avoids higher level frameworks at the beginning, so each step can be implemented and understood independently.

As a practical use case, the project uses connected Hilti product data stored in a Neo4j knowledge graph and allows users to ask questions in natural language, which are translated into Cypher queries and used to retrieve the relevant information from the graph.

## Project Goal

The goal is to gain hands-on experience with the main components of a Text-to-Cypher system:

* Structured data and graph schema preparation
* Data import into Neo4j
* Prompt construction using the graph schema and user question
* Cypher query generation with an LLM
* Cypher validation and safety checks
* Query execution against Neo4j
* Query result processing
* LLM answer generation
* Text-to-Cypher evaluation using a golden set
* UI development with Streamlit

## Technology Stack

| **Area**         | **Technology** |
| ---------------------- | -------------------- |
| Programming language   | Python               |
| Structured data source | Excel                |
| Graph schema           | JSON                 |
| Excel processing       | Pandas with openpyxl |
| Graph database         | Neo4j                |
| Query language         | Cypher               |
| LLM                    | Qwen3 4B via Ollama  |
| UI                     | Streamlit            |
