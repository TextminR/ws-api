from typing import List

from fastapi import Depends, FastAPI, File, UploadFile
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


def to_text_list(texts):
    text_list = []
    for text in texts:
        text_list.append(text)
    return text_list


@app.get("/findAllTexts", response_model=List[schemas.TextMetadata])
def findAllTexts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return to_text_list(crud.get_texts(db, skip=skip, limit=limit))


@app.get("/texts/{textid}", response_model=schemas.Text)
def findTextById(textid, db: Session = Depends(get_db)):
    return crud.get_text(db, text_id=textid)


# @app.post("/extractFromFile/", response_model=List[schemas.Extraction])
# def extractFromFile(file: UploadFile):
#     res = extractFromPDF(file)
#     return res

@app.post("/getTitleBetweenYears/", response_model=List[str])
def getTitleBetweenYears(minYear: int, maxYear: int, db: Session = Depends(get_db)):
    return to_text_list(crud.get_titles_between_years(db, minYear, maxYear))


@app.post("/getTitleByYear/", response_model=List[str])
def getTitleByYear(year: int, db: Session = Depends(get_db)):
    return to_text_list(crud.get_title_by_year(db, year))


@app.post("/createText/", response_model=schemas.Text)
def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
    return crud.create_text(db=db, text=text)


@app.post("/getTitleByAuthor/", response_model=List[str])
def getTitleByAuthor(author: str, db: Session = Depends(get_db)):
    return to_text_list(crud.get_title_by_author(db, author))


@app.post("/getTextByTitle/", response_model=List[schemas.Text])
def getTextByTitle(title: str, db: Session = Depends(get_db)):
    return to_text_list(crud.get_text_by_title(db, title))


@app.post("/getTextByAuthor/", response_model=List[schemas.Text])
def getTextByAuthor(author: str, db: Session = Depends(get_db)):
    return to_text_list(crud.get_texts_by_author(db, author))


@app.post("/getTextByYear/", response_model=List[schemas.Text])
def getTextByYear(year: int, db: Session = Depends(get_db)):
    return to_text_list(crud.get_texts_by_year(db, year))


@app.get("/getAuthors/", response_model=List[schemas.Author])
def getAuthors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return to_text_list(crud.get_authors(db, skip, limit))


@app.post("/getBirthplaceOfAuthor/", response_model=List[schemas.AuthorMetadata])
def getBirthplaceOfAuthor(authorname: str, db: Session = Depends(get_db)):
    return crud.get_birthplace_by_author(db, authorname)


@app.post("/getTextByYearBetween/", response_model=List[schemas.Text])
def getTextByYearBetween(minYear: int, maxYear: int, db: Session = Depends(get_db)):
    return to_text_list(crud.get_texts_by_years_between(db, minYear, maxYear))


@app.post("/getTextByLanguageAndYears/", response_model=List[schemas.Text])
def getTextByLanguageAndYears(minYear: int, maxYear: int, language: str, db: Session = Depends(get_db)):
    return to_text_list(crud.get_texts_by_language_and_years(db, minYear, maxYear, language))


@app.delete("/deleteText/{textid}")
def deleteText(textid, db: Session = Depends(get_db)):
    crud.delete_text(db, text_id=textid)
    return "deleted"


@app.post("/createNER_Data/", response_model=schemas.NER_Data)
def createNER_Data(data: schemas.NER_DataCreate, db: Session = Depends(get_db)):
    return crud.create_NER_Data(db=db, data=data)


@app.get("/getNER_Data/", response_model=List[schemas.NER_Data])
def getNER_Data(db: Session = Depends(get_db)):
    return crud.get_NER_Data(db, 0, 1000)


@app.get("/getNewsarticle/{textid}", response_model=schemas.Newsarticle)
def get_newsarticle(textid, db: Session = Depends(get_db)):
    res = crud.get_newsarticle(db, textid)
    return res


@app.get("/getNewsarticles/", response_model=List[schemas.Newsarticle])
def get_newsarticles(db: Session = Depends(get_db)):
    return crud.get_newsarticles(db, 0, 1000)


@app.post("/createNewsarticle/", response_model=schemas.Newsarticle)
def create_newsarticle(data: schemas.NewsarticleCreate, db: Session = Depends(get_db)):
    return crud.create_newsarticle(db, data)


@app.get("/")
async def hello():
    return "hi"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
