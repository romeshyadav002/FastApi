from fastapi import FastAPI, File, Query, UploadFile
from pydantic import BaseModel
from typing import List
import numpy as np
import pandas as pd
import io
from services.stats import get_csv_statistics
from services.number_analysis import analyze_numbers
from services.csv_filter import filter_csv_by_column


app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str
    origin: str

teas: List[Tea] = []


@app.get("/")
def read_root():
    return {"message":"welcome to chai code"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def add_tea(tea :Tea):
    teas.append(tea)
    return tea

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea : Tea):
    for index,tea in enumerate(teas):
        if tea.id == tea_id:
            teas[index] = updated_tea
            return updated_tea
    return {"error" : "Tea not found"}

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index,tea in enumerate(teas):
        if tea.id == tea_id:
            deleted = teas.pop(index)
            return deleted
    return {"error" : "Tea not found"}

class NumbersList(BaseModel):
    numbers: list[float]

@app.post("/stats/")
def get_numpy_stats(payload: NumbersList):
    arr = np.array(payload.numbers)
    return {
        "sum": float(np.sum(arr)),
        "mean": float(np.mean(arr)),
        "std_dev": float(np.std(arr)),
    }

# --------- Upload CSV and get column stats ---------
@app.post("/csv-stats/")
async def get_csv_stats(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    
    summary = df.describe().to_dict()
    return {
        "columns": df.columns.tolist(),
        "summary": summary
    }

class NumbersInput(BaseModel):
    numbers: list[float]

@app.post("/analyze-numbers/")
def analyze(numbers: NumbersInput):
    return analyze_numbers(numbers.numbers)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    return get_csv_statistics(content)

@app.post("/filter-csv/")
async def filter_csv(
    file: UploadFile = File(...),
    column: str = Query(...),
    value: str = Query(...)
):
    content = await file.read()
    return filter_csv_by_column(content, column, value)