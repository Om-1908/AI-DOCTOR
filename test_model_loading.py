import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Set environment variable to simulate Hugging Face Space
os.environ["IS_HF_SPACE"] = "true"

# Import the model service after setting up the environment
from backend.app.services.model_service import ModelService

try:
    print("=== Testing Model Loading ===")
    
    # Initialize the model service
    print("Initializing ModelService...")
    model_service = ModelService()
    
    # Test prediction with sample symptoms
    print("\nTesting prediction...")
    sample_symptoms = ["fever", "headache", "nausea"]
    prediction = model_service.predict(sample_symptoms)
    
    print("\nPrediction successful!")
    print(f"Predicted disease: {prediction['disease']}")
    print(f"Confidence: {prediction['confidence']:.2f}%")
    
    # Test getting disease info
    print("\nTesting disease info...")
    disease_info = model_service.get_disease_info(prediction['disease'])
    print(f"Description: {disease_info['description']}")
    print(f"Precautions: {disease_info['precautions']}")
    
    print("\n=== All tests passed successfully! ===")
    
except Exception as e:
    print(f"\n!!! Error during testing: {str(e)}")
    import traceback
    traceback.print_exc()
