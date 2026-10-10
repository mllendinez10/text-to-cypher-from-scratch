"""
Run the Text-to-Cypher pipeline by connecting the individual processing steps.
"""

from build_cypher_prompt import build_cypher_prompt


question = input("Ask a question: ")

cypher_prompt = build_cypher_prompt(question)

print(cypher_prompt)

