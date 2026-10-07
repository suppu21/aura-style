import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def analyze_dress_and_suggest_outfit(uploaded_file, occasion="General Casual/Festive"):
    base64_image = encode_image(uploaded_file)
    
    prompt = f"""
    You are an expert fashion stylist. Analyze this dress image and the occasion: {occasion}.
    Provide a structured styling guide in Markdown. 
    At the very bottom of your response, on a new line, provide exactly 3 comma-separated image search keywords for matching footwear, jewelry, and accessories (e.g., "traditional juttis, gold necklace, designer handbag").
    """
    
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
        temperature=0.7,
        max_tokens=1024
    )
    content = response.choices[0].message.content
    return content

def get_text_styling_advice(user_prompt, occasion="General Casual/Festive"):
    prompt = f"""
    You are an expert fashion stylist. The user wants styling advice for: "{user_prompt}" for the occasion: {occasion}.
    Provide a comprehensive styling guide in Markdown.
    At the very bottom of your response, on a new line, provide exactly 3 comma-separated image search keywords for visual inspiration (e.g., "ethnic wear, silver jewelry, high heels").
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a professional fashion stylist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content