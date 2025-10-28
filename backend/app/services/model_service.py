import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from ..core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.model = None
        self.symptoms_dict = {}
        self.diseases_list = {}
        self.symptoms_df = None
        self.precautions_df = None
        self.workout_df = None
        self.description_df = None
        self.medications_df = None
        self.diets_df = None
        self.training_df = None
        self.symptom_severity_df = None
        self._load_models()
        self._load_data()
        self._initialize_symptoms_dict()
        self._initialize_diseases_list()

    def _load_models(self):
        """Load the trained ML model"""
        try:
            model_path = settings.MODEL_PATH
            logger.info(f"Loading model from: {model_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            self.model = joblib.load(model_path)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load the model: {str(e)}"
            )

    def _load_data(self):
        """Load all required data files"""
        try:
            logger.info("Loading data files...")
            data_dir = settings.DATA_DIR
            logger.info(f"Data directory: {data_dir}")
            
            # Verify data directory exists
            if not os.path.exists(data_dir):
                raise FileNotFoundError(f"Data directory not found at {data_dir}")
                
            # List files in the data directory for debugging
            logger.info(f"Files in data directory: {os.listdir(data_dir)}")
            
            # Load data files
            self.symptoms_df = pd.read_csv(data_dir / "symptoms_df.csv")
            self.precautions_df = pd.read_csv(data_dir / "Precautions_df.csv")
            self.workout_df = pd.read_csv(data_dir / "workout_df.csv")
            self.description_df = pd.read_csv(data_dir / "Description.csv")
            self.medications_df = pd.read_csv(data_dir / "Medications.csv")
            self.diets_df = pd.read_csv(data_dir / "Diets.csv")
            self.training_df = pd.read_csv(data_dir / "training.csv")
            self.symptom_severity_df = pd.read_csv(data_dir / "Symptom_Severity.csv")
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load data files: {str(e)}"
            )

    def _initialize_symptoms_dict(self):
        """Initialize the symptoms dictionary"""
        symptoms = [col.replace('_', ' ') for col in self.training_df.columns[:-1]]
        self.symptoms_dict = {symptom: idx for idx, symptom in enumerate(symptoms)}

    def _initialize_diseases_list(self):
        """Initialize the diseases list"""
        diseases = self.training_df['prognosis'].unique()
        self.diseases_list = {idx: disease for idx, disease in enumerate(diseases)}

    def get_disease_info(self, disease_name: str) -> Dict[str, Any]:
        """Get detailed information about a disease"""
        try:
            # Get description
            desc = self.description_df[self.description_df['Disease'] == disease_name]['Description']
            description = desc.values[0] if not desc.empty else "No description available."
            
            # Get precautions
            prec = self.precautions_df[self.precautions_df['Disease'] == disease_name].iloc[0] \
                if not self.precautions_df[self.precautions_df['Disease'] == disease_name].empty else {}
            precautions = [prec.get(f'Precaution_{i+1}') for i in range(4) if prec.get(f'Precaution_{i+1}')]
            
            # Get medications
            meds = self.medications_df[self.medications_df['Disease'] == disease_name]['Medication']
            medications = meds.values.tolist() if not meds.empty else []
            
            # Get diets
            diet = self.diets_df[self.diets_df['Disease'] == disease_name]['Diet']
            diets = diet.values.tolist() if not diet.empty else []
            
            # Get workouts
            workouts = self.workout_df[self.workout_df['disease'] == disease_name]['workout'].values.tolist()
            
            return {
                'disease': disease_name,
                'description': description,
                'precautions': precautions,
                'medications': medications,
                'diets': diets,
                'workouts': workouts
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting disease info: {str(e)}"
            )

    def predict_disease(self, symptoms: List[str]) -> Dict[str, Any]:
        """Predict disease based on symptoms"""
        try:
            # Validate input symptoms
            invalid_symptoms = [s for s in symptoms if s not in self.symptoms_dict]
            if invalid_symptoms:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid symptoms: {', '.join(invalid_symptoms)}. Use /symptoms to get valid symptoms."
                )
            
            # Create input vector
            input_vector = np.zeros(len(self.symptoms_dict))
            for symptom in symptoms:
                input_vector[self.symptoms_dict[symptom]] = 1
            
            # Make prediction
            prediction_idx = self.model.predict([input_vector])[0]
            disease_name = self.diseases_list.get(prediction_idx, "Unknown Disease")
            
            # Get additional disease information
            disease_info = self.get_disease_info(disease_name)
            
            return {
                'prediction': disease_name,
                'details': disease_info
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Prediction error: {str(e)}"
            )
    
    def get_available_symptoms(self) -> List[Dict[str, Any]]:
        """Get list of all available symptoms with their IDs"""
        return [{"id": idx, "name": name} for name, idx in self.symptoms_dict.items()]
    
    def get_available_diseases(self) -> List[Dict[str, Any]]:
        """Get list of all available diseases with their IDs"""
        return [{"id": idx, "name": name} for idx, name in self.diseases_list.items()]
    
    def get_symptom_severity(self, symptom: str) -> Optional[Dict[str, Any]]:
        """Get severity information for a specific symptom"""
        try:
            severity = self.symptom_severity_df[self.symptom_severity_df['Symptom'] == symptom]
            if not severity.empty:
                return {
                    'symptom': symptom,
                    'weight': int(severity['weight'].iloc[0]),
                    'description': severity['description'].iloc[0]
                }
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting symptom severity: {str(e)}"
            )