from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({"error": "Video ID is required"}), 400
    
    try:
        # Try manual English captions first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return jsonify({"captions": " ".join([item['text'] for item in transcript])})
    
    except (TranscriptsDisabled, NoTranscriptFound):
        # Try manual captions in any other language
        try:
            transcript = YouTubeTranscriptApi.list_transcripts(video_id)
            for lang in transcript:
                if lang.is_translatable:
                    fetched_transcript = lang.translate('en').fetch()
                    return jsonify({"captions": " ".join([item['text'] for item in fetched_transcript])})
        
        except (TranscriptsDisabled, NoTranscriptFound):
            # Try auto-generated English captions
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], is_generated=True)
                return jsonify({"captions": " ".join([item['text'] for item in transcript])})
            
            except (TranscriptsDisabled, NoTranscriptFound):
                # Try auto-generated captions in any language
                try:
                    transcript = YouTubeTranscriptApi.list_transcripts(video_id)
                    fetched_transcript = transcript.find_generated_transcript(['en'])
                    return jsonify({"captions": " ".join([item['text'] for item in fetched_transcript])})
                except (TranscriptsDisabled, NoTranscriptFound):
                    return jsonify({"error": f"Could not retrieve a transcript for the video https://www.youtube.com/watch?v={video_id}!"}), 404

    return jsonify({"error": f"Could not retrieve a transcript for the video https://www.youtube.com/watch?v={video_id}!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
