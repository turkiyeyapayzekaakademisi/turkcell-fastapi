"""
1. Kullanıcıdan soru al
2. Gemini 2.5 Flash'a gönderelim
3. Gelen cevabı alalım
4. Soru ve cevabı SQLite a kaydet
5. Cevabı API response olarak dön
"""

from pathlib import Path
import os
import sqlite3

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio

load_dotenv()

DB_PATH = Path("questions.db")
MODEL_NAME = "gemini-2.5-flash"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise HTTPException("Gemini API KEY bulunamadı.")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(
    title = "FastAPI Gemini Backend"
)

class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)

class AskResponse(BaseModel):
    id: int
    question: str
    answer: str
    model: str
    created_at: str | None = None

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    return dict(row) if row else None

def save_question_answer(question: str, answer: str, model: str) -> int:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO questions (question, answer, model)
        VALUES (?, ?, ?)
        """, (
            question, answer, model
        )
    )

    new_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return new_id

def get_question_answer_by_id(question_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """ 
        SELECT id, question, answer, model, created_at
        FROM questions
        WHERE id = ?
        """, (question_id, )
    )

    row = cursor.fetchone()
    conn.close()

    return row_to_dict(row)

# new_id = save_question_answer(question = "merhaba sen kimsin", answer = "ben google gemini asistanıyım", model = "google gemini")
# print(get_question_answer_by_id(new_id))

@app.get("/")
def home():
    return {
        "message": "fastapi gemini backend çalışıyor"
    }

@app.post("/ask", response_model=AskResponse)
def ask_gemini(request: AskRequest):

    print("istek geldi")

    try:
        response = client.models.generate_content(
            model = MODEL_NAME,
            contents= request.question
        )

        answer = response.text

        if not answer:
            raise HTTPException(status_code=500, detail="gemini boş cevap döndürdü")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    new_id = save_question_answer(
        question=request.question,
        answer=answer,
        model=MODEL_NAME
    )

    saved_record = get_question_answer_by_id(new_id)

    return saved_record

@app.post("/ask-async")
async def ask_gemini(request: AskRequest):

    print("İstek geldi: ", datetime.now().strftime("%H:%M:%S.%f"))

    await asyncio.sleep(1)
    
    try:
        response = await client.aio.models.generate_content(
            model = MODEL_NAME,
            contents= request.question
        )

        answer = response.text

        if not answer:
            raise HTTPException(status_code=500, detail="gemini boş cevap döndürdü")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    print("Cevap döndü: ", datetime.now().strftime("%H:%M:%S.%f"))

    return {
        "question": request.question,
        "answer": answer
    }