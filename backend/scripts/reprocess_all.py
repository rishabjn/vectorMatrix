#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
from processing.preprocess_team import preprocess_team
from processing.preprocess_query import preprocess_query
from processing.rebuild_matches import rebuild_matches
# Import backend helpers
from app import (
    safe_read,
    safe_write,
    DB_FILE,
    PROCESSED_FILE,
    QUERIES_RAW_FILE,
    QUERIES_PROCESSED_FILE,
    MATCH_RESULTS_FILE,
    embed_text,
    extract_entities,
)

print("\n========================")
print(" VECTOR MATRIX — REPROCESSING PIPELINE")
print("========================\n")

# ----------------------------------------------
# Step 1 — Rebuild PROCESSED TEAMS
# ----------------------------------------------
def rebuild_teams():
    print("→ Rebuilding processed teams...")

    raw_teams = safe_read(DB_FILE)
    processed = []

    for t in raw_teams:
        processed.append(preprocess_team(t))

    safe_write(PROCESSED_FILE, processed)
    print(f"✔ Processed teams: {len(processed)}\n")


# ----------------------------------------------
# Step 2 — Rebuild PROCESSED QUERIES
# ----------------------------------------------
def rebuild_queries():
    print("→ Rebuilding processed queries...")

    raw_queries = safe_read(QUERIES_RAW_FILE)
    processed = []

    for q in raw_queries:
        text_blob = f"{q['title']} . {q['content']}"
        emb = embed_text(text_blob)
        entities = extract_entities(text_blob)

        processed.append({
            "id": q["id"],
            "clean_text": text_blob.lower(),
            "keywords": entities["skills"],
            "embedding": emb
        })

    safe_write(QUERIES_PROCESSED_FILE, processed)
    print(f"✔ Processed queries: {len(processed)}\n")


# ----------------------------------------------
# Step 3 — Rebuild MATCH RESULTS
# ----------------------------------------------
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def rebuild_matches():
    print("→ Rebuilding match results...")

    queries = safe_read(QUERIES_PROCESSED_FILE)
    teams = safe_read(PROCESSED_FILE)

    results = []

    for q in queries:
        q_emb = q["embedding"]
        ranking = []

        for t in teams:
            sim = cosine_similarity(q_emb, t["embedding"])
            ranking.append({
                "team_id": t["id"],
                "team_name": t["team_name"],
                "score": sim
            })

        ranking.sort(key=lambda x: x["score"], reverse=True)
        best = ranking[0]

        results.append({
            "query_id": q["id"],
            "team_id": best["team_id"],
            "score": best["score"],
            "ranking": ranking
        })

    safe_write(MATCH_RESULTS_FILE, results)
    print(f"✔ Match results rebuilt: {len(results)}\n")


# ----------------------------------------------
# RUN PIPELINE
# ----------------------------------------------
if __name__ == "__main__":
    print("Running full reprocess pipeline...\n")

    rebuild_teams()
    rebuild_queries()
    rebuild_matches()

    print("========================")
    print(" ✔ REPROCESS COMPLETE")
    print("========================\n")
    print("Updated files:")
    print(f" - {DB_FILE.name}")
    print(f" - {PROCESSED_FILE.name}")
    print(f" - {QUERIES_RAW_FILE.name}")
    print(f" - {QUERIES_PROCESSED_FILE.name}")
    print(f" - {MATCH_RESULTS_FILE.name}\n")


# def run_reprocess_pipeline():
#     print("🔄 Auto-Reprocess Triggered...")
#     rebuild_teams()
#     rebuild_queries()
#     rebuild_matches()
#     print("✔ Auto-Reprocess Complete")