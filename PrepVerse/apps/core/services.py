import google.generativeai as genai
import requests
from django.conf import settings
import json

def get_study_material_and_mcqs(topic):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    is_exam = "exam" in topic.lower()
    
    educational_check = f"""
    THE USER TOPIC IS: {topic}
    STRICT RULE: This application is for EDUCATIONAL PURPOSES ONLY. 
    1. If the topic is sexual, adult, or non-educational content, DO NOT generate the study material. Instead, return JSON with "error": "This content is not allowed."
    2. Ensure the content is safe and professional.
    """
    
    prompt = f"""
    {educational_check}
    Topic: {topic}
    Level: Intermediate
    
    1. Generate a brief study material (approx 200 words).
    2. Generate 30 Multiple Choice Questions (MCQs).
    Each MCQ must have:
    - Question
    - 4 options (Labeled A, B, C, D)
    - Correct answer (e.g., 'A')
    - Short explanation
    
    {"3. If this is an exam (the topic contains 'exam'), provide: " if is_exam else ""}
    {"   - Exam pattern details." if is_exam else ""}
    {"   - 3 previous question papers (reference summaries) with answers." if is_exam else ""}
    {"   - Preparation guidance." if is_exam else ""}
    
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
      {', "exam_pattern": "...", "previous_papers": "...", "preparation_guidance": "..."' if is_exam else ""}
    }}
    Ensure all 30 MCQs are generated and do not include any other text except the JSON.
    """
    
    try:
        # Re-using the stable model name
        model = genai.GenerativeModel('gemini-3-flash-preview')
        response = model.generate_content(prompt)
        
        if not response.text:
            return None
            
        content = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        
        if "error" in data:
            return data
            
        return data
    except Exception as e:
        print(f"Error in Gemini service: {e}")
        return None

def get_youtube_videos(topic):
    url = "https://www.googleapis.com/youtube/v3/search"
    # Append educational keywords to the query
    educational_query = f"{topic} educational lecture tutorial study guide"
    params = {
        'part': 'snippet',
        'q': educational_query,
        'key': settings.YOUTUBE_API_KEY,
        'maxResults': 3,
        'type': 'video',
        'safeSearch': 'strict',  # Strict filtering for adult content
        'relevanceLanguage': 'en'
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
