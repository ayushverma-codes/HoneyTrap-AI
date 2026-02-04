import google.generativeai as genai
from constants import GEMINI_MODEL
from llm.base import BaseLLM


class GeminiLLM(BaseLLM):

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
