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

def get_cur_id(db,model):
    if db.query(model).order_by(text("id desc")).first():
        return db.query(model).order_by(text("id desc")).first().id + 1
    else:
        return 1

@app.post("/api/submitData")
def submitData(data=Body(), db: Session = Depends(get_db)):
     current_date = datetime.now()
     raw_data = json.dumps({k: v for k, v in data.items() if k != "images"})

     usid = get_cur_id(db,Users)

     user = Users(id = usid,
                  email = data["user"]["email"],
                  phone = data["user"]["phone"],
                  fam   = data["user"]["fam"],
                  name  = data["user"]["name"],
                  otc   = data["user"]["otc"])
     db.add(user)

     chid = get_cur_id(db,Choords)
     choords = Choords(id = chid,
                       latitude  = data["coords"]["latitude"],
                       longitude = data["coords"]["longitude"],
                       height    = data["coords"]["height"])
     db.add(choords)

     id = get_cur_id(db,Pereval_added)
     pereval = Pereval_added(id = id,
                             beautyTitle=data["beauty_title"],
                             title=data["title"],
                             other_titles=data["other_titles"],
                             connect=data["connect"],
                             user=usid,
                             choords=chid,
                             level_winter=data["level"]["winter"],
                             level_summer=data["level"]["summer"],
                             level_autumn=data["level"]["autumn"],
                             level_spring=data["level"]["spring"],
                             date_added=current_date)
     db.add(pereval)
     for img in data["images"]:
         imid = get_cur_id(db,Pereval_images)
         pereval_images = Pereval_images(id=imid,
                                         title = img["title"],
                                         date_added=current_date,
                                         img=img["data"])
         pimid = get_cur_id(db,Pereval_pereval_images)
         Ppimages = Pereval_pereval_images(id=pimid,
                                           id_pereval=id,
                                           id_image=imid)
         db.add(Ppimages)

     db.commit()
     return json.dumps({ "status": 200, "message": 'null', "id": pereval.id })


