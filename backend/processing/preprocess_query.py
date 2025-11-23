from processing.utils import safe_read, safe_write
from app import embed_text, extract_entities

def preprocess_query(raw_q):
    text_blob = f"{raw_q['title']} . {raw_q['content']}"
    emb = embed_text(text_blob)
    entities = extract_entities(text_blob)

    return {
        "id": raw_q["id"],
        "clean_text": text_blob.lower(),
        "keywords": entities["skills"],
        "embedding": emb
    }
