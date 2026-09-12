# Video RAG Summarizer

A Python-based Video Retrieval-Augmented Generation (RAG) project that retrieves timestamped YouTube transcripts and prepares them for structured summarization through a FastAPI service and a custom GPT.

## Project Goal

The goal of this project is to allow a user to submit one or more YouTube URLs and receive transcript-grounded summaries.

Each video will be processed separately.

Planned output for each video includes:

* A 3–5 sentence summary based only on the transcript
* Key takeaways
* Relevant timestamps for each takeaway
* Clear error handling when transcripts are unavailable or cannot be retrieved

## Current Functionality

The project currently supports:

* YouTube URL parsing
* YouTube video ID extraction
* Timestamped transcript retrieval
* Transcript language detection
* Identification of generated captions
* Human-readable timestamp formatting
* Separation of transcript-unavailable errors from transcript-retrieval errors

## Current Architecture

```text
YouTube URL
    |
    v
transcript_service.py
    |
    +-- Validate URL
    +-- Extract video ID
    +-- Retrieve transcript
    +-- Preserve timestamps
    +-- Classify transcript errors
    |
    v
FastAPI Service
    |
    v
Custom GPT / LLM
    |
    +-- 3–5 sentence transcript-only summary
    +-- Key takeaways
    +-- Timestamp references
```

## Technology Stack

* Python 3.13
* FastAPI
* Uvicorn
* youtube-transcript-api
* Git
* GitHub
* Visual Studio Code

## Project Structure

```text
You Tube Video Summarizer/
|
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- transcript_service.py
|
`-- .venv/                 # Local virtual environment, excluded from Git
```

## Setup

Clone the repository:

```powershell
git clone <repository-url>
cd "You Tube Video Summarizer"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Transcript Service

From the project root:

```powershell
python transcript_service.py
```

The application will prompt for a YouTube URL:

```text
Enter a YouTube URL:
```

If a transcript is available, the service returns information such as:

```text
Video ID: example12345
Language: English
Generated captions: True

Transcript:
------------------------------------------------------------
[00:00] Example transcript text...
[00:05] Additional transcript text...
```

## Error Handling

The transcript service distinguishes between two major failure types.

### Transcript Not Available

Used when:

* Captions are disabled
* No matching transcript exists
* The video is unavailable

### Transcript Retrieval Error

Used when:

* YouTube blocks the request
* The request encounters an access error
* The video is age restricted
* YouTube returns an unexpected response
* Transcript data cannot be parsed

This distinction will allow the FastAPI service to provide more useful API responses.

## Planned Development

The next phases of the project include:

1. Create a FastAPI application
2. Add a `POST /transcript` endpoint
3. Accept YouTube URLs through JSON requests
4. Support multiple video URLs
5. Return structured JSON transcript data
6. Add automated tests
7. Connect the service to a custom GPT
8. Generate transcript-only summaries
9. Generate timestamped key takeaways
10. Prepare the application for deployment

## Summarization Requirements

The eventual GPT integration will follow these rules:

* Use only information contained in the retrieved transcript
* Do not introduce external facts
* Produce a 3–5 sentence summary
* Provide key takeaways
* Include timestamps where relevant
* Summarize multiple videos independently rather than combining their transcripts

## Development Status

**Current milestone:** Transcript retrieval service complete.

**Next milestone:** FastAPI transcript endpoint.

## Author

Developed as an academic software project demonstrating Python API development, transcript retrieval, retrieval-augmented generation, and LLM integration.
