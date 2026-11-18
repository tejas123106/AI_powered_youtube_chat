
from chunking import create_chunks
from vector_store import create_vector_store, retrieve_documents
from prompt import create_prompt
from llm import generate_answer


def process_video(video_id, transcript):

    # 1. Split transcript into chunks
    documents = create_chunks(transcript)

    # 2. Generate embeddings and save in FAISS
    create_vector_store(video_id, documents)

    return len(documents)


def ask_question(video_id, question):

    # 1. Retrieve relevant documents
    retrieved_docs = retrieve_documents(
        video_id,
        question,
        top_k=5
    )

    # 2. Construct prompt
    prompt = create_prompt(
        question,
        retrieved_docs
    )

    # 3. Generate answer using Ollama
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": retrieved_docs
    }
