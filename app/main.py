from typing import List
import motor.motor_asyncio
from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.model import models
from app.model.models import TextCollection, TextModel
import uvicorn

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:mongo@localhost:27017/")
db = client.text
text_collection = db.get_collection("text")


@app.get("/findAllTexts", response_model=TextCollection)
async def findAllTexts():
    return TextCollection(texts=await text_collection.find().to_list(1000))


@app.get("/texts/{textid}", response_model=TextModel)
async def findTextById(textid):
    if (
            text := await text_collection.find_one({"_id": ObjectId(textid)})
    ) is not None:
        return text

    raise HTTPException(status_code=404, detail=f"Text {textid} not found.")


@app.post("/getTitelBetweenYears/", response_model=TextCollection)
def getTitelBetweenYears(minYear: int, maxYear: int):
    return TextCollection(texts=text_collection.find({"year": {'$lt': maxYear, '$gte': minYear}}))


# @app.post("/getTitelByYear/", response_model=List[str])
# def getTitelByYear(year: int, db: Session = Depends(get_db)):
#     titels = crud.get_title_by_year(db, year)
#     titel_list = []
#     for titel in titels:
#         titel_list.append(titel[0])
#
#     return titel_list
#
#
# @app.post("/createText/", response_model=schemas.Text)
# def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
#     return crud.create_text(db=db, text=text)
#
#
# @app.post("/getTitleByAuthor/", response_model=List[str])
# def getTitleByAuthor(author: str, db: Session = Depends(get_db)):
#     titels = crud.get_title_by_author(db, author)
#     titel_list = []
#     for titel in titels:
#         titel_list.append(titel[0])
#
#     return titel_list
#
#
# @app.post("/getTextByTitle/", response_model=List[schemas.Text])
# def getTextByTitle(title: str, db: Session = Depends(get_db)):
#     texts = crud.get_text_by_title(db, title)
#     text_list = []
#     for text in texts:
#         text_list.append(text)
#
#     return text_list
#
#
# @app.post("/getTextByAuthor/", response_model=List[schemas.Text])
# def getTextByAuthor(author: str, db: Session = Depends(get_db)):
#     texts = crud.get_texts_by_author(db, author)
#     text_list = []
#     for text in texts:
#         text_list.append(text)
#
#     return text_list
#
#
# @app.post("/getTextByYear/", response_model=List[schemas.Text])
# def getTextByYear(year: int, db: Session = Depends(get_db)):
#     texts = crud.get_texts_by_year(db, year)
#     text_list = []
#     for text in texts:
#         text_list.append(text)
#
#     return text_list
#
#
# @app.post("/getBirthplaceOfAuthor/", response_model=str)
# def getBirthplaceOfAuthor(authorname: str, db: Session = Depends(get_db)):
#     birthplace = crud.get_birthplace_by_author(db, authorname=authorname)[0]
#     birthplace = birthplace[0]
#     return birthplace
#
#
# @app.post("/getTextByYearBetween/", response_model=List[schemas.Text])
# def getTextByYearBetween(minYear: int, maxYear: int, db: Session = Depends(get_db)):
#     texts = crud.get_texts_by_years_between(db, minYear, maxYear)
#     text_list = []
#     for text in texts:
#         text_list.append(text)
#
#     return text_list
#
#
# @app.delete("/deleteText/{textid}")
# def deleteText(textid, db: Session = Depends(get_db)):
#     crud.delete_text(db, text_id=textid)
#     return "deleted"
#
#
@app.get("/")
async def hello():
    return "hi"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
