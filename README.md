# VectorMatrix – AI Driven Query-to-Team Matching System

VectorMatrix is a full-stack ML-powered system designed to automatically match incoming technical queries from public forums (Reddit, Microchip forums, etc.) to the most suitable internal engineering teams using SBERT embeddings and cosine similarity.  
It includes:

- React (Vite) Frontend  
- Flask Backend  
- SBERT Embedding Model  
- Fully automated query → team matching  
- Dashboard + Full Ranking UI  
- JSON database (no external DB required)

---

# 🚀 Project Overview

### 1. Team Module
Users submit:
- Full Name  
- Email  
- Team Name  
- Manager Name  
- Documents / Links  

System:
- Extracts skills, tools, work areas  
- Generates SBERT embeddings  
- Saves raw + processed versions  

---

### 2. Query Module
Queries come from:
- Reddit JSON  
- Microchip forum  
- Manual input  

Each query contains:
- Title, Content  
- Source, URL  
- Timestamp  
- Comments count  

System:
- Cleans text  
- Extracts keywords  
- Embeds using SBERT  
- Saves raw + processed versions  

---

### 3. Matching Engine
Matching is done using cosine similarity:

```
score = dot(query_emb, team_emb) / (|query_emb| * |team_emb|)
```

Highest score = best team.

Results stored in:
- match_results.json  

---

### 4. Dashboard Module (React UI)
Features:
- Query → Team match cards  
- Color-coded score badges  
- Team logos  
- Sorting (asc/desc)  
- Filtering (team)  
- “View Full Ranking” page  
- Responsive layout  

---

# 🧠 System Architecture

```
Teams → Preprocess → Embedding
Queries → Preprocess → Embedding
               ↓
         Matching Engine
               ↓
Dashboard (Best Team + Ranking)
```

---

# 📁 Project Structure

```
vector-matrix/
│
├── backend/
│   ├── app.py
│   ├── teams_details.json
│   ├── team_processed_details.json
│   ├── queries_raw.json
│   ├── queries_processed.json
│   ├── match_results.json
│   └── requirements.txt
│
└── frontend-react/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── api.js
        ├── components/
        │   └── Navbar.jsx
        └── pages/
            ├── Dashboard.jsx
            ├── Ranking.jsx
            ├── Teams.jsx
            ├── ViewTeam.jsx
            ├── EditTeam.jsx
            └── Home.jsx
```

---

# 🔧 Backend Setup

## macOS
```
cd backend
/opt/homebrew/bin/python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Windows
```
cd backend
python -m venv venv
venv\Scriptsctivate
pip install -r requirements.txt
python app.py
```

Backend runs at:
```
http://127.0.0.1:5000
```

---

# 🌐 Frontend Setup

```
cd frontend-react
npm install
npm run dev
```

UI runs at:
```
http://localhost:5173
```

---

# 🌍 API Summary

## Team APIs
```
POST /api/teams
GET  /api/teams
GET  /api/teams/processed
GET  /api/team/<id>
GET  /api/team/processed/<id>
```

## Query APIs
```
POST /api/queries
POST /api/queries/process/<qid>
GET  /api/queries/raw
GET  /api/queries/processed
```

## Matching & Dashboard APIs
```
POST /api/match/<qid>
GET  /api/matches
GET  /api/dashboard/matches
GET  /api/dashboard/rankings/<qid>
```

---

# 🎨 UI Features

- Team logos  
- Color-coded score badges  
- Query cards  
- Sorting & filtering  
- Full ranking page  
- Team editing and details  

---

# 🗄 JSON Database Files

| File | Purpose |
|------|----------|
| teams_details.json | Raw team data |
| team_processed_details.json | Processed teams with embeddings |
| queries_raw.json | Raw queries |
| queries_processed.json | Processed queries with embeddings |
| match_results.json | All match records |

---

# 🛠 Troubleshooting

### macOS: “externally-managed-environment”
Use:
```
/opt/homebrew/bin/python3 -m venv venv
```

### ModuleNotFoundError (Flask)
```
source venv/bin/activate
pip install flask flask-cors
```

### SBERT model download errors
Ensure internet OR pre-download model:
```
pip install sentence-transformers
```

### React Vite plugin error
```
npm install @vitejs/plugin-react
```

---

# 🎉 You're Ready!
VectorMatrix is fully operational with Teams + Queries + Matching + Dashboard + Ranking.
