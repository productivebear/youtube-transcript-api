from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/get_captions', methods=['GET'])
def get_captions():
    video_id = request.args.get('video_id')
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({"captions": transcript}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
