from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(transcript):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    documents = []

    # Combine transcript entries while preserving
    # their timestamps.

    full_text = " ".join(
        item["text"] for item in transcript
    )

    splits = splitter.split_text(full_text)

    for chunk in splits:

        # Find approximate timestamp boundaries
        # in the original transcript.
        matched = [
            item for item in transcript
            if item["text"] in chunk
        ]

        start = matched[0]["start"] if matched else None

        end = (
            matched[-1]["start"] +
            matched[-1]["duration"]
            if matched else None
        )

        documents.append({
            "text": chunk,
            "start": start,
            "end": end
        })

    return documents