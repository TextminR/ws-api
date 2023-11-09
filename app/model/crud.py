from datetime import date

from sqlalchemy.orm import Session

from app.model import schemas
from app.model import models


def get_text(db: Session, text_id: int):
    return db.query(models.Text).filter(models.Text.id == text_id).first()


def get_texts(db: Session, skip, limit):
    return db.query(models.Text.id, models.Text.autor, models.Text.titel, models.Text.year).offset(skip).limit(
        limit).all()


def get_texts_by_year(db: Session, year: int):
    return db.query(models.Text).filter(models.Text.year == year).all()


def get_texts_by_years_between(db: Session, minYear: int, maxYear: int):
    return db.query(models.Text).filter(models.Text.year >= minYear).filter(models.Text.year <= maxYear).all()


def get_texts_by_author(db: Session, author: str):
    return db.query(models.Text).filter(models.Text.autor == author).all()


def get_text_by_title(db: Session, title: str):
    return db.query(models.Text).filter(models.Text.titel == title).all()


def get_title_by_id(db: Session, text_id: int):
    return db.query(models.Text.titel).filter(models.Text.id == text_id).first()


def get_title_by_year(db: Session, year: int):
    return db.query(models.Text.titel).filter(models.Text.year == year).all()


def get_titles_between_years(db: Session, minYear: int, maxYear: int):
    return db.query(models.Text.titel).filter(models.Text.year >= minYear).filter(models.Text.year <= maxYear).all()


def get_title_by_author(db: Session, author: str):
    return db.query(models.Text.titel).filter(models.Text.autor == author).all()


def get_birthplace_by_author(db: Session, authorname: str):
    return db.query(models.Author.birth_place).filter(models.Author.name == authorname).all()


def create_text(db: Session, text: schemas.TextCreate):
    db_text = models.Text(autor=text.autor, titel=text.titel, text=text.text, year=text.year)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def create_NER_Data(db: Session, data: schemas.NER_DataCreate):
    db_data = models.NER_Data(prompt=data.prompt, author=data.author, date=data.date)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_NER_Data(db: Session, skip, limit):
    return db.query(models.NER_Data).offset(skip).limit(limit).all()


def delete_text(db: Session, text_id: int):
    db.query(models.Text).filter(models.Text.id == text_id).delete()
    db.commit()
    return "deleted"


def get_newsarticles(db: Session, skip, limit):
    return db.query(models.Newsarticle).offset(skip).limit(limit).all()


def get_newsarticle(db: Session, text_id: int):
    return db.query(models.Newsarticle).filter(models.Newsarticle.id == text_id).first()


def get_newsarticle_by_date_between(db: Session, minDate: date, maxDate: date):
    return db.query(models.Newsarticle).filter(models.Newsarticle.date >= minDate).filter(
        models.Newsarticle.date <= maxDate).all()


def create_newsarticle(db: Session, data: schemas.NewsarticleCreate):
    db_data = models.Newsarticle(titel=data.titel, datum=data.datum, newspapername=data.newspapername, autor=data.autor,
                                 text=data.text)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
