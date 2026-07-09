"""
model.py - AI Model for Skin Lesion Classification

This module handles loading and running the CNN model.
It has TWO MODES:
1. SIMULATION MODE: Works without any trained model (for development/testing)
2. REAL MODE: Uses an actual trained ResNet50 model

The simulation mode generates realistic-looking predictions
so you can build and test the entire application without
needing a GPU or training data first.
"""

import numpy as np
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Skin lesion classes (based on HAM10000 dataset)
CLASSES = [
    "Melanoma",           # Most dangerous skin cancer
    "Melanocytic Nevus",  # Common mole (benign)
    "Basal Cell Carcinoma", # Common skin cancer
    "Actinic Keratosis",   # Pre-cancerous lesion
    "Benign Keratosis",    # Non-cancerous growth
    "Dermatofibroma",      # Benign skin nodule
    "Vascular Lesion"      # Blood vessel lesion
]

# Risk levels for each class
RISK_LEVELS = {
    "Melanoma": "High",
    "Melanocytic Nevus": "Low",
    "Basal Cell Carcinoma": "High",
    "Actinic Keratosis": "Medium",
    "Benign Keratosis": "Low",
    "Dermatofibroma": "Low",
    "Vascular Lesion": "Low"
}

# Detailed recommendations for each class
RECOMMENDATIONS = {
    "Melanoma": [
        "URGENT: Consult a dermatologist immediately",
        "Do not delay — early detection is critical for melanoma",
        "Prepare for possible biopsy and further diagnostic tests",
        "Avoid sun exposure until examined by a professional",
        "Note any changes in size, color, or shape of the lesion"
    ],
    "Melanocytic Nevus": [
        "This appears to be a common mole (nevus)",
        "Monitor for any changes using the ABCDE rule: Asymmetry, Border, Color, Diameter, Evolution",
        "Schedule routine skin check with a dermatologist",
        "Take photos monthly to track any changes",
        "Generally no immediate concern, but professional confirmation is recommended"
    ],
    "Basal Cell Carcinoma": [
        "Consult a dermatologist for professional evaluation",
        "Basal cell carcinoma is the most common but least dangerous skin cancer",
        "Treatment is usually very effective when caught early",
        "Avoid further sun damage to the area",
        "Various treatment options exist: surgery, topical medications, radiation"
    ],
    "Actinic Keratosis": [
        "This is a pre-cancerous lesion that should be monitored",
        "Schedule an appointment with a dermatologist",
        "Some actinic keratoses can progress to squamous cell carcinoma",
        "Treatment options include cryotherapy, topical creams, or photodynamic therapy",
        "Use broad-spectrum sunscreen daily to prevent new lesions"
    ],
    "Benign Keratosis": [
        "This appears to be a benign (non-cancerous) growth",
        "Seborrheic keratosis is very common and harmless",
        "No treatment is usually necessary unless it bothers you",
        "If it becomes irritated or changes appearance, see a dermatologist",
        "These can be removed for cosmetic reasons if desired"
    ],
    "Dermatofibroma": [
        "This appears to be a benign skin nodule",
        "Dermatofibromas are harmless and usually don't require treatment",
        "They may persist indefinitely but are not dangerous",
        "See a dermatologist if you're unsure or if it changes",
        "No specific follow-up is typically needed"
    ],
    "Vascular Lesion": [
        "This appears to be a vascular (blood vessel) lesion",
        "Most vascular lesions are benign (like cherry angiomas)",
        "Consult a dermatologist for proper identification",
        "Treatment is usually optional and for cosmetic reasons",
        "Laser therapy is effective if removal is desired"
    ]
}


