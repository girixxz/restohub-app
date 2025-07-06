import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'restohub-secret-key-2024'
    MONGODB_URI = os.getenv('MONGODB_URI')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
