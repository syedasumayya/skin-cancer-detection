# 🧬 Skin Cancer Detection AI System

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
- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)