import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MediProof"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mediproof_super_secret_key_314159")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Model Settings
    RESNET_MODEL_PATH: str = "models/resnet50_weights.h5"
    COLLATZ_SEED: int = 123
    
    # Storage
    UPLOAD_DIR: str = "data/uploads"
    RESULT_DIR: str = "data/results"
    
    # Blockchain
    BLOCKCHAIN_JSON_DB: str = "data/blockchain_ledger.json"

    class Config:
        case_sensitive = True

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULT_DIR, exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)
