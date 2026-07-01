from enum import Enum
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

DB_PATH = Path("courses.db")

app = FastAPI()

class CourseLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    level: CourseLevel
    price: float = Field(..., ge=0)

class CourseUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    level: CourseLevel
    price: float = Field(..., ge=0)

class CoursePatch(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=10)
    level: CourseLevel | None = None
    price: float | None = Field(None, ge=0)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    level: CourseLevel
    price: float
    created_at: str | None = None
    updated_at: str | None = None

def get_connection():
    """SQLite bağlantısı oluşturur."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    """
    sqlite row unu python da dictionary e çevir
    """
    return dict(row) if row else None

def get_course_or_404(course_id: int):
    """
    id ye göre eğitim getirir yoksa 404 hatası verir.
    """
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, description, level, price, created_at, updated_at
        FROM courses
        WHERE id = ?
        """, (course_id,)
    )

    row = cursor.fetchone()
    conn.close()

    course = row_to_dict(row)

    if course is None:
        raise HTTPException(status_code=404, detail = "Eğitim bulunamadı")

    return course

@app.get("/")
def home():
    return{
        "message": "FastAPI SQLite CRUD API"
    }

@app.get("/courses", response_model=list[CourseResponse])
def list_courses():
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, description, level, price, created_at, updated_at
        FROM courses
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]

@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    return get_course_or_404(course_id)

@app.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO courses (title, description, level, price)
        VALUES (?, ?, ?, ?)
        """, (
            course.title,course.description,course.level,course.price
        )
    )

    new_course_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_course_or_404(new_course_id)

# PUT eğitimin komple güncellenmesi
@app.put("/courses/{course_id}", response_model = CourseResponse)
def update_course(course_id: int, course: CourseUpdate):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE courses
        SET title = ?,
            description = ?,
            level = ?,
            price = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (
            course.title,
            course.description,
            course.level.value,
            course.price,
            course_id
        )
    )

    conn.commit()
    conn.close()

    return get_course_or_404(course_id)

# PATCH 
@app.patch("/courses/{course_id}", response_model= CourseResponse)
def patch_coruse(course_id: int, patch_data: CoursePatch):
     
    course = get_course_or_404(course_id)

    update_data = patch_data.model_dump(exclude_unset=True)

    course.update(update_data)

    level_value = course["level"]

    if isinstance(level_value, CourseLevel):
        level_value = level_value.value

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE courses
        SET title = ?,
            description = ?,
            level = ?,
            price = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (
            course["title"],
            course["description"],
            level_value,
            course["price"],
            course_id
        )
    )

    conn.commit()
    conn.close()

    return get_course_or_404(course_id)

# delete
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):

    course = get_course_or_404(course_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM courses
        WHERE id = ?
        """, (course_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Eğitim başarıyla silindi",
        "deleted_course": course

    }