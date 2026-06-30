from fastapi import FastAPI, HTTPException

tags_metadata = [
    {
        "name": "Genel",
        "description": "API endpoint listesi"
    },
    {
        "name": "Eğitimler",
        "description": "Eğitimler endpoint listesi"
    },
]

app = FastAPI(title = "Turkcell FastAPI Eğitimi", 
              description="Turkcell Eğitimi için Endpoint Listesi", 
              version="1.2.3",
              openapi_tags = tags_metadata)

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

@app.get(
        "/",
        tags = ["Genel"],
        summary="Endpoint özeti",
        description="Endpoint Açıklaması"
        )
def home():
    return {"message": "FastAPI eğitim platformu API"}

@app.get(
        "/courses",
        tags = ["Eğitimler"],
        )
def list_courses():
    return courses

@app.get("/courses/{course_id}",tags = ["Eğitimler"])
def get_course(course_id: int):

    for course in courses:
        if course["id"] == course_id:
            return course
        
    raise HTTPException(
        status_code=404,
        detail = "Eğitim listede bulunamadı."
    )

"""
200: başarılı
201: oluşturuldu
400: hatalı istek
401: giriş yapılmamış
403: yeti hatası
404: kayıt bulunamadı
422: validation hatası
500: sunucu hatası
"""