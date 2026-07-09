"""
auth.py - Authentication utilities
Handles password hashing, JWT token creation and verification.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-change-me-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24 hours default

# Password hashing context
# bcrypt is the industry standard for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token scheme
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password.
    Never store passwords in plain text — always hash them.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against its hash.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT token.
    
    The token contains the user's email (the 'sub' claim).
    It's signed with our secret key so it can't be forged.
    
    Args:
        data: Dictionary with claims (e.g., {"sub": "user@email.com"})
        expires_delta: How long until the token expires
    
    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    FastAPI dependency that extracts and validates the current user
    from the Authorization header.
    
    Use this in any endpoint that requires authentication:
        @app.get("/protected")
        async def protected_route(user = Depends(get_current_user)):
            ...
    
    Returns:
        dict with user info if token is valid
    
    Raises:
        HTTPException 401 if token is missing, invalid, or expired
    """
    token = credentials.credentials
    
    # Exception handling: catch any JWT errors
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Extract the email from the 'sub' claim
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
        return {"email": email}
        
    except JWTError:
        raise credentials_exception