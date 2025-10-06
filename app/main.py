from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app import database, crud
from app.models.intents import Intent
from app.models.conversation import User, Message
from pydantic import BaseModel
import joblib
from app.routers import chat 

app = FastAPI(title="ML Chatbot")

# Include router
app.include_router(chat.router)


# Seed intents
@app.on_event("startup")
def startup_event():
    db = next(database.get_db())
    crud.seed_intents(db, "data/intents.json")


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the ML Chatbot API!"}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
