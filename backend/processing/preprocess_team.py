from processing.utils import safe_read, safe_write
from app import embed_text, extract_entities

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
