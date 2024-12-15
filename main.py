from sqlalchemy.dialects.postgresql import array

from models import *
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import Depends, FastAPI, Body
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from fastapi.responses import JSONResponse,FileResponse

# создаем таблицы
Base.metadata.create_all(bind=engine)
app = FastAPI()
#
#
# class UserClass(BaseModel):
#     email: str
#     fam: str
#     name: str
#     otc: str | None = None
#     phone: str | None = None
#     name: str
#     age: int | None = None
#
# class CoordsClass(BaseModel):
#     latitude: float
#     longitude: float
#     height: int
#
# class LevelClass(BaseModel):
#     winter: str | None = None
#     summer: str | None = None
#     autumn: str | None = None
#     spring: str | None = None
#
# class ImgClass(BaseModel):
#     data: str
#     title: str
#
# class submitDatаClass(BaseModel):
#     beauty_title: str
#     title: str
#     other_titles: str
#     connect: str
#     add_time: datetime
#     other_titles: str
#     user: UserClass
#     coords: CoordsClass
#     level: LevelClass
#     images: array[ImgClass]




@app.get("/openapi/")
async def main():
    return FileResponse("sw.html")

@app.get("/openapischema/")
async def main():
    return FileResponse("openapi-schema.yml")


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

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # Convert SQLAlchemy model to dictionary
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

@app.get("/api/submitData")
def submitDatа_gp(email, db: Session = Depends(get_db)):
    qres = db.query(Pereval_added).filter(Pereval_added.user ==  db.query(Users).filter(Users.email == email).first().id)
    newlist = [{"date_added"      : str(item.date_added),
                  "beautyTitle"     : item.beautyTitle,
                  "title"           : item.title,
                  "other_titles"    : item.other_titles,
                  "connect"         : item.connect,
                  "level_winter"    : item.level_winter,
                  "level_summer"    : item.level_summer,
                  "level_autumn"    : item.level_autumn,
                  "level_spring"    : item.level_spring,
                  "status"          : str(item.status)} for item in qres]
    return JSONResponse(content={"status": 200, "message": newlist, "id": 'null'})

@app.get("/api/submitData/{item_id}")
def submitDatа_g(item_id, db: Session = Depends(get_db)):
    per = db.query(Pereval_added).filter(Pereval_added.id == item_id).first()
    if per:
        choords = db.query(Choords).filter(Choords.id == per.choords).first()
        user = db.query(Users).filter(Users.id == per.user).first()
        choords_struct = {"latitude": choords.latitude,
                         "longitude": choords.longitude,
                         "height"   : choords.height}
        user_struct = {"email"      : user.email,
                       "phone"      : user.phone,
                       "fam"        : user.fam,
                       "name"       : user.name,
                       "otc"        : user.otc}
        result = {"date_added"      : str(per.date_added),
                  "beautyTitle"     : per.beautyTitle,
                  "title"           : per.title,
                  "other_titles"    : per.other_titles,
                  "connect"         : per.connect,
                  "level_winter"    : per.level_winter,
                  "level_summer"    : per.level_summer,
                  "level_autumn"    : per.level_autumn,
                  "level_spring"    : per.level_spring,
                  "status"          : str(per.status),
                  "user"            : user_struct,
                  "choords"         : choords_struct} #
        return JSONResponse(content={"status": 200, "message": result, "id": item_id})
    else:
        return JSONResponse(content={"status": 500, "message": "item not exist", "id": item_id})

@app.patch("/api/submitData/{item_id}")
def submitDatа_p(item_id,data=Body(), db: Session = Depends(get_db)):
    if not db:
        return JSONResponse(content={"status": 500, "message": "db connect error", "id": 'null'})
    current_date = datetime.now()

    perevalforpatch = db.query(Pereval_added).filter(Pereval_added.id == item_id).first()
    choordsforpatch = db.query(Choords).filter(Choords.id == perevalforpatch.choords).first()

    perevalforpatch.update({'beautyTitle': data["beauty_title"],
                            'title': data["title"],
                            'other_titles': data["other_titles"],
                            'connect': data["connect"],
                            'level_winter': data["level"]["winter"],
                            'level_summer': data["level"]["summer"],
                            'level_autumn': data["level"]["autumn"],
                            'level_spring': data["level"]["spring"]})

    choordsforpatch.update({'latitude': data["coords"]["latitude"],
                            'longitude': data["coords"]["longitude"],
                            'height': data["coords"]["height"]})
    imid = get_cur_id(db, Pereval_images)
    pimid = get_cur_id(db, Pereval_pereval_images)
    for img in data["images"]:
        pereval_images = Pereval_images(id=imid,
                                        title=img["title"],
                                        date_added=current_date,
                                        img=bytes(img["data"], encoding='utf8'))
        db.add(pereval_images)
        Ppimages = Pereval_pereval_images(id=pimid,
                                          id_pereval=item_id,
                                          id_image=imid)
        db.add(Ppimages)
        imid += 1
        pimid += 1
    try:
        db.commit()
    except:
        return JSONResponse(content={"status": 500, "state": 0, "id": item_id})
    return JSONResponse(content={"status": 200, "state": 1, "id": item_id})

@app.post("/api/submitData")
def submitData(data=Body(), db: Session = Depends(get_db)):
     if not db:
         return json.dumps({"status": 500, "message": "db connect error", "id": 'null'})
     current_date = datetime.now()
     usid = get_cur_id(db,Users)
     user = Users(id    = usid,
                  email = data["user"]["email"],
                  phone = data["user"]["phone"],
                  fam   = data["user"]["fam"],
                  name  = data["user"]["name"],
                  otc   = data["user"]["otc"])
     db.add(user)
     chid = get_cur_id(db,Choords)
     choords = Choords(id        = chid,
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
                             date_added=current_date,
                             status = StatusEnum.NEW)
     db.add(pereval)
     imid = get_cur_id(db, Pereval_images)
     pimid = get_cur_id(db, Pereval_pereval_images)
     for img in data["images"]:
         # pereval_images = Pereval_images(id=imid,
         #                                 title = img["title"],
         #                                 date_added=current_date)
         pereval_images = Pereval_images(id=imid,
                                         title = img["title"],
                                         date_added=current_date,
                                         img=bytes(img["data"], encoding='utf8'))

         db.add(pereval_images)
         Ppimages = Pereval_pereval_images(id=pimid,
                                           id_pereval=id,
                                           id_image=imid)
         db.add(Ppimages)
         # да, это костыль, но в pgsql где есть последовательности
         # это будет не нужно
         imid += 1
         pimid += 1
     try:
        db.commit()
     except:
         return JSONResponse(content={"status": 500, "message": "db commit error", "id": 'null'})
     return JSONResponse(content={ "status": 200, "message": 'null', "id": pereval.id })


def test__submitData_post_return_dict():
    ret = submitData({},None)
    dict = json.loads(ret)
    if dict.get("status"):
        if dict.get("message"):
            if dict.get("id"):
                assert False
    assert True

def test__submitData_patch_return_dict():
    ret = submitDatа_p(0,{})
    dict = json.loads(ret)
    if dict.get("status"):
        if dict.get("state"):
            if dict.get("id"):
                assert False
    assert True

def test__submitData_get_return_dict():
    ret = submitDatа_g({},None)
    dict = json.loads(ret)
    if dict.get("status"):
        if dict.get("message"):
            if dict.get("id"):
                assert False
    assert True

def test__submitData_get_email_return_dict():
    ret = submitDatа_gp({},None)
    dict = json.loads(ret)
    if dict.get("status"):
        if dict.get("message"):
            if dict.get("id"):
                assert False
    assert True