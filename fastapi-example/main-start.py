from fastapi import FastAPI

app = FastAPI() # fastapi uygulamasını başlat

@app.get("/") # endpoint: kullanıcı / adresine get isteği gönderirse, hemen altındaki home fonksiyonu çağrılır
def home():
    return { # home return eder
        "message": "FastAPI Eğitimine hoş geldiniz."
    }

@app.get("/kcy")
def bu_fonksiyon_ismi_sacma_olabilir():
    return {
        "deneme": "zaaaa",
        "sonuc": 200,
        "hadi bir de array olsun": [1,2,3,3]
    }

# Path parameter: kullanıcının url içerisinde bir değer göndermesini sağlayan parametrelerden bir tanesi
@app.get("/courses/{course_id}")
def get_course(course_id: int) -> dict:
    return {
        "course_id": course_id,
        "title": "Yapay Zeka için Python Programlama"
    }

# Query Parameter: genellikle filtreleme, arama, sıralama ve sayfalama için kullanılır
@app.get("/courses")
def list_courses(level: str | None = None, limit: int = 10):

    return {
        "level": level,
        "limit": limit,
        "courses": [
            {"id": 1, "title": "yapay zeka için fastapi", "level": "beginner" },
            {"id": 2, "title": "veri bilim", "level": "int" }
        ]
    }