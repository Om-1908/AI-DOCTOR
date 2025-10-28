import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from backend.app.core.config import settings

def test_paths():
    print("Testing file paths...\n")
    
    # Check model file
    model_path = Path(settings.MODEL_PATH)
    print(f"Model path: {model_path}")
    print(f"Model exists: {model_path.exists()}")
    if not model_path.exists():
        print("  Looking for model file in alternative locations...")
        alt_path = Path(__file__).parent / "Models" / "svc.pkl"
        print(f"  Trying: {alt_path}")
        print(f"  Exists: {alt_path.exists()}\n")
    else:
        print()
    
    # Check data files
    data_files = {
        "Symptoms": settings.SYMPTOMS_CSV_PATH,
        "Precautions": settings.PRECAUTIONS_CSV_PATH,
        "Workout": settings.WORKOUT_CSV_PATH,
        "Description": settings.DESCRIPTION_CSV_PATH,
        "Medications": settings.MEDICATIONS_CSV_PATH,
        "Diets": settings.DIETS_CSV_PATH,
        "Training": settings.TRAINING_CSV_PATH,
        "Symptom Severity": settings.SYMPTOM_SEVERITY_CSV_PATH
    }
    
    for name, path in data_files.items():
        file_path = Path(path)
        print(f"{name} path: {file_path}")
        print(f"{name} exists: {file_path.exists()}")
        if not file_path.exists():
            # Try alternative path structure
            alt_path = Path(__file__).parent / "Data.csv" / Path(path).name
            print(f"  Trying alternative: {alt_path}")
            print(f"  Exists: {alt_path.exists()}")
        print()

if __name__ == "__main__":
    test_paths()
