from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from transcript_service import (
    get_transcript,
    InvalidYouTubeURLError,
    TranscriptNotAvailableError,
    TranscriptRetrievalError,
)

app = FastAPI(
    title="Video RAG Summarizer API",
    description="Retrieves timestamped YouTube transcripts for downstream summarization.",
    version="0.1.0",
)


class TranscriptRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {
        "message": "Video RAG Summarizer API is running."
    }


@app.post("/transcript")
def retrieve_transcript(request: TranscriptRequest):
    try:
        return get_transcript(request.url)

    except InvalidYouTubeURLError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except TranscriptNotAvailableError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except TranscriptRetrievalError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc