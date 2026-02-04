from groq import Groq
from constants import GROQ_MODEL
from llm.base import BaseLLM


class GroqLLM(BaseLLM):

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
