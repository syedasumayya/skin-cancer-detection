<!-- # 🧬 Skin Cancer Detection AI System

A professional medical AI application for skin lesion classification using a **ResNet50 CNN architecture** with a **Next.js** frontend and **FastAPI** backend.

---

## 🏥 Features

- **Professional Medical Image Validation** — Rejects non-medical images (empty pages, documents, random objects) before they reach the AI model.
- **Advanced Cancer Detection** — ResNet50 + CNN with realistic medical analysis, classifying lesions into 7 distinct categories.
- **Secure JWT Authentication** — Custom-built token-based authentication system with secure password hashing.
- **Real-time Analysis** — Fast skin lesion prediction with multi-class confidence scoring and color-coded risk assessment.
- **Persistent Database Storage** — User accounts and scan history are permanently saved to a database.
- **Medical Recommendations** — Professional post-analysis advice based on the specific predicted condition.

---

## 📋 Prerequisites

Before running this project, ensure you have:

- Python 3.11+ installed (**Note:** Python 3.12/3.13/3.14 will **NOT** work with TensorFlow)
- Node.js 18+ installed
- Git installed
- VS Code with Python and JavaScript extensions installed

---

## 🚀 Step-by-Step Setup Guide

### Step 1: Clone and Open Project

```bash
git clone https://github.com/syedasumayya/skin-cancer-detection.git
cd skin-cancer-detection
code .
```

### Step 2: Python Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: AI Model Setup

1. Create a folder named `model_weights` inside the `backend` folder.
2. Place your trained `skin_cancer_model.h5` file inside `model_weights/`.
3. In `backend/main.py`, ensure `use_simulation=False` to use the real AI.

> **Note:** If no model file is provided, the system safely falls back to an intelligent simulation mode.

### Step 4: Frontend Setup

Open a new VS Code terminal and run:

```bash
cd frontend
npm install
```

---

## 🔧 Running the Project

**Terminal 1 — Backend:**

```bash
cd backend
venv\Scripts\activate
python main.py
```

You should see: `✅ AI Model loaded successfully` and `✅ Server ready at http://localhost:8000`

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

You should see: `Local: http://localhost:3000/`

---

## 📁 Project Structure

```
skin-cancer-detection/
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── preprocessing.py
│   ├── auth.py
│   ├── schemas.py
│   ├── database.py
│   ├── models.py
│   ├── model_weights/         # PUT YOUR .h5 MODEL HERE
│   ├── uploads/               # User uploaded images
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js pages
│   │   ├── components/        # React UI components
│   │   ├── context/           # Authentication context
│   │   ├── lib/                # API client
│   │   └── types/              # TypeScript types
│   ├── package.json
│   └── tailwind.config.js
├── .gitignore
└── README.md
```

---

## 🧪 Testing the System

1. **Register/Login** — Go to `http://localhost:3000`. Create an account or sign in.
2. **Test Image Validation** — Upload a non-medical image (a Word document, a screenshot). Should see: *"This doesn't appear to contain skin."*
3. **Test Cancer Detection** — Upload a close-up image of a skin lesion or mole. Should receive a detailed analysis with confidence scores.
4. **Test Database Permanence** — Restart the backend server, log back in, and check the "History" tab. Your previous scans should still be there.

---

## 🔍 Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'tensorflow'` | You're using Python 3.12+. Install Python 3.11, delete the `venv` folder, and recreate it using `py -3.11 -m venv venv`. |
| `passlib`/`bcrypt` `ValueError` | Run `pip install bcrypt==4.0.1` to fix the version clash. |
| Frontend won't connect to Backend | Ensure the backend terminal is running on port 8000 before starting the frontend. |

---

## 🏥 Medical Disclaimer

This AI system is for **educational and screening purposes only**. All results must be interpreted by qualified healthcare professionals. Never use for final medical diagnosis without proper medical consultation.

