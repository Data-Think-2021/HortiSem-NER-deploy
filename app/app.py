import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import spacy
# import joblib
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi import Request, Response
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn 

# crf_model = joblib.load("/model/nerCRF.joblib") 

app = FastAPI(
    title="{{HortiSem.Named_Entity_Recognition}}",
    version="0.0",
    description="{{HortiSem.project_short_description}}"
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

nlp = spacy.load(os.getcwd()+"/model/spacy_ml_rule_model")

UPLOAD_FOLDER = os.getcwd()+"/upload_folder"

def read_pdf(file_path):
    output_string = StringIO()
    with open(file_path, "rb") as in_file:
        parser = PDFParser(in_file)
        try: 
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                try: 
                    interpreter.process_page(page)
                except:
                    print("not able to read the pdf file")
                    pass
        except:
            print("not able to read pdf file")
            pass
        return_string = preprocess_pdf(output_string.getvalue())
    return return_string   

def preprocess_pdf(string):
    string_final = ""
    # print(string+"\n")
    bla = string.split("\n")
    for line in bla:
        string_final += line
    return string_final

def predict(text, nlp_model):
    doc = nlp_model(text)
    ents = []
    for ent in doc.ents:
        ents.append({"entity":ent.text, "label":ent.label_})    
    return {"ents":ents}

# def predict(text, nlp_model):
#     doc = nlp_model(text)
#     entities = {
#         "Kultur": [], 
#         "Erreger": [],
#         "Mittel": [],
#         "BBCH_Stadium": [],
#         "Ort": [],
#        }
#     for ent in doc.ents:
#         if ent.text in entities[ent.label_]:
#             pass
#         else:
#             entities[ent.label_].append(ent.text)
#     return entities

@app.post("/predict/")
async def create_upload_file(file: UploadFile = File(...)):  
    # the user can upload a pdf file or direct give text . 
    file_object = file.file
    #create empty file to copy the file_object to
    Pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    print(Pdf_path)
    # save the pdf file
    upload_folder = open(Pdf_path, 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
    # Process the text
    input_text = read_pdf(Pdf_path)
    # Predict
    ents = predict(input_text,nlp)
    # print(ents)
    return {"filename": file.filename, "text":input_text,"ents":ents["ents"]}

@app.get("/main/")
async def predict_text(text):
    ents = predict(text,nlp)
    # print(ents)
    return {"text":text,"ents":ents["ents"]}
   

@app.get("/")
def index():
    return "foo"   

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, debug=True)  