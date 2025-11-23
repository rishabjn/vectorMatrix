import json
import uuid
import threading
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import numpy as np
# from scripts.reprocess_all import run_reprocess_pipeline

# # After saving team or query:
# run_reprocess_pipeline()
# -------------------------------------------------
# Paths & Setup
# -------------------------------------------------

BASE = Path(__file__).resolve().parent

DB_TEAMS_DIR = BASE / "db" / "teams"
DB_QUERIES_DIR = BASE / "db" / "queries"
DB_MATCH_DIR = BASE / "db" / "matches"

DB_FILE = DB_TEAMS_DIR / "teams_details.json"
PROCESSED_FILE = DB_TEAMS_DIR / "team_processed_details.json"

QUERIES_RAW_FILE = DB_QUERIES_DIR / "queries_raw.json"
QUERIES_PROCESSED_FILE = DB_QUERIES_DIR / "queries_processed.json"

MATCH_RESULTS_FILE = DB_MATCH_DIR / "match_results.json"


LOCK = threading.Lock()

app = Flask(__name__)
CORS(app)

# Load SBERT model
print("Loading SBERT model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("SBERT loaded.")

# -------------------------------------------------
# Safe JSON Helpers
# -------------------------------------------------
def safe_read(path: Path):
    with LOCK:
        if not path.exists():
            path.write_text("[]")
        return json.loads(path.read_text())

def safe_write(path: Path, data):
    with LOCK:
        path.write_text(json.dumps(data, indent=2))

# -------------------------------------------------
# Keyword Extraction Rules
# -------------------------------------------------
SKILL_KEYWORDS = {
    "c": [" c ", "c language"],
    "c++": ["c++", "cpp"],
    "embedded": ["embedded", "firmware"],
    "linux": ["linux"],
    "testing": ["testing", "unit test"],
}

TOOL_KEYWORDS = {
    "mplab": ["mplab", "mplab x"],
    "icd": ["icd3", "icd4"],
    "git": ["git", "github"],
}

WORK_AREA_KEYWORDS = {
    "development_tools": ["ide", "development tools"],
    "hardware": ["schematic", "pcb"],
}

def extract_entities(text):
    if not text:
        return {"skills": [], "tools": [], "work_areas": []}

    txt = text.lower()

    def find_keys(map_):
        results = set()
        for key, vals in map_.items():
            for v in vals:
                if v in txt:
                    results.add(key)
        return sorted(results)

    return {
        "skills": find_keys(SKILL_KEYWORDS),
        "tools": find_keys(TOOL_KEYWORDS),
        "work_areas": find_keys(WORK_AREA_KEYWORDS),
    }

# -------------------------------------------------
# Embedding Helper
# -------------------------------------------------
def embed_text(text):
    emb = model.encode(text, show_progress_bar=False)
    return emb.tolist()

# -------------------------------------------------
# TEAM PROCESSING
# -------------------------------------------------
def preprocess_team(raw):
    parts = [
        raw.get("team_name", ""),
        raw.get("full_name", ""),
        raw.get("manager_name", "")
    ]

    docs = raw.get("documents", [])
    parts.extend(docs)

    text_blob = " | ".join([p for p in parts if p])

    entities = extract_entities(text_blob)
    emb = embed_text(text_blob)

    return {
        "id": raw["id"],
        "team_name": raw.get("team_name"),
        "owner": raw.get("full_name"),
        "manager": raw.get("manager_name"),
        "skills": entities["skills"],
        "tools": entities["tools"],
        "work_areas": entities["work_areas"],
        "embedding": emb
    }

# -------------------------------------------------
# TEAM ROUTES (GET + POST merged to prevent 405)
# -------------------------------------------------
@app.route("/api/teams", methods=["GET", "POST"])
def teams_handler():
    if request.method == "GET":
        return jsonify(safe_read(DB_FILE))

    # POST: Add new team
    body = request.json or {}

    tid = str(uuid.uuid4())
    raw_team = {
        "id": tid,
        "full_name": body.get("full_name"),
        "email": body.get("email"),
        "team_name": body.get("team_name"),
        "manager_name": body.get("manager_name"),
        "documents": body.get("documents", []),
    }

    # Save raw
    raw_db = safe_read(DB_FILE)
    raw_db.append(raw_team)
    safe_write(DB_FILE, raw_db)

    # Save processed
    processed = preprocess_team(raw_team)
    proc_db = safe_read(PROCESSED_FILE)
    proc_db.append(processed)
    safe_write(PROCESSED_FILE, proc_db)

    return jsonify({"raw": raw_team, "processed": processed}), 201

@app.get("/api/teams/processed")
def get_processed_teams():
    return jsonify(safe_read(PROCESSED_FILE))

# -------------------------------------------------
# QUERY INGESTION (RAW)
# -------------------------------------------------
@app.post("/api/queries")
def ingest_query():
    body = request.json or {}

    qid = "q-" + str(uuid.uuid4())
    item = {
        "id": qid,
        "title": body.get("title", ""),
        "content": body.get("content", ""),
        "source": body.get("source", "unknown"),
        "url": body.get("url", ""),
        "timestamp": body.get("timestamp"),
        "comments_count": body.get("comments_count", 0)
    }

    raw_q = safe_read(QUERIES_RAW_FILE)
    raw_q.append(item)
    safe_write(QUERIES_RAW_FILE, raw_q)

    return jsonify(item), 201

# -------------------------------------------------
# QUERY PROCESSING (Embedding)
# -------------------------------------------------
@app.post("/api/queries/process/<qid>")
def process_query(qid):
    raw = safe_read(QUERIES_RAW_FILE)
    item = next((q for q in raw if q["id"] == qid), None)
    if not item:
        return jsonify({"error": "query not found"}), 404

    text_blob = f"{item['title']} . {item['content']}"
    emb = embed_text(text_blob)

    processed = {
        "id": qid,
        "clean_text": text_blob.lower(),
        "keywords": extract_entities(text_blob)["skills"],
        "embedding": emb
    }

    proc = safe_read(QUERIES_PROCESSED_FILE)
    proc.append(processed)
    safe_write(QUERIES_PROCESSED_FILE, proc)

    return jsonify(processed), 201

# -------------------------------------------------
# MATCHING ENGINE
# -------------------------------------------------
@app.post("/api/match/<qid>")
def match_query(qid):
    qlist = safe_read(QUERIES_PROCESSED_FILE)
    q = next((x for x in qlist if x["id"] == qid), None)
    if not q:
        return jsonify({"error": "query not processed yet"}), 400

    q_emb = np.array(q["embedding"])
    teams = safe_read(PROCESSED_FILE)

    if not teams:
        return jsonify({"error": "no teams in database"}), 400

    matches = []
    for t in teams:
        t_emb = np.array(t["embedding"])
        sim = float(np.dot(q_emb, t_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(t_emb)))
        matches.append({
            "team_id": t["id"],
            "team_name": t["team_name"],
            "score": sim
        })

    best = max(matches, key=lambda x: x["score"])

    # save match
    results = safe_read(MATCH_RESULTS_FILE)
    results.append({
        "query_id": qid,
        "team_id": best["team_id"],
        "score": best["score"]
    })
    safe_write(MATCH_RESULTS_FILE, results)

    return jsonify({
        "best_team": best,
        "ranking": sorted(matches, key=lambda x: x["score"], reverse=True)
    })

# -------------------------------------------------
# DASHBOARD ROUTES
# -------------------------------------------------
@app.get("/api/dashboard/matches")
def dashboard_matches():
    matches = safe_read(MATCH_RESULTS_FILE)
    queries = safe_read(QUERIES_RAW_FILE)
    teams = safe_read(PROCESSED_FILE)

    results = []
    for m in matches:
        q = next((x for x in queries if x["id"] == m["query_id"]), None)
        t = next((x for x in teams if x["id"] == m["team_id"]), None)

        if q and t:
            results.append({
                "query_id": q["id"],
                "query_title": q["title"],
                "team_id": t["id"],
                "team_name": t["team_name"],
                "score": m["score"]
            })

    return jsonify(results)

@app.get("/api/dashboard/rankings/<qid>")
def full_ranking(qid):
    q_list = safe_read(QUERIES_PROCESSED_FILE)
    q = next((x for x in q_list if x["id"] == qid), None)
    if not q:
        return jsonify({"error": "query not processed"}), 400

    q_emb = np.array(q["embedding"])
    t_list = safe_read(PROCESSED_FILE)

    results = []
    for t in t_list:
        t_emb = np.array(t["embedding"])
        sim = float(np.dot(q_emb, t_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(t_emb)))

        results.append({
            "team_id": t["id"],
            "team_name": t["team_name"],
            "score": sim
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results)



@app.get("/api/queries/raw")
def get_queries_raw():
    return jsonify(safe_read(QUERIES_RAW_FILE))

@app.get("/api/queries/processed")
def get_queries_processed():
    return jsonify(safe_read(QUERIES_PROCESSED_FILE))

@app.get("/api/matches")
def get_matches():
    return jsonify(safe_read(MATCH_RESULTS_FILE))

@app.get("/api/team/<tid>")
def get_single_team(tid):
    teams = safe_read(DB_FILE)
    team = next((t for t in teams if t["id"] == tid), None)
    if team:
        return jsonify(team)
    return jsonify({"error": "team not found"}), 404

@app.get("/api/team/processed/<tid>")
def get_single_team_processed(tid):
    teams = safe_read(PROCESSED_FILE)
    team = next((t for t in teams if t["id"] == tid), None)
    if team:
        return jsonify(team)
    return jsonify({"error": "team not found"}), 404

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/api/health")
def health():
    return {"ok": True}

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    # create directories if missing
    DB_TEAMS_DIR.mkdir(parents=True, exist_ok=True)
    DB_QUERIES_DIR.mkdir(parents=True, exist_ok=True)
    DB_MATCH_DIR.mkdir(parents=True, exist_ok=True)

    for p in [
        DB_FILE,
        PROCESSED_FILE,
        QUERIES_RAW_FILE,
        QUERIES_PROCESSED_FILE,
        MATCH_RESULTS_FILE
    ]:
        if not p.exists():
            p.write_text("[]")

    app.run(debug=True)

