from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Claims Orchestrator"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    MODEL_PATH: str = "app/models/fraud_model.joblib"
    UPLOAD_DIR: str = "app/uploads"

    class Config:
        env_file = ".env"

settings = Settings()
