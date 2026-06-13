import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def query_llm(prompt, model="llama3"):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"LLM Error: {response.text}")