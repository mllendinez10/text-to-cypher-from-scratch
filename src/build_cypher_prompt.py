"""
Build a prompt from the graph schema and user question to generate a Cypher query.

"""

SCHEMA_FILE = "data/schema.json"


def build_cypher_prompt(question):
    
    # Read graph schema file as JSON text
    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        schema = file.read()


    # Prompt
    prompt = f"""
Generate Neo4j Cypher queries from natural language questions.

Instructions:
- Return only the Cypher query.
- Do not include explanations or Markdown code fences.
- Generate only a read only query.
- Do not create, update, or delete data.
- Use only the node labels, relationship types, and properties defined in the graph schema.
- Follow the relationship directions defined in the schema.
- Respect the units specified in the schema.
- Return information relevant to the user's question.
- Treat missing values as unknown, not as zero.
- For torque and resistance questions, match the configuration requested, including components and quantities where applicable.

Graph schema:
{schema}

User question:
{question}

Cypher query:
"""

    return prompt.strip()