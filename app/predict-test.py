import requests
# import app

url = "http://localhost:5000/predict_pdf"
url_text = "http://localhost:5000/predict_text"

pdf_path = r"C:\Users\xia.he\Project\deployment_for_isip\app\upload_folder\GB14_2020.pdf"
pdf = {"my_file": open(pdf_path , "rb")}

text = {"text": "Tomate, Gurken, BBCH 12"}

res = requests.post(url, files=pdf)

# res = requests.post(url_text, json=text)

if res.ok:
    print("successfully")
    print(res.json())
else:
    print("error")

