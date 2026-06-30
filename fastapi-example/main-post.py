"""
POST: Veri ekleme

Kullanıcıdan JSON Body almamız lazım ve bunu almak için Pydantic model kullanırız
    {
        "title": ...,
        "description": ...
    }
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from enum import Enum

app = FastAPI()

class CourseLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    level: CourseLevel
    price: float = Field(..., ge=0)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    level: CourseLevel
    price: float

courses = [
    {
        "id": 1,
        "title": "Yapay Zeka için Python",
        "description": "Yapay zeka ve veri bilimi için Python temelleri",
        "level": "beginner",
        "price": 250
    },
    {
        "id": 2,
        "title": "Veri Bilimi",
        "description": "Pandas, NumPy, veri analizi ve görselleştirme",
        "level": "intermediate",
        "price": 350
    }
]

@app.get("/")
def home():
    return {"message": "FastAPI eğitim platformu"}

@app.get("/courses")
def list_courses():
    return courses

@app.post("/courses", response_model=CourseResponse)
def create_course(course: CourseCreate):

    new_course = {
        "id": len(courses) + 1,
        "title": 10,
        "description": course.description,
        "level": course.level,
        "price": course.price,
    } 

    # validate response
    try:
        validated_course = CourseResponse(**new_course)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail = "Çıktı response modeline uygun değil")

    courses.append(validated_course.model_dump())

    return validated_course
