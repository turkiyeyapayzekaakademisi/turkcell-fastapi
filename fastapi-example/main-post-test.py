import requests

BASE_URL = "http://127.0.0.1:8000"

# ana sayfayı kontrol et
response = requests.get(f"{BASE_URL}/")
print(response.status_code)
print(response.json())

# eğitimleri listele
response = requests.get(f"{BASE_URL}/courses")
print(response.status_code)
print(response.json())

# yeni eğitim ekle
new_course = {
    "title": "Fastapi",
    "description": "Fastapi temelleri",
    "level": "beginner",
    "price": 100 
}

reponse = requests.post(f"{BASE_URL}/courses", json = new_course)
print(response.status_code)
print(response.json())

# eğitimleri listele
response = requests.get(f"{BASE_URL}/courses")
print(response.status_code)
print(response.json())