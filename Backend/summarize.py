
import os
import pickle
import ollama

from llm import MODEL_NAME

VECTOR_DB_PATH = "vector_db"

def summarize_video(video_id):

    # Load all transcript chunks
    video_path = os.path.join(VECTOR_DB_PATH, video_id)
    document_path = os.path.join(video_path, "documents.pkl")

    if not os.path.exists(document_path):
        raise ValueError("Video has not been processed yet.")

    with open(document_path, "rb") as file:
        documents = pickle.load(file)

    if not documents:
        raise ValueError("No transcript chunks found.")

    # Divide all chunks into batches of 10
    batch_size = 10
    batch_summaries = []

    for i in range(0, len(documents), batch_size):

        batch = documents[i:i + batch_size]

        context = "\n".join(
            doc["text"] for doc in batch
        )


        prompt = f"""
        You are summarizing a YouTube video transcript.

        IMPORTANT RULES:
        1. Use ONLY information explicitly present in the transcript.
        2. Do not introduce outside knowledge.
        3. Do not invent concepts, examples or explanations.
        4. Preserve the speaker's meaning.
        5. Include important concepts and examples.
        6. Keep the summary concise and factual.

        Summarize this transcript section:

        {context}
        """

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={"temperature": 0.3}
        )

        batch_summaries.append(
            response["message"]["content"]
        )

    # Combine all batch summaries
    
    final_prompt = f"""
    You are creating a complete summary of a YouTube video.

    Combine the following section summaries.

    Instructions:
    1. Use only the information in the section summaries.
    2. Remove repeated information.
    3. Organize concepts under meaningful headings.
    4. Include important examples and explanations.
    5. Do not invent additional topics.
    6. Make the summary easy to understand.

    Section summaries:

    {" ".join(batch_summaries)}
    """

    final_response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        options={"temperature": 0.3}
    )

    return {
        "summary": final_response["message"]["content"],
        "total_chunks_processed": len(documents),
        "batches_processed": len(batch_summaries)
    }