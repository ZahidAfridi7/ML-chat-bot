from sqlalchemy.orm import Session
from app.models.intents import Intent
from app.models.conversation import User, Message
import json

# Seed intents
def seed_intents(db: Session, json_file: str):
    with open(json_file, "r") as f:
        intents = json.load(f)
        for intent in intents:
            db_intent = Intent(
                intent=intent["intent"],
                text=intent["text"],
                response=intent["response"]
            )
            db.add(db_intent)
        db.commit()

# Get response from intents
def get_response(db: Session, user_input: str) -> str:
    intents = db.query(Intent).all()
    for intent in intents:
        if intent.text.lower() in user_input.lower():
            return intent.response
    return "Sorry, I didn't understand that."

# Create or get user
def get_or_create_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# Save message to DB
def save_message(db: Session, username: str, text: str, response: str):
    user = get_or_create_user(db, username)
    message = Message(user_id=user.id, text=text, response=response)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
