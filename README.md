# VectorMatrix – Team Details Management System

VectorMatrix is a full-stack project built using:

- **React (Vite)** – Single Page Application (SPA)
- **Flask (Python)** – REST API backend
- **JSON Database** – Lightweight storage for:
  - Raw team details (`teams_details.json`)
  - Processed team details (`team_processed_details.json`)

When a user submits team details through the UI, the backend **automatically preprocesses** them and stores both raw and transformed data.

---

# 🚀 Project Overview

VectorMatrix enables teams to:

- Submit team data from UI  
- Automatically preprocess team information  
- Store raw + processed data separately  
- View team lists instantly  
- Use a futuristic React UI  
- Connect to a Flask JSON-backed API

---

# 📁 Folder Structure

```
vector-matrix/
│
├── backend/
│   ├── app.py
│   ├── teams_details.json
│   ├── team_processed_details.json
│   ├── requirements.txt
│   └── venv/
│
└── frontend-react/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
```

---

# 🔧 Backend Setup (Flask API)

## macOS

### Install Python & Node (Homebrew recommended)
```
brew install python node
```

### Create virtual environment
```
cd vector-matrix/backend
/opt/homebrew/bin/python3 -m venv venv
source venv/bin/activate
```

### Install backend dependencies
```
pip install -r requirements.txt
```

### Start backend server
```
python3 app.py
```

Backend runs at:
```
http://127.0.0.1:5000
```

---

## Windows

### Create virtual environment
```
cd vector-matrix\backend
python -m venv venv
venv\Scripts\activate
```

### Install dependencies
```
pip install flask flask-cors
```

### Start server
```
python app.py
```

---

# 🌐 Frontend Setup (React + Vite)

### Install frontend dependencies
```
cd vector-matrix/frontend-react
npm install
```

### Start frontend dev server
```
npm run dev
```

Frontend runs at:
```
http://localhost:5173/
```

---

# 🧠 API Endpoints

## Base URL
```
http://127.0.0.1:5000/api
```

### 1️⃣ Get all raw teams  
**GET** `/api/teams`

### 2️⃣ Add new team (triggers processing)  
**POST** `/api/teams`

### 3️⃣ Get single raw item  
**GET** `/api/team/<id>`

### 4️⃣ Delete raw item  
**DELETE** `/api/team/<id>`

### 5️⃣ Get all processed items  
**GET** `/api/processed`

### 6️⃣ Get one processed item  
**GET** `/api/processed/<id>`

---

# 🗄 JSON Database Files

| File | Description |
|------|-------------|
| `teams_details.json` | Raw submitted team data |
| `team_processed_details.json` | Backend-processed data |

Both are auto-created if missing.

---

# 🐞 Troubleshooting

### Flask: ModuleNotFoundError: No module named flask
You installed Flask globally instead of inside venv.

Fix:
```
source venv/bin/activate
pip install flask flask-cors
```

### macOS: “externally-managed-environment”
Use Homebrew Python:
```
/opt/homebrew/bin/python3 -m venv venv
```

### React plugin error
```
npm install @vitejs/plugin-react
```

---

# 🎉 You're Ready!
VectorMatrix is fully set up on **Windows** and **macOS**.

