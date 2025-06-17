"""Configuration settings for the Langflow Chat application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_URL = os.getenv(
    "LANGFLOW_API_URL",
    "http://127.0.0.1:7860/api/v1/run/d2728a04-3aaa-49d2-998f-f1a8d22d7d8c"
)
HEADERS = {
    "Content-Type": "application/json"
}

# Application Settings
DEFAULT_SESSION_ID = "default_session"
MAX_CHAT_HISTORY = 20  # Maximum number of messages to keep in chat history
