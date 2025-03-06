import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (Required for Hugging Face Inference API)
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")  # Required for authentication

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# CORS Settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Verify required environment variables
def verify_env_vars():
    required_vars = ["HUGGINGFACE_API_TOKEN"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("Some functionality may not work properly.")
        return False
    
    return True 