import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    SECRET_KEY = 'restohub-secret-key-2024'
    
    # MongoDB URI diambil dari environment
    MONGODB_URI = os.getenv('MONGODB_URI')
    
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
