import re
from youtube_transcript_api import YouTubeTranscriptApi



def transcript(url):
    pattern = r'(?<=\?v=)[\w-]+'
    match = re.search(pattern, url)
    if match:
        video_id = match.group(0)
        print(video_id)
    else:   
        print("Video ID not found in the URL.")
    

    txt = YouTubeTranscriptApi.get_transcript(video_id) #Returning the JSON file

    transcript_output = """ """

    
    for i in txt:
        transcript_output = transcript_output + str(i['text']) + " " #Only taking the text element from the JSON file
    
    print(transcript_output)

    return transcript_output

