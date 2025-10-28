from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Determine the environment
IS_HF_SPACE = os.environ.get('SPACE_ID') is not None
IS_CONTAINER = os.environ.get('DOCKER_CONTAINER', 'false').lower() == 'true' or IS_HF_SPACE

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Doctor API"
    
    # Base directory - points to the project root
    if IS_HF_SPACE:
        BASE_DIR: Path = Path("/home/user/app")  # Hugging Face Spaces path
    elif IS_CONTAINER:
        BASE_DIR: Path = Path("/app")  # Container path
    else:
        BASE_DIR: Path = Path(__file__).parent.parent.parent.parent  # Local dev path
    
    # Model path
    MODEL_DIR: Path = BASE_DIR / "Models"
    MODEL_PATH: str = str(MODEL_DIR / "svc.pkl")
    
    # Data file paths
    if IS_CONTAINER:
        DATA_DIR: Path = Path("/app/Data.csv")  # Container path
    else:
        DATA_DIR: Path = BASE_DIR / "Data.csv"  # Local dev path
        
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