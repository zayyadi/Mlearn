from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import gender, get_estimated_bmi

import pickle

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

model = pickle.load(open('bmi_model.pickle','rb'))

@app.get("/")
async def home(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/ht_predict')
def ht_predict(request:Request):
        output = "enter your detail"
        return templates.TemplateResponse("index.html",{"request": request, "output": output})

# @app.post('/ht_predict', response_class=HTMLResponse)
# def ht_predict(request:Request,Gender: str, weight_in_kg: int, height_sqr: float ):
#     input = get_estimated_bmi(Gender,weight_in_kg, height_sqr)
#     pred = model.predict(input)
#     print(pred)
#     output = pred
#     return templates.TemplateResponse(
#     "index.html",{"request": request, "output": output},prediction_text=
#     'Your predicted BMI is {}'.format(output))

@app.get('/get_gender')
def get_gender():
    response = gender()
    return response

@app.post('/predict_bmi')
def predict_bmi(gender: str=Form(...), weight_in_kg: int =Form(...), height_sqr: float =Form(...)):
    response = jsonable_encoder({"get_estimated_bmi":get_estimated_bmi(gender,weight_in_kg,height_sqr)})
    return JSONResponse(response)