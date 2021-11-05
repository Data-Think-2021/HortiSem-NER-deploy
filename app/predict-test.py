import requests

url = "http://localhost:8000/predict"



response = requests.post(url, pdf).json()
print(response)

