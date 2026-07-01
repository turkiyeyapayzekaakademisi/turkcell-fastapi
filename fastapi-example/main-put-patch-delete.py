"""
PUT mevcut bir kaynağı güncellemek için kullanılır. 

{
    "id":1,
    "price": 250
}

{
    "id":1,
    "price": 500
}

"""
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title = "FastAPI Eğitim Platformu API - PUT",
    description="FastAPI ile modern backend geliştirme",
    version="1.2.3"
)

class CourseLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced" 

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., min_length=5, max_length=50)
    level: CourseLevel
    price: float = Field(..., ge = 0)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    level: CourseLevel
    price: float

class CoursePatch(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=50)
    description: str | None = Field(None, min_length=5, max_length=50)
    level: CourseLevel | None = None
    price: float | None = Field(None, ge = 0)

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
    },
    {
        "id": 3,
        "title": "Makine Öğrenmesi",
        "description": "Scikit-learn ile makine öğrenmesi modelleri",
        "level": "intermediate",
        "price": 400
    }
]

@app.put("/courses/{course_id}", response_model=CourseResponse) # /courses/{course_id} adresine PUT isteği gelirse bu fonksiyon çalışsın 
def update_course(course_id: int, updated_course: CourseCreate):
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            course_data = {
                "id": course_id,
                "title": updated_course.title,
                "description": updated_course.description,
                "level": updated_course.level,
                "price": updated_course.price
            }

            courses[index] = course_data

            return course_data
    
    raise HTTPException(status_code=404, detail = "Eğitim bulunamadı.")


def find_course_index(course_id: int) -> int:
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            return index
    raise HTTPException(status_code=404, detail = "Eğitim bulunamadı")

@app.patch("/courses/{course_id}", response_model = CourseResponse)
def patch_course(course_id: int, patch_data: CoursePatch):

    course_index = find_course_index(course_id)

    existing_course = courses[course_index]

    update_data = patch_data.model_dump(exclude_unset=True)
    existing_course.update(update_data)

    courses[course_index] = existing_course

    return existing_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    course_index = find_course_index(course_id)

    deleted_course = courses.pop(course_index)

    return {
        "message": "silindi",
        "deleted_course": deleted_course
    }