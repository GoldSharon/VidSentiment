from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import torch
import warnings
import tiktoken
from scripts.youtube_data_fetcher import YouTubeDataFetcher
from scripts.pre_processes import Utility as ut
from backend.models.Model.GPT_2 import GPTModel, GPT_CONFIG_124M

warnings.filterwarnings('ignore')

# Initialize FastAPI app
app = FastAPI()
tokenizer = tiktoken.get_encoding("gpt2")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and tokenizer
API_KEY = ut.get_api_key()
device = "cpu"

# Load the GPT Model
try:
    gpt = GPTModel(GPT_CONFIG_124M)
    gpt.eval()
    optimizer = torch.optim.Adam(gpt.parameters(), lr=0.0004, weight_decay=0.1)

    # Load model weights (ensure the path is correct)
    checkpoint_path = "backend/models/Model Weights/model_and_optimizer_youtubes_senti.pth"
    checkpoint = torch.load(checkpoint_path, map_location=device)
    gpt.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
except Exception as e:
    print(f"❌ Error loading model: {e}")
    gpt = None

# Define the VideoLink model for API request
class VideoLink(BaseModel):
    link: str

@app.get("/")
def home():
    """Health check endpoint"""
    return {"message": "YouTube Sentiment Analysis API is running!"}

@app.post("/analyze_comments/")
def analyze_comments(video: VideoLink):
    """Analyze sentiment of comments for a given YouTube video"""
    if gpt is None:
        return {"error": "Model not loaded properly"}

    try:
        # Extract video ID from the YouTube link
        video_id = ut.extract_video_id(video.link)

        # Fetch YouTube data
        fetcher = YouTubeDataFetcher(api_key=API_KEY, video_id=video_id)
        data = fetcher.fetch_youtube_data()

        # Extract video details
        title = data.get("Title", "Unknown")
        publish_date = data.get("Publish Date", "Unknown")
        views = data.get("Views", "Unknown")
        top_comments = data.get("Top Comments", [])
        total_comments = len(data.get("All Comments", []))

        # Analyze sentiment of comments
        sentiment_counts = ut.analyze_sentiments_all_comments(data=data, model=gpt, device=device,tokenizer=tokenizer)

        return {
            "video_id": video_id,
            "title": title,
            "publish_date": publish_date,
            "views": views,
            "total_comments": total_comments,
            "top_comments": top_comments,
            "sentiment_counts": sentiment_counts
        }
    except Exception as e:
        return {"error": str(e)}
