from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id):
    transcript = None
    languages_to_try = ['en', 'hi']  # English and Hindi as fallback

    # Try fetching manual captions first
    for language in languages_to_try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            return transcript  # Return manual captions if available
        except (TranscriptsDisabled, NoTranscriptFound):
            print(f"No manual captions found in {language}. Trying next language...")

    # If manual captions are not available, fetch auto-generated captions
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # This will attempt auto-generated captions
        return transcript
    except Exception as e:
        print(f"Error fetching auto-generated captions: {e}")
        return None
