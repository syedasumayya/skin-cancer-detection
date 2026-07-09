"""
schemas.py - Data models for the API
These define what data looks like going in and out of your endpoints.
Pydantic validates that incoming data matches these schemas automatically.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ============ AUTHENTICATION SCHEMAS ============

class UserCreate(BaseModel):
    """Data required to register a new user"""
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=100, description="Password (min 6 chars)")


class UserLogin(BaseModel):
    """Data required to log in"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Data returned about a user (never includes password)"""
    id: str
    email: str
    name: str
    created_at: str
    scans_count: int = 0


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============ ANALYSIS SCHEMAS ============

class ClassPrediction(BaseModel):
    """Prediction for a single skin lesion class"""
    class_name: str
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage 0-100")
    risk_level: str = Field(..., description="Low, Medium, or High")


class AnalysisResponse(BaseModel):
    """Full analysis result returned after image processing"""
    success: bool
    is_valid_image: bool
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    all_predictions: Optional[List[ClassPrediction]] = None
    risk_assessment: Optional[str] = None
    recommendations: Optional[List[str]] = None
    error_message: Optional[str] = None
    image_id: Optional[str] = None
    analyzed_at: Optional[str] = None


class AnalysisHistoryItem(BaseModel):
    """Single item in analysis history"""
    id: str
    prediction: str
    confidence: float
    risk_level: str
    image_filename: str
    analyzed_at: str


# ============ SYSTEM SCHEMAS ============

class HealthResponse(BaseModel):
    """System health check response"""
    status: str
    model_loaded: bool
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    status_code: int = 400