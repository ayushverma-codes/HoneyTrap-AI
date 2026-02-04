import requests
from constants import OLLAMA_MODEL
from llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(self, host="http://localhost:11434"):
        self.host = host

    def generate(self, prompt: str) -> str:

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(f"{self.host}/api/generate", json=payload)
        return r.json()["response"].strip()