---

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [TensorFlow Documentation](https://www.tensorflow.org/api_docs) -->
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow) ![ResNet50](https://img.shields.io/badge/ResNet50-CNN-blue?style=for-the-badge) ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite)

# 🧬 SkinAI: Full-Stack Skin Cancer Detection System

SkinAI is a professional, production-grade medical AI application designed for skin lesion classification. Built with a custom-trained **ResNet50 Convolutional Neural Network (CNN)**, it features a strict separation of concerns between a **Next.js** frontend and a **FastAPI** backend, ensuring scalable and maintainable architecture.



---

## 🌟 Key Features

- 🧠 **Real-Time Deep Learning** — Uses a custom-trained ResNet50 model (Transfer Learning) to classify skin lesions into 7 distinct categories.
- 🛡️ **Smart Image Validation** — OpenCV-powered preprocessing rejects non-medical images (documents, random objects) before they reach the AI.
- 🔐 **Secure Authentication** — JWT-based auth system with bcrypt password hashing and protected API routes.
- 🗄️ **Persistent Database** — SQLAlchemy ORM with SQLite for permanent storage of user data and scan history.
- 🎨 **Modern UI/UX** — Built with Next.js 14 (App Router), TypeScript, and Tailwind CSS for a flawless, responsive interface.
- 📊 **Detailed Analytics** — Displays multi-class confidence percentages, color-coded risk levels, and professional medical recommendations.

---

## 🏗️ Architecture & Tech Stack

This project utilizes a monorepo structure, strictly separating frontend and backend logic.

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS | User Interface, State Management, API Calls |
| **Backend** | Python, FastAPI, Pydantic | REST API, JWT Auth, Request Handling |
| **Database** | SQLite, SQLAlchemy ORM | Persistent User & Analysis Storage |
| **AI / ML** | TensorFlow, Keras, ResNet50 | Image Preprocessing, Feature Extraction, Prediction |
| **Vision** | OpenCV, NumPy, Pillow | Image Validation, Color Space Analysis |

**Data Flow:**
`User Upload ➜ Next.js (Axios) ➜ FastAPI ➜ OpenCV Validation ➜ ResNet50 Inference ➜ SQLite Database ➜ UI Response`

---

## 📂 Project Structure

```
skin-cancer-detection/
├── backend/                  # Python FastAPI Server
│   ├── main.py                # Application entry point & API routes
│   ├── auth.py                # JWT & Bcrypt authentication logic
│   ├── model.py                # ResNet50 AI model wrapper & simulation mode
│   ├── preprocessing.py       # OpenCV image validation & formatting
│   ├── schemas.py              # Pydantic data models (Type safety)
│   ├── database.py             # SQLAlchemy engine & session config
│   ├── models.py                # Database table blueprints (Users, Analysis)
│   ├── model_weights/          # Directory for the trained .h5 model file
│   ├── uploads/                # Directory for user-uploaded images
│   ├── requirements.txt        # Python dependencies
│   └── skin_cancer.db          # SQLite database file (auto-generated)
│
├── frontend/                  # Next.js 14 Application
│   ├── src/
│   │   ├── app/                # App Router (pages)
│   │   ├── components/         # Reusable UI components
│   │   ├── context/            # React Context (Auth state)
│   │   ├── lib/                 # Axios API client configuration
│   │   ├── types/                # TypeScript interfaces
│   │   └── utils/                 # Helper functions
│   ├── package.json            # Node.js dependencies
│   └── tailwind.config.js      # Tailwind CSS configuration
│
├── .gitignore                  # Files ignored by Git
└── README.md                   # You are here!
```

---

## 🚀 Local Setup & Installation

### Prerequisites

- Python 3.11+ (Required for TensorFlow compatibility)
- Node.js 18+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/syedasumayya/skin-cancer-detection.git
cd skin-cancer-detection
```

### 2. Backend Setup

> **Note:** Requires Python 3.11 due to TensorFlow constraints. If you have Python 3.12+, use `py -3.11` to create the venv.

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> To use the real AI model, place your trained `skin_cancer_model.h5` file inside the `backend/model_weights/` folder and ensure `use_simulation=False` in `main.py`. If no model is provided, the system safely falls back to an intelligent simulation mode.

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

### 4. Run the Application

**Terminal 1 (Backend):**

```bash
cd backend
venv\Scripts\activate
python main.py
# Server runs on http://localhost:8000
```

**Terminal 2 (Frontend):**

```bash
cd frontend
npm run dev
# Client runs on http://localhost:3000
```

Access the application at: **http://localhost:3000**

---

## 🧠 AI Model Training

The ResNet50 model was trained using **Transfer Learning** on the **HAM10000** (Human Against Machine with 10000 Training Images) dataset.

**Pipeline:**

- **Base Model:** Pre-trained ResNet50 on ImageNet (frozen weights).
- **Classification Head:** `GlobalAveragePooling2D → Dense(512) → Dropout(0.5) → Softmax(7)`.
- **Training Environment:** Google Colab (NVIDIA T4 GPU).
- **Classes:** Melanoma, Melanocytic Nevus, Basal Cell Carcinoma, Actinic Keratosis, Benign Keratosis, Dermatofibroma, Vascular Lesion.

---

## 🛠️ API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/health` | Check server and model status | ❌ |
| `POST` | `/api/auth/register` | Register a new user | ❌ |
| `POST` | `/api/auth/login` | Login and get JWT token | ❌ |
| `GET` | `/api/auth/me` | Get current user profile | ✅ |
| `POST` | `/api/analyze` | Upload & analyze skin image | ✅ |
| `GET` | `/api/history` | Get user's past scans | ✅ |

---

## 🚧 Future Improvements

- [ ] Dockerize the application for seamless deployment.
- [ ] Upgrade database to PostgreSQL for production.
- [ ] Deploy backend on AWS/Azure and Frontend on Vercel.
- [ ] Implement "Google Sign-In" via OAuth2.
- [ ] Add Grad-CAM heatmap visualizations to show exactly what the AI is looking at.

---

## ⚕️ Medical Disclaimer

This AI system is developed strictly for **educational and demonstration purposes**. It is **NOT** a certified medical device. The predictions generated by this model should never be used as a definitive medical diagnosis. Always consult a qualified dermatologist or healthcare professional for medical advice and diagnosis.

---

## 📜 License

This project is licensed under the **MIT License**.

<div align="center">

Built with ❤️ by <a href="https://github.com/syedasumayya">Syeda Sumayya</a>

</div>