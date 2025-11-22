import json
from pathlib import Path
from app import preprocess_team, safe_read, safe_write, DB_FILE, PROCESSED_FILE

def main():
    raw = safe_read(DB_FILE)

    new_processed = []
    for team in raw:
        processed = preprocess_team(team)
        new_processed.append(processed)

    safe_write(PROCESSED_FILE, new_processed)
    print("Teams reprocessed successfully!")

if __name__ == "__main__":
    main()
