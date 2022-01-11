import spacy
import os
import shutil
import re
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from fastapi import FastAPI, File, UploadFile
from fastapi import Request, Response
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn 


app = FastAPI(
    title="{{HortiSem.Named_Entity_Recognition}}",
    version="0.0",
    description="{{HortiSem.project_short_description}}"
)

class Data(BaseModel):
    text: str
    
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

nlp = spacy.load(os.getcwd()+"/model/spacy_ml_rule_model")

# UPLOAD_FOLDER = os.getcwd()+"/upload_folder"

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

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path

def predict(text, nlp_model):
    doc = nlp_model(text)
    entities = {
        "Kultur": [], 
        "Erreger": [],
        "Mittel": [],
        "BBCH_Stadium": [],
        "Ort": [],
        "Auftreten":[]
       }
    for ent in doc.ents:
        new_ent = re.sub(r'\n\r?', ' ', ent.text)
        if ent.label_ == "Witterung" or ent.label_ == "Zeit":
            pass
        elif new_ent in entities[ent.label_]:
            pass
        else:
            entities[ent.label_].append(new_ent)
    return entities

@app.post("/predict_pdf/")
async def create_upload_file(file: UploadFile = File(...)):  
    tmp_path = save_upload_file_tmp(file)
    try:
        # Process the text
        input_text = read_pdf(tmp_path)
        # Predict
        ents = predict(input_text,nlp)
    finally:
        tmp_path.unlink() # delete the temp file
    
    return {"filename": file.filename, "text":input_text,"ents":ents}

@app.post("/predict_text/")
async def predict_text(data: Data):
    ents = predict(data.text,nlp)
    return {"text":data.text,"ents":ents}
   

if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True, debug=True)  