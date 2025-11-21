from flask import Flask, request, jsonify
import json, uuid, threading
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)
CORS(app)

DB_FILE = Path("teams_details.json")
LOCK = threading.Lock()

def read_db():
    with LOCK:
        if not DB_FILE.exists():
            DB_FILE.write_text("[]")
        return json.loads(DB_FILE.read_text())

def write_db(data):
    with LOCK:
        DB_FILE.write_text(json.dumps(data, indent=2))

def read_processed():
    f = Path("team_processed_details.json")
    with LOCK:
        if not f.exists():
            f.write_text("[]")
        return json.loads(f.read_text())

def write_processed(data):
    with LOCK:
        Path("team_processed_details.json").write_text(json.dumps(data, indent=2))

# -----------------------------
#  PREPROCESSING LOGIC
# -----------------------------
def preprocess_team(raw_team):
    processed = {
        "id": raw_team["id"],
        "team_name_upper": raw_team["team_name"].upper(),
        "owner_short": raw_team["full_name"].split()[0],
        "email_domain": raw_team["email"].split("@")[-1],
        "manager_is_owner": raw_team["manager_name"].lower() == raw_team["full_name"].lower(),
        "documents_count": len(raw_team["documents"])
    }
    return processed


# -----------------------------
#  API ROUTES
# -----------------------------
@app.get("/api/teams")
def get_all():
    return jsonify(read_db())

@app.post("/api/teams")
def create():
    data = request.json

    new_team = {**data, "id": str(uuid.uuid4())}

    # Save raw
    db = read_db()
    db.append(new_team)
    write_db(db)

    # Preprocess
    processed = preprocess_team(new_team)

    # Save processed
    proc = read_processed()
    proc.append(processed)
    write_processed(proc)

    return jsonify({"raw": new_team, "processed": processed}), 201


@app.get("/api/team/<id>")
def get_one(id):
    for t in read_db():
        if t["id"] == id:
            return jsonify(t)
    return jsonify({"error":"not found"}),404


@app.put("/api/team/<id>")
def update(id):
    db = read_db()
    for i,t in enumerate(db):
        if t["id"] == id:
            db[i] = {**request.json, "id": id}
            write_db(db)
            return jsonify(db[i])
    return jsonify({"error":"not found"}),404


@app.delete("/api/team/<id>")
def delete(id):
    db = read_db()
    db = [t for t in db if t["id"] != id]
    write_db(db)
    return jsonify({"status":"deleted"})


# New processed data endpoints
@app.get("/api/processed")
def get_processed():
    return jsonify(read_processed())


@app.get("/api/processed/<id>")
def get_processed_one(id):
    for item in read_processed():
        if item["id"] == id:
            return jsonify(item)
    return jsonify({"error":"not found"}),404


if __name__=="__main__":
    app.run(debug=True)
