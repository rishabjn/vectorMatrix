# VectorMatrix Backend – Modular Architecture & Auto-Reprocess

## 📦 Overview
VectorMatrix is a modular backend built using **Flask + SBERT** for:
- Collecting team details
- Collecting forum queries (Reddit, Microchip forums etc.)
- Preprocessing inputs using embeddings
- Running semantic matching between queries & teams
- Visualizing results in a React dashboard  

This document includes:
1. Project Structure  
2. JSON Database Layout  
3. API Endpoints  
4. Auto-Reprocess Feature  
5. Developer Commands  
6. Dataflow Diagram Explanation  
7. Extending the System  

---

# 📁 Folder Structure

```
backend/
│
├── app.py
├── db/
│   ├── teams/
│   │   ├── teams_details.json
│   │   └── team_processed_details.json
│   │
│   ├── queries/
│   │   ├── queries_raw.json
│   │   └── queries_processed.json
│   │
│   ├── matches/
│       └── match_results.json
│
├── processing/
│   ├── preprocess_team.py
│   ├── preprocess_query.py
│   ├── rebuild_matches.py
│   └── utils.py
│
├── scripts/
│   ├── reprocess_all.py
│   ├── import_reddit.py
│
├── requirements.txt
└── venv/
```

---

# 🧠 Data Flow (Example)

```
Raw Teams ─────────────┐
                        │
                        ▼
             preprocess_team.py
                        │
                        ▼
         team_processed_details.json
                        │
                        │
Raw Queries ────────────┐
                        ▼
            preprocess_query.py
                        │
                        ▼
        queries_processed.json
                        │
                        ▼
        rebuild_matches.py (cosine similarity)
                        │
                        ▼
           match_results.json
                        │
                        ▼
        React Dashboard (UI)
```

### ✔ Example Scenario

- Team: *MPLAB Tooling Team*  
- Query: “PIC16F877 enum structure issues in MPLAB X”

Generated:
```
PIC16F Query → Assigned to MPLAB Tools (Score 0.89)
```

---

# ⚙️ Auto-Reprocess Feature

Whenever a **team or query** is added, VectorMatrix:

✔ Rebuilds processed team embeddings  
✔ Rebuilds processed query embeddings  
✔ Regenerates match results  
✔ Automatically updates dashboard  


---

# 🔌 API Endpoints

## Teams
POST `/api/teams`  
GET `/api/teams`  
GET `/api/teams/processed`

## Queries
POST `/api/queries`  
GET `/api/queries/raw`  
GET `/api/queries/processed`

## Matching
POST `/api/match/<qid>`  
GET `/api/dashboard/overview`  
GET `/api/dashboard/rankings/<qid>`  

---

# 🛠 Setup Instructions

## Mac
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
python3 -m scripts.reprocess_all # (Optional, when new data arrives)
```

## Windows
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
python -m scripts.reprocess_all # (Optional, when new data arrives)

```

---

# React Setup

```
cd frontend-react
npm install
npm run dev
```

---

# JSON DB Structures

### teams_details.json
```
{
  "id": "uuid",
  "team_name": "...",
  "full_name": "...",
  "documents": ["doc1", "doc2"]
}
```

### team_processed_details.json
```
{
  "id": "uuid",
  "skills": ["c", "embedded"],
  "embedding": [...]
}
```

### queries_processed.json
```
{
  "id": "q-uuid",
  "clean_text": "...",
  "keywords": ["c"],
  "embedding": [...]
}
```

### match_results.json
```
{
  "query_id": "q-uuid",
  "team_id": "uuid",
  "score": 0.87,
  "ranking": [...]
}
```

---

# Extending the System

- Add Jira/Github/StackOverflow sources  
- Replace SBERT with GPT embeddings  
- Add Authentication (JWT)  
- Add CLI tools  
- Convert JSON DB → SQLite or MongoDB  

