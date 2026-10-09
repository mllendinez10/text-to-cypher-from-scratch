"""
Tests the connection to neo4j by executing a simple Cypher query.

"""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

with GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(
        os.environ["NEO4J_USERNAME"],
        os.environ["NEO4J_PASSWORD"],
    ),
) as driver:
    driver.verify_connectivity()

    records, _, _ = driver.execute_query(
        "RETURN 'Connected to Neo4j!' AS message",
        database_=os.environ["NEO4J_DATABASE"],
    )

    print(records[0]["message"])