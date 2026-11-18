def create_prompt(question, retrieved_docs):

    context = ""

    for i, doc in enumerate(retrieved_docs):

        timestamp = doc["start"]

        context += f"""
        Document {i+1}
        Timestamp: {timestamp}
        Content: {doc["text"]}
        """

    prompt = f"""
    You are an intelligent YouTube video assistant.

    Answer the user's question using the
    retrieved video transcript documents.

    Instructions:
    1. Use the provided context.
    2. Do not invent information.
    3. If the answer is unavailable, say so.
    4. Include relevant timestamps.
    5. Explain concepts clearly.

    Retrieved Context:
    {context}

    User Question:
    {question}

    Answer:
    """

    return prompt