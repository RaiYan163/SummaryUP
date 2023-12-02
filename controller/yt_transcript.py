import re
from youtube_transcript_api import YouTubeTranscriptApi

random = "Hello"


def get_video_id(url):
    pattern = r'(?<=\?v=)[\w-]+'
    match = re.search(pattern, url)
    if match:
        return match.group(0)
    else:
        return None


def transcript(url):
    video_id = get_video_id(url)

    if video_id:
        try:
            txt = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_output = " ".join([i['text'] for i in txt])
            return {'transcript': transcript_output}
        except Exception as e:
            return {'error': f"Failed to fetch transcript: {str(e)}"}, 500
    else:
        return {'error': 'Video ID not found in the URL'}, 400
