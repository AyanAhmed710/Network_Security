import os
import sys
import json 
from dotenv import load_dotenv
import pymongo
from network_security.exception.exception import NetworkSecuritySystem
from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request,FastAPI,UploadFile,File
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from network_security.utils.main_utils.utils import load_object

from network_security.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME

from network_security.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

from network_security.utils.ml_utils.model.estimator import Network_Model


load_dotenv()

import certifi
ca=certifi.where()

mongo_db_url=os.getenv("MONGODB_URL_KEY")

client=pymongo.MongoClient(mongo_db_url)

database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

@app.get("/" ,tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is Successful")
    except Exception as e:
        raise NetworkSecuritySystem(e,sys)
    

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        from io import BytesIO
        import os

        # Read CSV
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))

        preprocessor = load_object("Final_Model/preprocessing.pkl")
        model = load_object("Final_Model/model.pkl")

        network_model = Network_Model(preprocessor, model)
        y_pred = network_model.predict(df)

        df["predict_column"] = y_pred

        # Ensure folder exists
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        # Convert to HTML for template
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecuritySystem(e, sys)


    

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)

    
    