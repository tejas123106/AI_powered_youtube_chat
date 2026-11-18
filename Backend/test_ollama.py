
import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in simple terms."
        }
    ]
)

print("\nAI RESPONSE:\n")
print(response["message"]["content"])
