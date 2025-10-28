from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SymptomInput(BaseModel):
    symptoms: List[str] = Field(..., description="List of symptoms")

class DiseasePrediction(BaseModel):
    prediction: str = Field(..., description="Predicted disease name")
    details: Dict[str, Any] = Field(..., description="Detailed information about the predicted disease")

class SymptomList(BaseModel):
    symptoms: List[Dict[str, Any]] = Field(..., description="List of available symptoms with their IDs")

class DiseaseList(BaseModel):
    diseases: List[Dict[str, Any]] = Field(..., description="List of available diseases with their IDs")
