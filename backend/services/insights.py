import requests
from ..config import settings

def generate_insights(temporal_data, tag_data, sentiment_data, lifespan_data):
    """Generate insights based on various analyses."""
    prompt_template = f"""
    Analyze the following engagement data:
    - Temporal Patterns: {temporal_data}
    - Tag Co-occurrence: {tag_data}
    - Sentiment Impact: {sentiment_data}
    - Post Lifespan: {lifespan_data}

    Provide insights and actionable recommendations for improving engagement.
    Focus on patterns and trends that are relevant for content optimization.
    """

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt_template}]
        }]
    }
    url = f"{settings.GEMINI_API_ENDPOINT}?key={settings.GEMINI_API_KEY}"

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    print("Gemini Response:", result)
    return result.get("candidates", [{}])[0].get("content", [{}]).get("parts", [{}])[0].get("text", "No insights generated.")