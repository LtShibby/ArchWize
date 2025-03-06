import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (Optional - Hugging Face Inference API has a free tier)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Optional for higher rate limits

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# CORS Settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Verify required environment variables
def verify_env_vars():
    # None are strictly required since we're using the free tier of Hugging Face
    return True 