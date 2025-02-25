import re
import torch
from collections import defaultdict

class Utility:
    
    api_key = "Pate your API key here"
    
    @staticmethod
    def extract_video_id(youtube_url):
        pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.match(pattern, youtube_url)
        
        if match:
            return match.group(1)
        else:
            return None
        
    @staticmethod
    def print_video_data(data):
        """Formats and prints YouTube video details and comments."""

        print("\n--- YouTube Video Data ---\n")
        
        print('Title:', data.get('Title', 'N/A'))
        print('Publish Date:', data.get('Publish Date', 'N/A'))
        
        print('\nTags:')
        if data.get('Tags'):
            for idx, tag in enumerate(data['Tags']):
                print(f"  {idx+1}. {tag}")
        else:
            print("  No tags available")

        print('\nViews:', data.get('Views', 'N/A'))
        print('Total Comments:', data.get('Total Comments', 'N/A'))
        print("\n--- Top Comments ---\n")

        if 'Top Comments' in data and data['Top Comments']:
            for idx, comment in enumerate(data['Top Comments']):
                print(f"{idx+1}. {comment['Author']} - {comment['Comment']}")
                print(f"   Likes: {comment['Likes']}\n")
        else:
            print("No top comments available\n")

        print("\n--- All Comments ---\n")
        
        if 'All Comments' in data and data['All Comments']:
            for idx, comment in enumerate(data['All Comments']):
                print(f"{idx+1}. {comment}")
        else:
            print("No comments available.")
        
    
    @staticmethod 
    def classify_sentiment(text, model, tokenizer, device, max_length=None, pad_token_id=50256):
        model.eval()

        # Prepare inputs to the model
        input_ids = tokenizer.encode(text)
        supported_context_length = model.pos_emb.weight.shape[0]
        # Note: In the book, this was originally written as pos_emb.weight.shape[1] by mistake
        # It didn't break the code but would have caused unnecessary truncation (to 768 instead of 1024)

        # Truncate sequences if they too long
        input_ids = input_ids[:min(max_length, supported_context_length)]

        # Pad sequences to the longest sequence
        input_ids += [pad_token_id] * (max_length - len(input_ids))
        input_tensor = torch.tensor(input_ids, device=device).unsqueeze(0) # add batch dimension

        # Model inference
        with torch.no_grad():
            logits = model(input_tensor)[:, -1, :]  # Logits of the last output token
        predicted_label = torch.argmax(logits, dim=-1).item()

        # Return the classified result
        return "Positive" if predicted_label == 1 else "Neutral" if predicted_label == 2 else "Negative"
    
    @staticmethod
    def analyze_sentiments_all_comments(data, model, tokenizer, device, max_length=256, pad_token_id=50256):
        
        total_comments =0
        sentiment_counts = {}
        sentiment_counts["Positive"] = 0
        sentiment_counts["Neutral"] = 0
        sentiment_counts["Negative"] = 0
        
        for comments in data['All Comments']:
            
            sentiment = Utility.classify_sentiment(comments,model,tokenizer,device,max_length=max_length)
            sentiment_counts[sentiment]+=1
            
        return sentiment_counts
    
    @staticmethod
    def get_api_key():
        return Utility.api_key
            
            
            