from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    VideoUnplayable,
    RequestBlocked,
    IpBlocked,
    YouTubeRequestFailed,
    InvalidVideoId,
    AgeRestricted,
    YouTubeDataUnparsable,
)


class TranscriptServiceError(Exception):
    """Base exception for transcript service errors."""


class TranscriptNotAvailableError(TranscriptServiceError):
    """Raised when a video exists but no usable transcript is available."""


class TranscriptRetrievalError(TranscriptServiceError):
    """Raised when a transcript may exist but could not be retrieved."""


class InvalidYouTubeURLError(TranscriptServiceError):
    """Raised when a valid YouTube video ID cannot be extracted."""


def extract_video_id(url: str) -> str:
    """
    Extract a YouTube video ID from common YouTube URL formats.

    Supported examples:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """

    if not url or not isinstance(url, str):
        raise InvalidYouTubeURLError("A YouTube URL is required.")

    url = url.strip()

    parsed = urlparse(url)

    hostname = (parsed.hostname or "").lower()

    video_id = None

    # Standard youtube.com URLs
    if hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            query = parse_qs(parsed.query)
            video_id = query.get("v", [None])[0]

        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/")[0]

        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/")[0]

    # Short youtu.be URLs
    elif hostname == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0]

    if not video_id or len(video_id) != 11:
        raise InvalidYouTubeURLError(
            "Could not determine a valid YouTube video ID from the URL."
        )

    return video_id


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS or MM:SS format.
    """

    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours:
        return f"{hours:02}:{minutes:02}:{secs:02}"

    return f"{minutes:02}:{secs:02}"


def get_transcript(url: str) -> dict:
    """
    Retrieve a timestamped transcript from a YouTube URL.

    Returns:
        {
            "video_id": "...",
            "language": "English",
            "language_code": "en",
            "is_generated": True,
            "segments": [
                {
                    "start": 12.3,
                    "duration": 4.2,
                    "timestamp": "00:12",
                    "text": "..."
                }
            ],
            "full_text": "[00:12] ...\\n..."
        }
    """

    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=["en"],
        )

        segments = []

        for snippet in transcript:
            segment = {
                "start": snippet.start,
                "duration": snippet.duration,
                "timestamp": format_timestamp(snippet.start),
                "text": snippet.text.strip(),
            }

            segments.append(segment)

        full_text = "\n".join(
            f"[{segment['timestamp']}] {segment['text']}"
            for segment in segments
        )

        return {
            "video_id": video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "segments": segments,
            "full_text": full_text,
        }

    # The video has no transcripts/captions available.
    except (TranscriptsDisabled, NoTranscriptFound) as exc:
        raise TranscriptNotAvailableError(
            "No transcript is available for this video."
        ) from exc

    # The supplied URL/video itself is invalid or unavailable.
    except (InvalidVideoId, VideoUnavailable, VideoUnplayable) as exc:
        raise TranscriptNotAvailableError(
            "The YouTube video is unavailable or cannot be accessed."
        ) from exc

    # Age restriction is technically an access issue.
    except AgeRestricted as exc:
        raise TranscriptRetrievalError(
            "The transcript could not be retrieved because the video is age restricted."
        ) from exc

    # YouTube may block automated transcript requests.
    except (RequestBlocked, IpBlocked) as exc:
        raise TranscriptRetrievalError(
            "YouTube blocked the transcript request. "
            "The transcript may exist, but it could not be retrieved."
        ) from exc

    # Network, HTTP, or parsing problems.
    except (YouTubeRequestFailed, YouTubeDataUnparsable) as exc:
        raise TranscriptRetrievalError(
            "The transcript could not be retrieved because of a YouTube "
            "access or response error."
        ) from exc

    except Exception as exc:
        raise TranscriptRetrievalError(
            f"An unexpected transcript retrieval error occurred: {exc}"
        ) from exc


if __name__ == "__main__":
    test_url = input("Enter a YouTube URL: ").strip()

    try:
        result = get_transcript(test_url)

        print()
        print(f"Video ID: {result['video_id']}")
        print(f"Language: {result['language']}")
        print(f"Generated captions: {result['is_generated']}")
        print()
        print("Transcript:")
        print("-" * 60)
        print(result["full_text"])

    except TranscriptServiceError as exc:
        print(f"ERROR: {exc}")