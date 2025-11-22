# VectorMatrix — Interface Specification

Includes: Machine & human readable interface specs (Markdown), JSON Schemas, and OpenAPI (YAML).

Reference file uploaded by user: /mnt/data/README.md

---

## 1. Purpose
This document defines all data structures, metadata, API contracts, and interactions between frontend and backend for the VectorMatrix project.

It is split into:
- Data model descriptions (JSON objects)
- API endpoint contracts (request/response examples)
- Metadata interactions (how fields change through pipeline)
- File-level interactions (where JSON files live)

---

## 2. Data Models (Human readable)

### Team (raw) — `teams_details.json`
```json
{
  "id": "uuid",
  "full_name": "John Doe",
  "email": "john@example.com",
  "team_name": "MPLAB Tools Team",
  "manager_name": "Arjun",
  "documents": [
    "https://repo.example/doc1",
    "https://drive.example/doc2"
  ]
}
```
- `id` — unique identifier (uuid).
- `documents` — array of strings (URLs or short text descriptors).

### Team (processed) — `team_processed_details.json`
```json
{
  "id": "uuid",
  "team_name": "MPLAB Tools Team",
  "owner": "John Doe",
  "manager": "Arjun",
  "skills": ["embedded","c"],
  "tools": ["mplab","icd"],
  "work_areas": ["development_tools"],
  "embedding": [0.123, -0.04, ...]
}
```
- `embedding` — array of floats (SBERT vector).

### Query (raw) — `queries_raw.json`
```json
{
  "id": "q-uuid",
  "title": "enum structire in C for Pic 16f877",
  "content": "I am trying to write firmware ...",
  "source": "reddit/pic_programming",
  "url": "https://reddit.com/...",
  "timestamp": 1762885134.0,
  "comments_count": 4
}
```

### Query (processed) — `queries_processed.json`
```json
{
  "id": "q-uuid",
  "clean_text": "enum structire in c for pic 16f877. i am trying ...",
  "keywords": ["c","embedded"],
  "embedding": [0.234, 0.543, ...]
}
```

### Match Result — `match_results.json`
```json
{
  "query_id": "q-uuid",
  "team_id": "uuid",
  "score": 0.83
}
```

---

## 3. JSON Schemas
A machine-readable set of JSON Schemas is provided in `interface_schemas.json` (same folder as this file). Use them for validation and contracts.

---

## 4. API Contracts (examples)
Base URL: `http://127.0.0.1:5000/api`

### Add Team
**POST** `/api/teams`
Request body: Team (raw) without `id`
Response: `201` with `{ "raw": <team_raw>, "processed": <team_processed> }`

### Get Teams
**GET** `/api/teams` → returns array of raw teams.

### Get Processed Teams
**GET** `/api/teams/processed` → returns array of processed teams.

### Add Query
**POST** `/api/queries` with raw query body (no id)
Response: `201` returns created raw query.

### Process Query
**POST** `/api/queries/process/<qid>` — generates processed entry with embedding.

### Match Query
**POST** `/api/match/<qid>` — returns match result object with `best_team` and full `ranking`.

### Dashboard endpoints
`GET /api/dashboard/matches` → simplified cards for UI  
`GET /api/dashboard/rankings/<qid>` → full ranking for given query

---

## 5. Metadata & Field Lifecycle (how fields transform)
1. Team created: `teams_details.json` (raw)
2. Immediately processed via `preprocess_team()` → adds `skills`, `tools`, `work_areas`, `embedding` → stored in `team_processed_details.json`
3. Query ingested to `queries_raw.json`
4. Query processed via `process_query()` → `queries_processed.json`
5. Match run `match_query()` uses processed lists to compute `match_results.json`

---

## 6. Example End-to-End (Concrete)
1. POST team raw (no id) → server assigns id `t-1` and stores both raw and processed.
2. POST query raw → server assigns `q-1`.
3. POST `/api/queries/process/q-1` → server adds processed embedding.
4. POST `/api/match/q-1` → server computes scores and writes to `match_results.json`.
5. UI calls `/api/dashboard/matches` → card shows `q-1` matched with `t-1` and score.

---

## 7. Files & Paths
Backend expects JSON files in `backend/` by default:
- `backend/teams_details.json`
- `backend/team_processed_details.json`
- `backend/queries_raw.json`
- `backend/queries_processed.json`
- `backend/match_results.json`

---

## 8. Validation & Integration Tips
- Validate embeddings length (384 floats) on ingest to avoid shape mismatch.
- Use JSON Schema file `interface_schemas.json` for CI validation.
- For frontend, always call processed endpoints (`/api/teams/processed`) when you need embeddings or tools lists.

---


## 9. References
- Project README (uploaded): [README](./README.md)
