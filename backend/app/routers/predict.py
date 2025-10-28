from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ..services.model_service import ModelService

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)

# Initialize model service
model_service = ModelService()

class SymptomInput(BaseModel):
    symptoms: List[str]

class DiseasePredictionResponse(BaseModel):
    prediction: str
    details: Dict[str, Any]

class SymptomListResponse(BaseModel):
    symptoms: List[Dict[str, Any]]

class DiseaseListResponse(BaseModel):
    diseases: List[Dict[str, Any]]

class DiseaseInfoResponse(BaseModel):
    disease: str
    description: str
    precautions: List[str]
    medications: List[str]
    diets: List[str]
    workouts: List[str]

class SymptomSeverityResponse(BaseModel):
    symptom: str
    weight: int
    description: str

@router.post("/", response_model=DiseasePredictionResponse)
async def predict_disease(symptom_input: SymptomInput) -> Dict[str, Any]:
    """
    Predict disease based on symptoms
    
    - **symptoms**: List of symptoms to predict the disease
    
    Example request body:
    ```json
    {
        "symptoms": ["fever", "headache", "nausea"]
    }
    ```
    """
    try:
        return model_service.predict_disease(symptom_input.symptoms)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/symptoms", response_model=SymptomListResponse)
async def get_symptoms() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get list of all available symptoms with their IDs
    
    Returns a list of symptoms in the format:
    ```json
    {
        "symptoms": [
            {"id": 0, "name": "symptom1"},
            {"id": 1, "name": "symptom2"}
        ]
    }
    ```
    """
    try:
        return {"symptoms": model_service.get_available_symptoms()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch symptoms: {str(e)}"
        )

@router.get("/diseases", response_model=DiseaseListResponse)
async def get_diseases() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get list of all available diseases with their IDs
    
    Returns a list of diseases in the format:
    ```json
    {
        "diseases": [
            {"id": 0, "name": "Disease 1"},
            {"id": 1, "name": "Disease 2"}
        ]
    }
    ```
    """
    try:
        return {"diseases": model_service.get_available_diseases()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch diseases: {str(e)}"
        )

@router.get("/disease/{disease_name}", response_model=DiseaseInfoResponse)
async def get_disease_info(disease_name: str):
    """
    Get detailed information about a specific disease
    
    - **disease_name**: Name of the disease to get information about
    
    Returns disease information including description, precautions, medications, diets, and workouts.
    """
    try:
        return model_service.get_disease_info(disease_name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch disease info: {str(e)}"
        )

@router.get("/symptom/severity/{symptom}", response_model=SymptomSeverityResponse)
async def get_symptom_severity(symptom: str):
    """
    Get severity information for a specific symptom
    
    - **symptom**: Name of the symptom to get severity for
    
    Returns the weight and description of the symptom's severity.
    """
    try:
        result = model_service.get_symptom_severity(symptom)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Symptom '{symptom}' not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch symptom severity: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for the prediction service"""
    return {"status": "healthy"}
