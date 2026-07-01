import requests

response = requests.post("http://127.0.0.1:8000/ask", json = {"question": "yapay zeka nedir 1 cümle ile anlat."})

print(response.status_code)
print(response.json())