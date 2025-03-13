from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

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
    "https://www.youtube.com/watch?v=P91b4civBxA",
    "https://www.youtube.com/watch?v=iPUOQRpdOeQ",
    "https://www.youtube.com/watch?v=bY6JTLwkUzc",
    "https://www.youtube.com/watch?v=9EqrUK7ghho",
    "https://www.youtube.com/watch?v=strvdoGo_a0",
    "https://www.youtube.com/watch?v=avx4Ww9h3Tc",
    "https://www.youtube.com/watch?v=RAv8ysXZ0U4",
    "https://www.youtube.com/watch?v=siNNCI6JAjk",
    "https://www.youtube.com/watch?v=90bxNpimtb8",
    "https://www.youtube.com/watch?v=t2OeZcxVVI4",
    "https://www.youtube.com/watch?v=tl6_3tzjCNg",
    "https://www.youtube.com/watch?v=T30Ul9AiIfs",
    "https://www.youtube.com/watch?v=6ADogpDq0t4",
    "https://www.youtube.com/watch?v=AIFYrV3yivQ",
    "https://www.youtube.com/watch?v=FRP1q1Jj-7o",
    "https://www.youtube.com/watch?v=4M8eTJbVQmo",
    "https://www.youtube.com/watch?v=VvbjMMepKwE",
    "https://www.youtube.com/watch?v=vWCdkRo4xRE",
    "https://www.youtube.com/watch?v=-O9j0Hnw7NA",
    "https://www.youtube.com/watch?v=mDrVYkNn25E",
    "https://www.youtube.com/watch?v=q6O9mwYkLrM",
    "https://www.youtube.com/watch?v=v1EyY8mePcU",
    "https://www.youtube.com/watch?v=NgYjS4IseL4",
    "https://www.youtube.com/watch?v=X2vNGwMCw-M",
    "https://www.youtube.com/watch?v=OkgtwMxbnLw",
    "https://www.youtube.com/watch?v=43VoxYFHUas",
    "https://www.youtube.com/watch?v=6y1fcHUOHZI",
    "https://www.youtube.com/watch?v=cDkFzpe2VPg",
    "https://www.youtube.com/watch?v=g5GaBnavBrY",
    "https://www.youtube.com/watch?v=GXLZahgHz3s",
    "https://www.youtube.com/watch?v=QQGxI0dIO_g",
    "https://www.youtube.com/watch?v=ZAs-brQ56RQ",
    "https://www.youtube.com/watch?v=obpp0d6m7LU",
    "https://www.youtube.com/watch?v=60pHJXUjaJY",
    "https://www.youtube.com/watch?v=snGnDtf0LCo",
    "https://www.youtube.com/watch?v=uZQh9g1chJE",
    "https://www.youtube.com/watch?v=cEkkdwQxTm8",
    "https://www.youtube.com/watch?v=95-bJRsFDg4",
    "https://www.youtube.com/watch?v=QGozyflCDzo",
    "https://www.youtube.com/watch?v=-d1dvrj_fMk",
    "https://www.youtube.com/watch?v=S7IQOa19-eI",
    "https://www.youtube.com/watch?v=EUqBAcSDpL4",
    "https://www.youtube.com/watch?v=dGLbCOTkVnk",
    "https://www.youtube.com/watch?v=AOEOmRIJ1YE",
    "https://www.youtube.com/watch?v=LYm9NFU1ZAc",
    "https://www.youtube.com/watch?v=iaw8DwQ7YGo",
    "https://www.youtube.com/watch?v=sNXinv6NEgQ",
    "https://www.youtube.com/watch?v=lCiZ2G2GSY4&t=1949s",
    "https://www.youtube.com/watch?v=M4PzOjM5BJQ",
    "https://www.youtube.com/watch?v=SBYvuAtaUtA",
    "https://www.youtube.com/watch?v=NEKHOzrasdg",
    "https://www.youtube.com/watch?v=lCiZ2G2GSY4",
    "https://www.youtube.com/watch?v=0setn-FtDs8",
    "https://www.youtube.com/watch?v=dDtFVpudkNk",
    "https://www.youtube.com/watch?v=dGLbCOTkVnk&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=YB8ma6fmb1A&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=Cw6xuzosn4s",
    "https://www.youtube.com/watch?v=0SPC_Q7-k40&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=jSqCL7Npln0&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=Eu1kHIztT24&t=2249s&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=SJKr7BPOXY0&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=g2cQ2kD6lzs&t=3s&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
    "https://www.youtube.com/watch?v=kbKldiDOgEE&pp=ygUZcG9kY2FzdCBtb3RpdmF0aW9uIGFkdmljZQ%3D%3D",
]



    
    keywords = ["worst advice", "best advice","advice"]
    matching_videos = []
    
    for link in video_links:
        video_id = extract_video_id(link)
        if video_id:
            transcript = get_transcript(video_id)
            if transcript and find_keywords_in_transcript(transcript, keywords):
                matching_videos.append(link)
    
    print("Videos containing keywords:")
    for video in matching_videos:
        print(video)

if __name__ == "__main__":
    main()
