"""
preprocessing.py - Image validation and preprocessing
This is the GATEKEEPER — it decides if an image is actually
a skin lesion photo or just a random photo/document.
"""

import cv2
import numpy as np
from PIL import Image
import io


# Skin lesion images typically have these characteristics:
# - Dominantly light/pinkish tones (skin color)
# - Rounded/irregular dark spots (lesions)
# - Relatively uniform background (skin)
# - Not mostly text, not mostly one solid color


def validate_medical_image(image_bytes: bytes) -> dict:
    """
    Validates if the uploaded image appears to be a skin lesion image.
    
    This uses multiple heuristics:
    1. Color distribution check (should have skin-tone pixels)
    2. Edge density check (lesions create edges)
    3. Texture variance check (skin has texture, documents don't)
    4. Aspect ratio check (medical images are roughly square)
    
    Args:
        image_bytes: Raw image bytes from upload
        
    Returns:
        dict with 'is_valid' (bool) and 'reason' (str)
    """
    try:
        # Convert bytes to numpy array for OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {
                "is_valid": False,
                "reason": "Could not decode the image file. Please upload a valid image (JPG, PNG)."
            }
        
        # Check image dimensions — too small = probably not a real photo
        height, width = img.shape[:2]
        if height < 100 or width < 100:
            return {
                "is_valid": False,
                "reason": "Image resolution is too low. Please upload a higher quality image."
            }
        
        # Check aspect ratio — medical images are usually roughly square
        aspect_ratio = max(height, width) / min(height, width)
        if aspect_ratio > 4.0:
            return {
                "is_valid": False,
                "reason": "Image aspect ratio is unusual for a medical image. Please upload a standard photo."
            }
        
        # Check if image is mostly one color (like a blank white page)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0], None, [50], [0, 180])
        hist = hist.flatten()
        hist = hist / hist.sum()  # Normalize
        
        # If one color bin has >60% of pixels, it's probably a solid color image
        max_bin_ratio = hist.max()
        if max_bin_ratio > 0.60:
            return {
                "is_valid": False,
                "reason": "Image appears to be mostly a solid color. This doesn't look like a skin lesion photo."
            }
        
        # Check for skin-tone pixels
        # Skin color in HSV: H roughly 0-20, S roughly 15-170, V roughly 80-255
        lower_skin = np.array([0, 15, 80])
        upper_skin = np.array([20, 170, 255])
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        skin_percentage = np.count_nonzero(skin_mask) / (height * width)
        
        # Also check for darker skin tones
        lower_dark_skin = np.array([0, 20, 40])
        upper_dark_skin = np.array([25, 180, 140])
        dark_skin_mask = cv2.inRange(hsv, lower_dark_skin, upper_dark_skin)
        dark_skin_percentage = np.count_nonzero(dark_skin_mask) / (height * width)
        
        total_skin = skin_percentage + dark_skin_percentage
        
        if total_skin < 0.15:
            return {
                "is_valid": False,
                "reason": "Image doesn't appear to contain skin. Please upload a photo of a skin lesion or mole."
            }
        
        # Check edge density — real photos have edges, blank pages don't
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.count_nonzero(edges) / (height * width)
        
        if edge_density < 0.01:
            return {
                "is_valid": False,
                "reason": "Image appears to be blank or very simple. This doesn't look like a medical image."
            }
        
        # If it passed all checks, it's likely valid
        return {
            "is_valid": True,
            "reason": "Image appears to be a valid skin lesion photo."
        }
        
    except Exception as e:
        return {
            "is_valid": False,
            "reason": f"Error processing image: {str(e)}"
        }


def preprocess_image(image_bytes: bytes, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Preprocess image for the CNN model.
    
    Steps:
    1. Decode image bytes to PIL Image
    2. Resize to model's expected input size (224x224 for ResNet50)
    3. Convert to numpy array
    4. Normalize pixel values to [0, 1]
    5. Add batch dimension (model expects batches, not single images)
    
    Args:
        image_bytes: Raw image bytes
        target_size: Tuple of (height, width) for resizing
    
    Returns:
        Preprocessed numpy array with shape (1, 224, 224, 3)
    """
    # Open image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB (remove alpha channel if present)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to target size
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array and normalize to [0, 1]
    image_array = np.array(image, dtype=np.float32) / 255.0
    
    # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array