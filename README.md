# VIDSENTIMENT  
**Sentiment Analysis of Video Comments**  

## 📌 Overview  
VIDSENTIMENT is a web-based application that performs sentiment analysis on YouTube video comments. The project leverages machine learning models to classify sentiments and visualize results for better audience insights.  

## 🚀 Features  
- **Sentiment Classification**: Achieved over **85% accuracy** in classifying sentiments (positive, neutral, negative).  
- **YouTube API Integration**: Fetches video metadata (title, description, channel name, likes, views) and comments using the YouTube API.  
- **FastAPI Backend**: Provides a scalable and fast API to serve predictions.  
- **Web Interface**: Developed using **HTML, CSS, and JavaScript** for user-friendly interaction.  
- **Visualization**: Implements graphical bar charts to display sentiment distribution.  
- **GPT-2 Model**: Uses a **123M parameter GPT-2 model** for sentiment classification.  

## 🛠️ Tech Stack  
- **Machine Learning**: TensorFlow  
- **Backend**: FastAPI  
- **Frontend**: HTML, CSS, JavaScript  
- **Cloud Deployment**: AWS EC2  
- **Visualization**: Matplotlib, Seaborn  

## 📂 Project Structure  
```
VIDSENTIMENT/
│── backend/
│   ├── models/
│   │   ├── Model/
│   │   │   ├── GPT_2.py
│   │   ├── Model Weights/
│   │   │   ├── model_and_optimizer_youtube...
│   ├── routes/
│── frontend/
│   ├── css/
│   │   ├── style.css
│   ├── js/
│   │   ├── script.js
│   ├── index.html
│── scripts/
│   ├── pre_processes.py
│   ├── youtube_data_fetcher.py
│── main.py
│── README.md
│── requirements.txt
```

## 🔧 Setup Instructions  

### 1️⃣ Prerequisites  
- Python 3.8+  
- Google Cloud Console API Key (for YouTube API access)  

### 2️⃣ Installation  
Clone the repository and install dependencies:  
```bash
git clone https://github.com/your-repo/Vidsentiment.git  
cd Vidsentiment  
pip install -r requirements.txt  
```

### 3️⃣ Configure API Key  
- Get a YouTube API key from [Google Cloud Console](https://console.cloud.google.com/)  
- Paste your API key in:  
  ```
  scripts/pre_processes.py
  ```

### 4️⃣ Run the Application  
Start the FastAPI backend:  
```bash
uvicorn main:app --reload
```

Access the web interface at: `http://127.0.0.1:8000/`  

## 📊 Impact  
- Helps **content creators** and **marketing teams** understand audience sentiment.  
- Improves **engagement strategies** and **data-driven decision-making**.  

---

📌 **Contributors**: Gold Sharon  
📌 **License**: MIT  
📌 **Contact**: gold33sharon@gmail.com  


