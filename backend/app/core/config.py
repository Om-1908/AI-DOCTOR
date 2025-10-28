from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Doctor API"
    
    # Base directory - points to the project root
    BASE_DIR: Path = Path(__file__).parent.parent.parent.parent  # Updated to point to project root
    
    # Model path - points to Models directory in the root
    MODEL_PATH: str = str(BASE_DIR / "Models" / "svc.pkl")
    
    # Data file paths - points to Data.csv directory in the root
    DATA_DIR: Path = BASE_DIR / "Data.csv"
    SYMPTOMS_CSV_PATH: str = str(DATA_DIR / "symptoms_df.csv")
    PRECAUTIONS_CSV_PATH: str = str(DATA_DIR / "Precautions_df.csv")
    WORKOUT_CSV_PATH: str = str(DATA_DIR / "workout_df.csv")
    DESCRIPTION_CSV_PATH: str = str(DATA_DIR / "Description.csv")
    MEDICATIONS_CSV_PATH: str = str(DATA_DIR / "Medications.csv")
    DIETS_CSV_PATH: str = str(DATA_DIR / "Diets.csv")
    TRAINING_CSV_PATH: str = str(DATA_DIR / "training.csv")
    SYMPTOM_SEVERITY_CSV_PATH: str = str(DATA_DIR / "Symptom_Severity.csv")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()