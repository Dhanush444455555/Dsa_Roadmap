import os
import logging
from typing import Optional, Any
from app.config import settings

logger = logging.getLogger(__name__)

def get_llm():
    """
    Returns an initialized LLM based on configuration (Gemini / OpenAI / Ollama).
    Falls back gracefully if keys are missing.
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "gemini" and settings.GEMINI_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.2
            )
        except Exception as e:
            logger.warning(f"Could not initialize ChatGoogleGenerativeAI: {e}")

    elif provider == "openai" and settings.OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=settings.OPENAI_API_KEY,
                temperature=0.2
            )
        except Exception as e:
            logger.warning(f"Could not initialize ChatOpenAI: {e}")

    elif provider == "ollama":
        try:
            from langchain_community.chat_models import ChatOllama
            return ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model="llama3",
                temperature=0.2
            )
        except Exception as e:
            logger.warning(f"Could not initialize ChatOllama: {e}")

    return None
