from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id, languages=None):
    if languages is None:
        languages = ["en", "hi"]

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    try:
        transcript = transcript_list.find_transcript(languages)
    except Exception:
        transcript = transcript_list.find_generated_transcript(languages)

    transcript = transcript.fetch()

    results = []

    for item in transcript:
        results.append({
            "text": item.text,
            "start": item.start,
            "duration": item.duration
        })

    return results