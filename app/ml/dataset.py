import json
from sqlalchemy.orm import Session
from app.models.intents import Intent
from app.database import SessionLocal

def load_intents_from_json(json_file="data/intents.json"):
    with open(json_file, "r") as f:
        data = json.load(f)
    texts = [item["text"] for item in data]
    labels = [item["intent"] for item in data]
    return texts, labels

def load_intents_from_db(db: Session):
    intents = db.query(Intent).all()
    texts = [intent.text for intent in intents]
    labels = [intent.intent for intent in intents]
    return texts, labels

# Example usage
if __name__ == "__main__":
    db = SessionLocal()
    texts, labels = load_intents_from_json()
    print(texts, labels)
