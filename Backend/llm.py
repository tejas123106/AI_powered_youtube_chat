
import ollama

MODEL_NAME = "qwen2.5:3b"


def generate_answer(prompt):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
                You are an intelligent YouTube AI assistant.

                Answer questions using only the provided
                video transcript context.

                Do not invent information.

                If the answer is unavailable,
                clearly mention that.

                Include relevant timestamps.

                Keep answers concise and direct.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2,
            "num_predict": 250
        }
    )

    return response["message"]["content"]
