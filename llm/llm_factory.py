import os
from dotenv import load_dotenv

from constants import StrategyEngine_LLM, PersonaEngine_LLM, SUMMARIZER_LLM
# from llm.gemini import GeminiLLM
from llm.groq import GroqLLM
# from llm.ollama import OllamaLLM


# Load .env from project root
load_dotenv()

_LLM_CACHE = {}


def _create_llm(name):

    # if name == "gemini":
    #     api_key = os.getenv("GEMINI_API_KEY")
    #     return GeminiLLM(api_key)

    if name == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        return GroqLLM(api_key)

    # if name == "ollama":
    #     host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    #     return OllamaLLM(host)

    raise ValueError(f"Unknown LLM provider: {name}")


def get_llm(component="persona"):
    """
    component: strategy | persona | summarizer
    """

    if component == "strategy":
        key = StrategyEngine_LLM
    elif component == "persona":
        key = PersonaEngine_LLM
    elif component == "summarizer":
        key = SUMMARIZER_LLM
    else:
        raise ValueError("Unknown component")

    if key not in _LLM_CACHE:
        _LLM_CACHE[key] = _create_llm(key)

    return _LLM_CACHE[key]
