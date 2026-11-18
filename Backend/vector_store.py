
import os
import pickle
import faiss
import numpy as np

from embeddings import generate_embeddings

VECTOR_DB_PATH = "vector_db"


def create_vector_store(video_id, documents):

    video_path = os.path.join(
        VECTOR_DB_PATH, video_id
    )

    os.makedirs(video_path, exist_ok=True)

    texts = [doc["text"] for doc in documents]

    embeddings = generate_embeddings(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        np.asarray(embeddings, dtype="float32")
    )

    faiss.write_index(
        index,
        os.path.join(video_path, "index.faiss")
    )

    with open(
        os.path.join(video_path, "documents.pkl"),
        "wb"
    ) as file:

        pickle.dump(documents, file)


def retrieve_documents(video_id, question, top_k=5):

    video_path = os.path.join(
        VECTOR_DB_PATH, video_id
    )

    index_path = os.path.join(
        video_path, "index.faiss"
    )

    document_path = os.path.join(
        video_path, "documents.pkl"
    )

    if not os.path.exists(index_path):
        raise ValueError("Video index not found")

    index = faiss.read_index(index_path)

    with open(document_path, "rb") as file:
        documents = pickle.load(file)

    if not documents:
        return []

    query_embedding = generate_embeddings([question])

    scores, indices = index.search(
        np.asarray(query_embedding, dtype="float32"),
        min(top_k, len(documents))
    )

    retrieved_docs = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        retrieved_docs.append({
            **documents[idx],
            "score": float(score)
        })

    return retrieved_docs
