Sanal Ortam Kurulumu ve Aktivasyonu:
Windows:
    python -m venv venv
    .\venv\Scripts\activate
Mac / Linux:
    python3 -m venv venv
    source venv/bin/activate

Kütüphane Kurulumu:
Windows: pip install -r requirements.txt
Mac: pip3 install -r requirements.txt

Optional:
    Windows: pip freeze > requirements.txt
    Mac: pip3 freeze > requirements.txt