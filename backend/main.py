"""
main.py - FastAPI Application Entry Point (WITH DATABASE)
"""
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

# Import our modules
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    AnalysisResponse, ClassPrediction,
    AnalysisHistoryItem, HealthResponse
)
from preprocessing import validate_medical_image, preprocess_image
from model import SkinCancerModel
from database import SessionLocal, engine, Base
from models import User, Analysis as AnalysisModel

# ============ SETUP LOGGING ============
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============ GLOBAL MODEL INSTANCE ============
model_instance = None

# ============ APP LIFESPAN ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_instance
    logger.info("=" * 50)
    logger.info("🚀 SKIN CANCER DETECTION AI - STARTING")
    logger.info("=" * 50)
    
    # CREATE DATABASE TABLES IF THEY DON'T EXIST
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables checked/created")
    
    # Create directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static/results", exist_ok=True)
    
    # Load AI model
    try:
        model_instance = SkinCancerModel(use_simulation=False)
        logger.info("✅ AI Model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Model init failed: {e}")
    
    logger.info("✅ Server ready at http://localhost:8000")
    logger.info("=" * 50)
    yield
    logger.info("🛑 Server shutting down...")

# ============ DATABASE DEPENDENCY ============
def get_db():
    """Opens a database connection, yields it, and closes it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ CREATE FASTAPI APP ============
app = FastAPI(title="Skin Cancer Detection AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ========================================
# ROUTES
# ========================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    return HealthResponse(status="healthy", model_loaded=model_instance is not None and model_instance.model_loaded, version="1.0.0", timestamp=datetime.utcnow().isoformat())

@app.post("/api/auth/register", response_model=UserResponse, tags=["Auth"])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists in DATABASE
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="This email is already registered")
    
    # Save to DATABASE
    user_id = str(uuid.uuid4())
    new_user = User(id=user_id, email=user_data.email, name=user_data.name, hashed_password=get_password_hash(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"👤 New user registered: {user_data.email}")
    return UserResponse(id=new_user.id, email=new_user.email, name=new_user.name, created_at=str(new_user.created_at), scans_count=new_user.scans_count)

@app.post("/api/auth/login", response_model=Token, tags=["Auth"])
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Check DATABASE for user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": user.email})
    logger.info(f"🔑 User logged in: {credentials.email}")
    return Token(access_token=token, token_type="bearer", user=UserResponse(id=user.id, email=user.email, name=user.name, created_at=str(user.created_at), scans_count=user.scans_count))

@app.get("/api/auth/me", response_model=UserResponse, tags=["Auth"])
async def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user.id, email=user.email, name=user.name, created_at=str(user.created_at), scans_count=user.scans_count)

@app.post("/api/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        return AnalysisResponse(success=False, is_valid_image=False, error_message="File too large. Maximum size is 10MB.")
    
    validation = validate_medical_image(image_bytes)
    if not validation["is_valid"]:
        return AnalysisResponse(success=False, is_valid_image=False, error_message=validation["reason"])
    
    try:
        preprocessed = preprocess_image(image_bytes, target_size=(224, 224))
    except Exception as e:
        return AnalysisResponse(success=False, is_valid_image=True, error_message=f"Error preprocessing image: {str(e)}")
    
    if not model_instance: return AnalysisResponse(success=False, is_valid_image=True, error_message="AI model is not loaded.")
    
    try:
        result = model_instance.predict(preprocessed)
    except Exception as e:
        return AnalysisResponse(success=False, is_valid_image=True, error_message=f"Error during AI analysis: {str(e)}")
    
    # Save uploaded file
    image_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
    safe_filename = f"{image_id}.{file_extension}"
    with open(os.path.join("uploads", safe_filename), "wb") as f:
        f.write(image_bytes)
    
    # DETERMINE RISK LEVEL
    risk_level = "Low"
    if result["prediction"] in ["Melanoma", "Basal Cell Carcinoma"]: risk_level = "High"
    elif result["prediction"] == "Actinic Keratosis": risk_level = "Medium"

    # SAVE SCAN TO DATABASE
    new_analysis = AnalysisModel(
        id=image_id, user_email=current_user["email"],
        prediction=result["prediction"], confidence=result["confidence"],
        risk_level=risk_level, image_filename=safe_filename
    )
    db.add(new_analysis)
    
    # Update user scan count in DATABASE
    db_user = db.query(User).filter(User.email == current_user["email"]).first()
    if db_user: db_user.scans_count += 1
    
    db.commit() # PERMANENTLY SAVE TO HARD DRIVE
    logger.info(f"🔬 Analysis saved to database for {current_user['email']}")

    return AnalysisResponse(
        success=True, is_valid_image=True, prediction=result["prediction"], confidence=result["confidence"],
        all_predictions=[ClassPrediction(**p) for p in result["all_predictions"]],
        risk_assessment=result["risk_assessment"], recommendations=result["recommendations"],
        image_id=image_id, analyzed_at=datetime.utcnow().isoformat()
    )

@app.get("/api/history", response_model=list[AnalysisHistoryItem], tags=["Analysis"])
async def get_history(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 20):
    # READ FROM DATABASE
    history = db.query(AnalysisModel).filter(AnalysisModel.user_email == current_user["email"]).order_by(AnalysisModel.analyzed_at.desc()).limit(limit).all()
    return [AnalysisHistoryItem(id=h.id, prediction=h.prediction, confidence=h.confidence, risk_level=h.risk_level, image_filename=h.image_filename, analyzed_at=str(h.analyzed_at)) for h in history]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)