class SkinCancerModel:
    """
    Skin lesion classification model.
    
    Supports two modes:
    - Simulation mode (default): Generates realistic predictions without a trained model
    - Real mode: Uses a trained TensorFlow/Keras model
    
    To switch to real mode, place your trained model file at:
        backend/model_weights/skin_cancer_model.h5
    
    And set USE_SIMULATION = False below.
    """
    
    def __init__(self, model_path: Optional[str] = None, use_simulation: bool = True):
        """
        Initialize the model.
        
        Args:
            model_path: Path to trained .h5 or .keras model file
            use_simulation: If True, use simulation mode (no model file needed)
        """
        self.model = None
        self.use_simulation = use_simulation
        self.model_loaded = False
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), "model_weights", "skin_cancer_model.h5"
        )
        
        if not use_simulation:
            self._load_model()
        else:
            logger.info("📊 Running in SIMULATION mode — no model file needed")
            self.model_loaded = True
    
    def _load_model(self):
        """Load the trained TensorFlow model"""
        try:
            import tensorflow as tf
            logger.info(f"Loading model from: {self.model_path}")
            
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                self.model_loaded = True
                logger.info("✅ Model loaded successfully")
            else:
                logger.warning(f"⚠️ Model file not found at {self.model_path}")
                logger.warning("⚠️ Falling back to SIMULATION mode")
                self.use_simulation = True
                self.model_loaded = True
                
        except ImportError:
            logger.warning("⚠️ TensorFlow not installed. Falling back to SIMULATION mode")
            self.use_simulation = True
            self.model_loaded = True
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            logger.warning("⚠️ Falling back to SIMULATION mode")
            self.use_simulation = True
            self.model_loaded = True
    
    def predict(self, preprocessed_image: np.ndarray) -> Dict:
        """
        Run prediction on a preprocessed image.
        
        Args:
            preprocessed_image: numpy array of shape (1, 224, 224, 3), values in [0, 1]
        
        Returns:
            Dictionary with prediction results
        """
        if self.use_simulation:
            return self._simulate_prediction(preprocessed_image)
        else:
            return self._real_prediction(preprocessed_image)
    
    def _simulate_prediction(self, image: np.ndarray) -> Dict:
        """
        Generate a realistic-looking prediction without an actual model.
        
        This uses the image's color statistics to produce somewhat
        consistent results — same image will tend to get similar predictions.
        This is NOT real AI — it's for development and testing only.
        """
        # Use image statistics as a pseudo-random seed for consistency
        mean_val = np.mean(image)
        std_val = np.std(image)
        seed = int((mean_val * 1000 + std_val * 500) % 1000)
        
        rng = np.random.RandomState(seed)
        
        # Generate confidence scores for each class
        raw_scores = rng.dirichlet(np.ones(len(CLASSES)) * 0.5)
        
        # Boost one class to be dominant (simulating a real prediction)
        dominant_idx = rng.choice(len(CLASSES), p=[0.3, 0.25, 0.1, 0.1, 0.15, 0.05, 0.05])
        raw_scores[dominant_idx] += rng.uniform(0.3, 0.6)
        
        # Normalize to sum to 1, then convert to percentages
        raw_scores = raw_scores / raw_scores.sum()
        percentages = raw_scores * 100
        
        # Build predictions list
        predictions = []
        for i, class_name in enumerate(CLASSES):
            predictions.append({
                "class_name": class_name,
                "confidence": round(float(percentages[i]), 1),
                "risk_level": RISK_LEVELS[class_name]
            })
        
        # Sort by confidence (highest first)
        predictions.sort(key=lambda x: x["confidence"], reverse=True)
        
        top_prediction = predictions[0]
        
        return {
            "prediction": top_prediction["class_name"],
            "confidence": top_prediction["confidence"],
            "all_predictions": predictions,
            "risk_assessment": self._generate_risk_assessment(top_prediction),
            "recommendations": RECOMMENDATIONS[top_prediction["class_name"]],
            "is_simulation": True
        }
    
    def _real_prediction(self, image: np.ndarray) -> Dict:
        """
        Run actual model prediction.
        Used when a trained model is available.
        """
        try:
            import tensorflow as tf
            
            # Run prediction
            predictions = self.model.predict(image, verbose=0)
            
            # Get class probabilities
            class_probs = predictions[0]
            
            # Build predictions list
            pred_list = []
            for i, class_name in enumerate(CLASSES):
                pred_list.append({
                    "class_name": class_name,
                    "confidence": round(float(class_probs[i] * 100), 1),
                    "risk_level": RISK_LEVELS[class_name]
                })
            
            # Sort by confidence
            pred_list.sort(key=lambda x: x["confidence"], reverse=True)
            
            top = pred_list[0]
            
            return {
                "prediction": top["class_name"],
                "confidence": top["confidence"],
                "all_predictions": pred_list,
                "risk_assessment": self._generate_risk_assessment(top),
                "recommendations": RECOMMENDATIONS[top["class_name"]],
                "is_simulation": False
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            # Fall back to simulation on error
            return self._simulate_prediction(image)
    
    def _generate_risk_assessment(self, top_prediction: Dict) -> str:
        """Generate a human-readable risk assessment"""
        risk = top_prediction["risk_level"]
        confidence = top_prediction["confidence"]
        cls = top_prediction["class_name"]
        
        if risk == "High":
            return (
                f"⚠️ HIGH RISK: The analysis indicates a {confidence}% probability of "
                f"{cls}. This is a serious finding that requires immediate professional "
                f"medical evaluation. Do not use this result as a definitive diagnosis."
            )
        elif risk == "Medium":
            return (
                f"🔍 MEDIUM RISK: The analysis suggests a {confidence}% probability of "
                f"{cls}. While not immediately alarming, this finding warrants "
                f"professional medical consultation for proper evaluation."
            )
        else:
            return (
                f"✅ LOW RISK: The analysis indicates a {confidence}% probability of "
                f"{cls}, which is typically benign. However, this is not a medical "
                f"diagnosis — regular skin checks with a dermatologist are always recommended."
            )