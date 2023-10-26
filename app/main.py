from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.model import schemas, crud
from app.model import models
from app.model.database import SessionLocal, engine
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


@app.get("/findAllTexts", response_model=List[schemas.TextMetadata])
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
def getTitelBetweenYears(minYear: int, maxYear: int, db: Session = Depends(get_db)):
    titels = crud.get_titles_between_years(db, minYear, maxYear)
    titel_list = []
    for titel in titels:
        titel_list.append(titel[0])

    return titel_list


@app.post("/getTitelByYear/", response_model=List[str])
def getTitelByYear(year: int, db: Session = Depends(get_db)):
    titels = crud.get_title_by_year(db, year)
    titel_list = []
    for titel in titels:
        titel_list.append(titel[0])

    return titel_list


@app.post("/createText/", response_model=schemas.Text)
def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
    return crud.create_text(db=db, text=text)


@app.post("/getTitleByAuthor/", response_model=List[str])
def getTitleByAuthor(author: str, db: Session = Depends(get_db)):
    titels = crud.get_title_by_author(db, author)
    titel_list = []
    for titel in titels:
        titel_list.append(titel[0])

    return titel_list


@app.post("/getTextByTitle/", response_model=List[schemas.Text])
def getTextByTitle(title: str, db: Session = Depends(get_db)):
    texts = crud.get_text_by_title(db, title)
    text_list = []
    for text in texts:
        text_list.append(text)

    return text_list


@app.post("/getTextByAuthor/", response_model=List[schemas.Text])
def getTextByAuthor(author: str, db: Session = Depends(get_db)):
    texts = crud.get_texts_by_author(db, author)
    text_list = []
    for text in texts:
        text_list.append(text)

    return text_list


@app.post("/getTextByYear/", response_model=List[schemas.Text])
def getTextByYear(year: int, db: Session = Depends(get_db)):
    texts = crud.get_texts_by_year(db, year)
    text_list = []
    for text in texts:
        text_list.append(text)

    return text_list


@app.post("/getBirthplaceOfAuthor/", response_model=str)
def getBirthplaceOfAuthor(authorname: str, db: Session = Depends(get_db)):
    birthplace = crud.get_birthplace_by_author(db, authorname=authorname)[0]
    birthplace = birthplace[0]
    return birthplace


@app.post("/getTextByYearBetween/", response_model=List[schemas.Text])
def getTextByYearBetween(minYear: int, maxYear: int, db: Session = Depends(get_db)):
    texts = crud.get_texts_by_years_between(db, minYear, maxYear)
    text_list = []
    for text in texts:
        text_list.append(text)

    return text_list


@app.delete("/deleteText/{textid}")
def deleteText(textid, db: Session = Depends(get_db)):
    crud.delete_text(db, text_id=textid)
    return "deleted"

@app.get("/")
async def hello():
    return "hi"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
