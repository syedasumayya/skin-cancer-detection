PythonFastAPINext.jsTensorFlowResNet50SQLite
🧬 SkinAI: Full-Stack Skin Cancer Detection System
SkinAI is a professional, production-grade medical AI application designed for skin lesion classification. Built with a custom-trained ResNet50 Convolutional Neural Network (CNN), it features a strict separation of concerns between a Next.js frontend and a FastAPI backend, ensuring scalable and maintainable architecture.



🌟 Key Features
🧠 Real-Time Deep Learning: Uses a custom-trained ResNet50 model (Transfer Learning) to classify skin lesions into 7 distinct categories.
🛡️ Smart Image Validation: OpenCV-powered preprocessing rejects non-medical images (documents, random objects) before they reach the AI.
🔐 Secure Authentication: JWT-based auth system with bcrypt password hashing and protected API routes.
🗄️ Persistent Database: SQLAlchemy ORM with SQLite for permanent storage of user data and scan history.
🎨 Modern UI/UX: Built with Next.js 14 (App Router), TypeScript, and Tailwind CSS for a flawless, responsive interface.
📊 Detailed Analytics: Displays multi-class confidence percentages, color-coded risk levels, and professional medical recommendations.
🏗️ Architecture & Tech Stack
This project utilizes a monorepo structure, strictly separating frontend and backend logic.

Layer	Technology	Purpose
Frontend	Next.js 14, TypeScript, Tailwind CSS	User Interface, State Management, API Calls
Backend	Python, FastAPI, Pydantic	REST API, JWT Auth, Request Handling
Database	SQLite, SQLAlchemy ORM	Persistent User & Analysis Storage
AI / ML	TensorFlow, Keras, ResNet50	Image Preprocessing, Feature Extraction, Prediction
Vision	OpenCV, NumPy, Pillow	Image Validation, Color Space Analysis
Data Flow: User Upload ➜ Next.js (Axios) ➜ FastAPI ➜ OpenCV Validation ➜ ResNet50 Inference ➜ SQLite Database ➜ UI Response

📂 Project Structure
skin-cancer-detection/├── backend/                  # Python FastAPI Server│   ├── main.py              # Application entry point & API routes│   ├── auth.py              # JWT & Bcrypt authentication logic│   ├── model.py             # ResNet50 AI model wrapper & simulation mode│   ├── preprocessing.py     # OpenCV image validation & formatting│   ├── schemas.py           # Pydantic data models (Type safety)│   ├── database.py          # SQLAlchemy engine & session config│   ├── models.py            # Database table blueprints (Users, Analysis)│   ├── model_weights/        # Directory for the trained .h5 model file│   ├── uploads/             # Directory for user-uploaded images│   ├── requirements.txt     # Python dependencies│   └── skin_cancer.db       # SQLite database file (auto-generated)│├── frontend/                 # Next.js 14 Application│   ├── src/│   │   ├── app/             # App Router (pages)│   │   ├── components/      # Reusable UI components│   │   ├── context/         # React Context (Auth state)│   │   ├── lib/             # Axios API client configuration│   │   ├── types/           # TypeScript interfaces│   │   └── utils/           # Helper functions│   ├── package.json         # Node.js dependencies│   └── tailwind.config.js   # Tailwind CSS configuration│├── .gitignore               # Files ignored by Git└── README.md                # You are here!
🚀 Local Setup & Installation
Prerequisites
Python 3.11+ (Required for TensorFlow compatibility)
Node.js 18+
Git
1. Clone the Repository
bash

git clone https://github.com/syedasumayya/skin-cancer-detection.git
cd skin-cancer-detection
2. Backend Setup
(Note: Requires Python 3.11 due to TensorFlow constraints. If you have Python 3.12+, use py -3.11 to create the venv).

bash

cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Note: To use the real AI model, place your trained skin_cancer_model.h5 file inside the backend/model_weights/ folder and ensure use_simulation=False in main.py. If no model is provided, the system safely falls back to an intelligent simulation mode.

3. Frontend Setup
Open a new terminal:

bash

cd frontend
npm install
4. Run the Application
Terminal 1 (Backend):

bash

cd backend
venv\Scripts\activate
python main.py
# Server runs on http://localhost:8000
Terminal 2 (Frontend):

bash

cd frontend
npm run dev
# Client runs on http://localhost:3000
Access the application at: http://localhost:3000

🧠 AI Model Training
The ResNet50 model was trained using Transfer Learning on the HAM10000 (Human Against Machine with 10000 Training Images) dataset.

Pipeline:

Base Model: Pre-trained ResNet50 on ImageNet (frozen weights).
Classification Head: Custom GlobalAveragePooling2D → Dense(512) → Dropout(0.5) → Softmax(7).
Training Environment: Google Colab (NVIDIA T4 GPU).
Classes: Melanoma, Melanocytic Nevus, Basal Cell Carcinoma, Actinic Keratosis, Benign Keratosis, Dermatofibroma, Vascular Lesion.
🛠️ API Endpoints
Method
Endpoint
Description
Auth Required
GET	/health	Check server and model status	❌
POST	/api/auth/register	Register a new user	❌
POST	/api/auth/login	Login and get JWT token	❌
GET	/api/auth/me	Get current user profile	✅
POST	/api/analyze	Upload & analyze skin image	✅
GET	/api/history	Get user's past scans	✅

🚧 Future Improvements
 Dockerize the application for seamless deployment.
 Upgrade database to PostgreSQL for production.
 Deploy backend on AWS/Azure and Frontend on Vercel.
 Implement "Google Sign-In" via OAuth2.
 Add Grad-CAM heatmap visualizations to show exactly what the AI is looking at.
⚕️ Medical Disclaimer
This AI system is developed strictly for educational and demonstration purposes. It is NOT a certified medical device. The predictions generated by this model should never be used as a definitive medical diagnosis. Always consult a qualified dermatologist or healthcare professional for medical advice and diagnosis.

📜 License
This project is licensed under the MIT License.

<div align="center">
Built with ❤️ by <a href="https://github.com/syedasumayya">Syeda Sumayya</a>
</div>
```