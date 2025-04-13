from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import numpy as np
import pandas as pd
import io


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