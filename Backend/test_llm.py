
from llm import generate_answer

prompt = """
Context:

RAG stands for Retrieval Augmented Generation.

It combines information retrieval with
large language models.

Question:

What is RAG and why is it used?

Answer:
"""

answer = generate_answer(prompt)

print("\nGenerated Answer:\n")
print(answer)
