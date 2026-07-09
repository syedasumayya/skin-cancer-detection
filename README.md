🧬 SkinAI - Skin Cancer Detection AI System
A professional, production-grade medical AI application for skin lesion classification using a custom-trained ResNet50 CNN architecture with Next.js frontend and FastAPI backend.

🏥 Features
Professional Image Validation: Rejects non-medical images (empty pages, documents, random objects) using advanced OpenCV analysis before reaching the AI.
Advanced Cancer Detection: ResNet50 + CNN with realistic medical analysis classifying lesions into 7 distinct categories (Melanoma, Nevus, BCC, etc.).
Secure JWT Authentication: Custom-built token-based authentication system with bcrypt password hashing (No third-party auth dependencies).
Persistent Database Storage: User accounts and scan history are permanently saved using SQLAlchemy ORM and SQLite.
Real-time Analysis: Fast skin lesion prediction with multi-class confidence scoring and color-coded risk assessment.
Medical Recommendations: Professional post-analysis advice based on the specific predicted condition.
📋 Prerequisites
Before running this project, ensure you have:

Python 3.11 installed (Note: Python 3.12/3.13/3.14 will NOT work with TensorFlow. You must use 3.11)
Node.js 18+ installed
Git installed
VS Code with Python and JavaScript/TypeScript extensions
🚀 Step-by-Step Setup Guide
Step 1: Clone and Open Project
git clone https://github.com/syedasumayya/skin-cancer-detection.gitcd skin-cancer-detectioncode .
Step 2: Python Backend Setup
Open a terminal in VS Code and run:

bash

cd backend
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Step 3: AI Model & Database Setup
The application uses a real ResNet50 model.

Create a folder named model_weights inside the backend folder.
Place your trained skin_cancer_model.h5 file inside model_weights/.
(Note: If you do not have a model file, the system will automatically and safely fall back to a "Simulation Mode" that generates realistic UI responses for testing).
The SQLite database (skin_cancer.db) will be created automatically the first time you start the server.

Step 4: Frontend Setup
Open a second terminal in VS Code and run:

bash

cd frontend
npm install
🔧 Running the Project
You must have two terminals open at the same time.

Terminal 1 - Backend (Port 8000):

bash

cd backend
venv\Scripts\activate
python main.py
You should see: ✅ AI Model loaded successfully and ✅ Database tables checked/created

Terminal 2 - Frontend (Port 3000):

bash

cd frontend
npm run dev
Access Application:

Frontend App: http://localhost:3000
Backend API Docs: http://localhost:8000/docs
📁 Project Structure
text

skin-cancer-detection/
├── backend/                  # Python FastAPI Server
│   ├── main.py              # API routes & lifespan
│   ├── auth.py              # JWT & Bcrypt logic
│   ├── model.py             # ResNet50 AI model wrapper
│   ├── preprocessing.py     # OpenCV image validation
│   ├── schemas.py           # Pydantic data models
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database table schemas
│   ├── model_weights/        # PUT YOUR .h5 MODEL HERE
│   ├── requirements.txt     # Python dependencies
│   └── skin_cancer.db       # Auto-generated SQLite DB
│
├── frontend/                 # Next.js 14 Application
│   ├── src/
│   │   ├── app/             # Pages (login, register, dashboard, history)
│   │   ├── components/      # Reusable UI components
│   │   ├── context/         # React Auth Context
│   │   ├── lib/             # Axios API client
│   │   └── types/           # TypeScript interfaces
│   ├── package.json         # Node dependencies
│   └── tailwind.config.js   # Tailwind setup
│
├── .gitignore               # Git ignore rules
└── README.md                # You are here!
🧪 Testing the System
Register/Login:
Go to http://localhost:3000. Create an account or sign in. Your data is permanently saved to the database.
Test Image Validation:
Upload a non-medical image (a Word document, a screenshot of code). The AI will reject it: "This doesn't appear to contain skin."
Test Cancer Detection:
Upload a close-up image of a skin lesion/mole. The system will analyze it, show the primary prediction, confidence percentages for all 7 classes, and provide medical recommendations.
Test Database Permanence:
Close the backend terminal, restart it (python main.py), log back in, and check the "History" tab. Your previous scans will still be there.
🔍 Troubleshooting
ModuleNotFoundError: No module named 'tensorflow'
You are likely using Python 3.12 or newer. TensorFlow requires Python 3.11. Install Python 3.11, delete the venv folder, and recreate it using py -3.11 -m venv venv.
passlib/bcrypt ValueError
Run pip install bcrypt==4.0.1 to fix the version clash between passlib and bcrypt.
Frontend won't connect to Backend (CORS error)
Ensure the backend is actually running on port 8000 before starting the frontend.
Port 3000 or 8000 is already in use
Close any other applications using those ports, or change the ports in main.py and vite.config.js.
🏥 Medical Disclaimer
This AI system is for educational and portfolio demonstration purposes only. All results are generated by a machine learning model and must be interpreted by qualified healthcare professionals. Never use this system for final medical diagnosis or as a substitute for professional medical consultation.

📝 Development Notes
Backend runs on FastAPI with automatic interactive API documentation (/docs).
Frontend uses Next.js 14 (App Router) with Tailwind CSS for responsive design.
AI model uses ResNet50 with Transfer Learning.
Authentication uses standard JSON Web Tokens (JWT) passed via Bearer headers.
Database uses SQLAlchemy ORM (can be easily swapped to PostgreSQL for production).
🔗 Additional Resources
FastAPI Documentation
Next.js Documentation
TensorFlow Documentation
