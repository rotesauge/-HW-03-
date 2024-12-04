from models import *
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import json

# создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()


# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/api/submitData")
def submitData():
    return "{ ""status"": 500, ""message"": ""Use POST methood"",""id"": 'null'}"



@app.post("/api/submitData")
def submitData(data=Body(), db: Session = Depends(get_db)):
     current_date = datetime.now()
     id = db.query(Pereval_added).order_by(text("id desc")).first().id+1
     raw_data = json.dumps({k: v for k, v in data.items() if k != "images"})
     pereval = Pereval_added(id = id, date_added=current_date, raw_data=raw_data, images="")
     db.add(pereval)
     db.commit()
     db.refresh(pereval)
     return json.dumps({ "status": 200, "message": 'null', "id": pereval.id })

