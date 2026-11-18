
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarize import summarize_video

from transcript import get_transcript
from rag import process_video, ask_question

app = FastAPI(title="YouTube AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class VideoRequest(BaseModel):
    video_id: str


class QuestionRequest(BaseModel):
    video_id: str
    question: str


@app.get("/")
def home():
    return {"message": "YouTube AI Assistant is running"}


@app.post("/ingest")
def ingest_video(request: VideoRequest):

    try:
        transcript = get_transcript(request.video_id)

        chunk_count = process_video(
            request.video_id,
            transcript
        )

        return {
            "message": "Video processed successfully",
            "video_id": request.video_id,
            "chunks_created": chunk_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/ask")
def ask(request: QuestionRequest):

    try:
        result = ask_question(
            request.video_id,
            request.question
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/summarize")
def summarize(request: VideoRequest):
    try:
        result = summarize_video(request.video_id)

        return {
            "message": "Video summarized successfully",
            "video_id": request.video_id,
            "summary": result["summary"],
            "total_chunks_processed": result["total_chunks_processed"],
            "batches_processed": result["batches_processed"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))