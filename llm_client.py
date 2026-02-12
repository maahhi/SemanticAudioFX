import os
import requests
import json

def get_api_key():
    """Retrieves the Groq API key from environment variables."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it to use the tool.")
    return api_key

def query_llama(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Sends a prompt to the Groq API and returns the response content.
    
    Args:
        prompt: The full prompt string to send.
        model: The model identifier (default: llama-3.3-70b-versatile).
        
    Returns:
        The content of the model's response.
    """
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": model,
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False,
        "stop": None
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
    result = response.json()
    return result["choices"][0]["message"]["content"]
