import re
import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi


API_KEY = 'AIzaSyCRrUH1fq8UWjXMsLvu-F_brL8MvW0qSxs' 
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def has_subtitles(video_id):
    """Check if the video has subtitles available using YouTube Data API."""
    try:
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            caption_available = video['snippet'].get('captions', 'none') == 'true'
            return caption_available
        return False
    except googleapiclient.errors.HttpError as e:
        print(f"Error checking subtitles for {video_id}: {e}")
        return False

def get_transcript(video_id):
    """Fetch transcript for a given YouTube video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None

def find_keywords_in_transcript(transcript, keywords):
    """Check if any keyword is present in the transcript."""
    transcript_lower = transcript.lower()
    return any(keyword.lower() in transcript_lower for keyword in keywords)

def main():
    video_links = [

    ]
    
    keywords = ["worst advice", "best advice", "advice"]
    matching_videos = []

    for link in video_links:
        video_id = extract_video_id(link)
        if video_id:
            # First check if subtitles are available
            if has_subtitles(video_id):
                transcript = get_transcript(video_id)
                if transcript and find_keywords_in_transcript(transcript, keywords):
                    matching_videos.append(link)
    
    print("Videos containing keywords:")
    for video in matching_videos:
        print(video)

if __name__ == "__main__":
    main()
