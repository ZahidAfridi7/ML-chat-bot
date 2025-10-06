from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.models.intents import Intent
from app.models.conversation import User, Message
from pydantic import BaseModel
import joblib
import os

# Load trained ML model
model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "intent_classifier.joblib")
model = joblib.load(model_path)

router = APIRouter(prefix="/v1",tags=["Chat"])

# Pydantic models
class ChatRequest(BaseModel):
    username: str
    text: str

class ChatResponse(BaseModel):
    response: str

# POST /chat endpoint
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Predict intent with confidence
    probs = model.predict_proba([request.text])[0]
    predicted_intent = model.classes_[probs.argmax()]
    confidence = probs.max()
    threshold = 0.6

    if confidence < threshold:
        response_text = "Sorry, I didn't understand that. Can you rephrase?"
        fallback_intent = None
    else:
        intent_obj = db.query(Intent).filter(Intent.intent == predicted_intent).first()
        response_text = intent_obj.response if intent_obj else "Sorry, I didn't understand that."
        fallback_intent = predicted_intent

    # Save message
    crud.save_message(db, request.username, request.text, response_text)

    # Save low-confidence messages for dataset expansion
    if confidence < threshold:
        with open("app/ml/new_data.json", "a", encoding="utf-8") as f:
            f.write(f'{{"text": "{request.text}", "intent": "unknown"}}\n')

    return {"response": response_text}

# GET /history endpoint
@router.get("/history")
def get_history(username: str = Query(...), db: Session = Depends(get_db)):
    user = crud.get_or_create_user(db, username)
    messages = db.query(Message).filter(Message.user_id == user.id).order_by(Message.timestamp).all()
    return [{"text": m.text, "response": m.response, "timestamp": m.timestamp} for m in messages]
