import requests
import json
import sys

def test_generation():
    url = "http://localhost:8000/generate"
    
    # Example request payload
    payload = {
        "text": "Hello, this is a test of the DIA voice generation system.",
        "emotion": "happy",
        "tone": "friendly",
        "pace": 1.0
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("Success!")
        print(f"Generated audio path: {result['audio_path']}")
        print(f"Message: {result['message']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_generation() 