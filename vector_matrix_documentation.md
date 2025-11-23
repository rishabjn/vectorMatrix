
# VectorMatrix – Technical Documentation (Detailed)

## 1. Project Overview
VectorMatrix is an AI-driven Query-to-Team matching system designed to automatically route product-related queries from public forums (such as Reddit, Microchip community) to the correct internal engineering teams. The system processes both teams and queries using Sentence-BERT embeddings and computes similarity scores using cosine similarity.

## 2. System Goals
- Automate routing of public queries to relevant teams
- Reduce manual triage workload
- Provide insights and ranking of teams per query
- Serve as an internal dashboard for monitoring team-query match health

## 3. High-Level Workflow
1. **Teams Enter Data** (name, docs, skills)
2. **System Processes Teams**
   - Extracts keywords (skills/tools/work areas)
   - Generates embeddings from combined text
3. **Queries Imported**
   - Reddit / Forum raw data
4. **Query Preprocessing**
   - Clean + embed using SBERT
5. **Match Engine**
   - Calculates cosine similarity
   - Finds best team
6. **Dashboard**
   - Shows matched team
   - Full ranking per query
   - Filters, sorting, team logos, score colors

## 4. Backend Architecture (Flask)
Main components:
- `app.py` → REST API Server
- JSON-based database:
  - `teams_details.json`
  - `team_processed_details.json`
  - `queries_raw.json`
  - `queries_processed.json`
  - `match_results.json`

### 4.1 API Summary
```
POST /api/teams                   → Add team
GET  /api/teams                   → Get all teams (raw)
GET  /api/teams/processed         → Processed teams

POST /api/queries                 → Add a query (raw)
POST /api/queries/process/<qid>   → Process a query

POST /api/match/<qid>             → Match query → team

GET /api/dashboard/matches        → Dashboard cards
GET /api/dashboard/rankings/<qid> → Full ranking view

GET /api/queries/raw              → Raw queries
GET /api/queries/processed        → Processed queries
```

### 4.2 Team Processing
- Combine fields: team_name + full_name + manager + documents
- Extract entities (skills, tools, work areas)
- Generate SBERT vector embedding
- Store in JSON DB

### 4.3 Query Processing
- Combine title + content
- Clean + extract keywords
- Generate embedding
- Store in processed DB

### 4.4 Match Engine (Cosine Similarity)
```
score = dot(q_emb, team_emb) / (norm(q_emb) * norm(team_emb))
```

---

## 5. Machine Learning Component

### 5.1 Model Used
- **Sentence-BERT**
- Model: `"all-MiniLM-L6-v2"`
- Dimensionality: 384

### 5.2 Why SBERT?
- High-quality semantic similarity
- Lightweight (fast CPU inference)
- Ideal for clustering + ranking tasks

### 5.3 Embedding Flow
- Convert team/query text → embedding
- Store vector in JSON
- Compare vectors at match time

---

## 6. Frontend Architecture (React + Vite + Tailwind)

### 6.1 Pages
- **Home**
- **Teams** (list)
- **View Team**
- **Edit Team**
- **Dashboard** (query → team mapping)
- **Ranking** (full ranking page)

### 6.2 Dashboard Features
- Team logos (🌀, 🛠, 🔍, ⚡, etc.)
- Color-coded scores
  - 🟢 ≥ 70%
  - 🟡 40–70%
  - 🔴 < 40%
- Sorting
- Filtering
- Ranking navigation
- Clean card-based layout

---

## 7. Data Flow Diagram
```
db/teams/teams_details.json
            ↓
preprocess_team.py
            ↓
db/teams/team_processed_details.json
            ↓
                ↘
                 ↘   rebuild_matches.py
                 ↙
db/queries/queries_processed.json
            ↑
preprocess_query.py
            ↑
db/queries/queries_raw.json
            ↓
match_results.json
            ↓
Frontend Dashboard (React)

```

---

## 8. File Structure
```
vector-matrix/
│
├── backend/
│   ├── app.py
│   ├── db/
│   │   ├── teams/
│   │   ├── queries/
│   │   └── matches/
│   ├── processing/
│   ├── scripts/
│   ├── requirements.txt
│   └── venv/
│
├── frontend-react/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md (root)

```

---

## 9. Future Enhancements
- Add explainability (“why this team”)
- Add charts and graphs for score trends
- Add authentication and roles
- Add Slack/email notifications

---

## 10. Conclusion
VectorMatrix provides:
- Automated triage
- ML-powered similarity engine
- Clean UI dashboard
- Extendable architecture

This forms a scalable foundation for organizational AI query routing.
