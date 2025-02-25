from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

class YouTubeDataFetcher:
    def __init__(self, api_key, video_id):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.video_id = video_id
    
    def get_video_details(self, video_id):
        try:
            response = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()
            
            if "items" in response and len(response["items"]) > 0:
                video = response["items"][0]
                return {
                    "Title": video["snippet"]["title"],
                    "Publish Date": video["snippet"]["publishedAt"],
                    "Description": video["snippet"]["description"],
                    "Tags": video["snippet"].get("tags", [])[:5],
                    "Views": video["statistics"].get("viewCount", "N/A"),
                    "Total Comments": video["statistics"].get("commentCount", "0")
                }
            return {"Error": "Video not found or access restricted"}
        except Exception as e:
            return {"Error": str(e)}
    
    def get_video_comments(self, video_id, max_results=100):
        try:
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=max_results
            ).execute()
            
            if "items" not in response or not response["items"]:
                return {"Message": "Comments are disabled or not available for this video."}
            
            comments = []
            for item in response["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "Author": snippet["authorDisplayName"],
                    "Comment": snippet["textDisplay"],
                    "Likes": int(snippet.get("likeCount", 0))
                })
            
            top_comments = sorted(comments, key=lambda x: x["Likes"], reverse=True)[:5]
            
            all_comments = [comment["Comment"] for comment in comments]
            
            return {
                "Top Comments": top_comments,
                "All Comments": all_comments
            }
        except HttpError as e:
            if e.resp.status == 403:
                return {"Error": "Comments are turned off for this video or restricted."}
            return {"Error": f"An HTTP error occurred: {e}"}
        except Exception as e:
            return {"Error": f"An unexpected error occurred: {str(e)}"}
        
    def extract_video_id(youtube_url):
        # Regular expression to match YouTube video URLs and extract the video ID
        pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.match(pattern, youtube_url)
        
        if match:
            return match.group(1)
        else:
            return None
        
    
    
    def fetch_youtube_data(self):


        # Fetch video details
        video_details = self.get_video_details(self.video_id)

        # Fetch video comments
        comments_data = self.get_video_comments(self.video_id)

        # Combine the data
        youtube_data = {**video_details, **comments_data}

        return youtube_data


# Example usage (to be called from another file)
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    video_id = "YOUR_VIDEO_ID"
    
    fetcher = YouTubeDataFetcher(api_key)
    video_details = fetcher.get_video_details(video_id)
    comments_data = fetcher.get_video_comments(video_id)
    
    youtube_data = {**video_details, **comments_data}
    print(youtube_data)
