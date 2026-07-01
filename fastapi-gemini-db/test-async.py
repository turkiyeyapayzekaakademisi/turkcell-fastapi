import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

API_URL = "http://127.0.0.1:8000/ask-async"

questions = [
    "Fastapi nedir. 1 cümle ile anlat.",
    "Fastapi nedir. 1 cümle ile anlat."
]

def send_request(question: str):

    start_time = datetime.now()

    payload = {
        "question": question
    }

    response = requests.post(API_URL, json = payload)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    return {
        "question": question,
        "status_code": response.status_code,
        "start_time": start_time.strftime("%H:%M:%S.%f")[:-3],
        "end_time": end_time.strftime("%H:%M:%S.%f")[:-3],
        "duration_second": duration,
        "response": response.json()
    }

with ThreadPoolExecutor(max_workers=2) as executer:
    results = executer.map(send_request, questions)

for index, result in enumerate(results, start = 1):
    print(f"İstek: {index}")
    print("Soru: ", result["question"])
    print("Status code: ", result["status_code"])
    print("start_time: ", result["start_time"])
    print("end_time: ", result["end_time"])
    print("duration_second: ", result["duration_second"])
    print("response: ", result["response"])

"""
İstek: 1
Soru:  Fastapi nedir. 5 cümle ile anlat.
Status code:  200
start_time:  14:36:25.457
end_time:  14:36:47.728
duration_second:  22.271415
response:  {'id': 12, 'question': 'Fastapi nedir. 5 cümle ile anlat.', 'answer': "İşte FastAPI'nin 5 cümlelik açıklaması:\n\n1.  FastAPI, Python ile modern, hızlı ve yüksek performanslı API'ler (uygulama programlama arayüzleri) oluşturmak için kullanılan açık kaynaklı bir web framework'üdür.\n2.  Python'ın tip ipuçlarından ve asenkron (async/await) yeteneklerinden tam olarak faydalanarak çok verimli ve ölçeklenebilir uygulamalar geliştirmeyi sağlar.\n3.  Pydantic kütüphanesini kullanarak otomatik veri doğrulama, serileştirme ve dokümantasyon oluşturma özellikleri sunar, bu da geliştirme sürecini hızlandırır.\n4.  API'niz için otomatik olarak interaktif Swagger UI ve ReDoc dokümantasyonu oluşturur, bu sayede API'nizi test etmek ve anlamak çok daha kolaylaşır.\n5.  Kolay kullanımı, güçlü özellikleri ve yüksek performansı sayesinde, mikroservislerden büyük ölçekli web uygulamalarına kadar geniş bir yelpazede tercih edilen modern bir çözümdür.", 'model': 'gemini-2.5-flash', 'created_at': '2026-07-01 11:36:47'}
İstek: 2
Soru:  Fastapi nedir. 5 cümle ile anlat.
Status code:  200
start_time:  14:36:25.457
end_time:  14:36:36.716
duration_second:  11.259266
response:  {'id': 11, 'question': 'Fastapi nedir. 5 cümle ile anlat.', 'answer': "FastAPI, Python ile modern, hızlı ve yüksek performanslı API'lar (web servisleri) oluşturmak için kullanılan açık kaynaklı bir web framework'üdür. Async/await desteği sayesinde oldukça hızlı çalışır ve yüksek eşzamanlı istekleri verimli bir şekilde yönetebilir. Python'ın tip ipuçlarını (type hints) kullanarak veri doğrulama, bağımlılık enjeksiyonu ve kod tamamlama gibi gelişmiş özellikler sunar. API'niz için otomatik olarak interaktif dokümantasyon (Swagger UI ve ReDoc) oluşturarak geliştirici deneyimini büyük ölçüde artırır. Bu özellikleri sayesinde hızlıca sağlam, güvenilir ve bakımı kolay web servisleri geliştirmek için ideal bir araçtır.", 'model': 'gemini-2.5-flash', 'created_at': '2026-07-01 11:36:36'}
"""