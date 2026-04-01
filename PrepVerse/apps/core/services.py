import google.generativeai as genai
import requests
from django.conf import settings
import json

def get_study_material_and_mcqs(topic):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""
    Topic: {topic}
    Level: Intermediate
    
    1. Generate a brief study material (approx 200 words).
    2. Generate 30 Multiple Choice Questions (MCQs).
    Each MCQ must have:
    - Question
    - 4 options (Labeled A, B, C, D)
    - Correct answer (e.g., 'A')
    - Short explanation
    
    Output the result in EXACT JSON format with these exact keys:
    {{
      "study_material": "...",
      "mcqs": [
        {{
          "question": "...",
          "options": ["...", "...", "...", "..."],
          "correct_answer": "...",
          "explanation": "..."
        }},
        ...
      ]
    }}
    Ensure all 30 MCQs are generated and do not include any other text except the JSON.
    """
    
    response = model.generate_content(prompt)
    try:
        # If response has backticks, strip them
        content = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return None

def get_youtube_videos(topic):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': topic,
        'key': settings.YOUTUBE_API_KEY,
        'maxResults': 3,
        'type': 'video'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        videos = []
        for item in data.get('items', []):
            videos.append({
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            })
        return videos
    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return []
