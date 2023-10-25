from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import crud
from model import schemas
from model import models
from database import SessionLocal, engine
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/findAllTexts", response_model=List[schemas.Text])
def findAllTexts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=skip, limit=limit)
    text_list = []
    for text in texts:
        text_list.append(text)

    return text_list

@app.get("/texts/{textid}", response_model=schemas.Text)
def findTextById(textid, db: Session = Depends(get_db)):
    return crud.get_text(db, text_id=textid)

@app.post("/getTitelBetweenYears/", response_model=List[str])
def getTextByYears(minYear: int, maxYear: int, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getYear() >= minYear and text.getYear() <= maxYear:
            text_list.append(text.getTitel())

    return text_list

@app.post("/getTitelByYear/", response_model=List[str])
def getTextByYears(year: int, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getYear() == year:
            text_list.append(text.getTitel())

    return text_list


@app.post("/createText/", response_model=schemas.Text)
def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
    return crud.create_text(db=db, text=text)

@app.post("/getTitelByAuthor/", response_model=List[str])
def getTextByAuthor(author: str, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getAutor() == author:
            text_list.append(text.getTitel())

    return text_list

@app.post("/getTextByTitle/", response_model=List[str])
def getTextByTitle(title: str, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getTitel() == title:
            text_list.append(text.getText())

    return text_list

@app.post("/getTextByAuthor/", response_model=List[str])
def getTextByAuthor(author: str, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getAutor() == author:
            text_list.append(text.getText())

    return text_list

@app.post("/getTextByYear/", response_model=List[str])
def getTextByYear(year: int, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getYear() == year:
            text_list.append(text.getText())

    return text_list

@app.post("/getTextByYearBetween/", response_model=List[str])
def getTextByYearBetween(minYear: int, maxYear: int, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=0, limit=100)
    text_list = []
    for text in texts:
        if text.getYear() >= minYear and text.getYear() <= maxYear:
            text_list.append(text.getText())

    return text_list

@app.post("/getBirthplaceOfAuthor/", response_model=str)
def getBirthplaceOfAuthor(authorname: str, db: Session = Depends(get_db)):
    birthplace = "none"
    authorlist = crud.get_birthplace_by_author(db, authorname=authorname)
    for author in authorlist:
        birthplace = author.getBirthplace()
    return birthplace

@app.get("/")
async def hello():
    return "hi"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
