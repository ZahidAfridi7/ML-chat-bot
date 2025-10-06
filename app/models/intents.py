from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.database import Base

class Message(BaseModel):
    text: str

class Response(BaseModel):
    response: str


class Intent(Base):
    __tablename__ = "intents"

    id = Column(Integer, primary_key=True, index=True)
    intent = Column(String, index=True)
    text = Column(String, index=True)
    response = Column(String)
