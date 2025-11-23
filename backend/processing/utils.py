import json
import threading
from pathlib import Path

LOCK = threading.Lock()

def safe_read(path: Path):
    with LOCK:
        if not path.exists():
            path.write_text("[]")
        return json.loads(path.read_text())

def safe_write(path: Path, data):
    with LOCK:
        path.write_text(json.dumps(data, indent=2))
