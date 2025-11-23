import numpy as np
from processing.utils import safe_read, safe_write

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def rebuild_matches(processed_queries_file, processed_teams_file, match_results_file):
    queries = safe_read(processed_queries_file)
    teams = safe_read(processed_teams_file)

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
        best_team = ranking[0]

        results.append({
            "query_id": q["id"],
            "team_id": best_team["team_id"],
            "score": best_team["score"],
            "ranking": ranking
        })

    safe_write(match_results_file, results)
    return len(results)
