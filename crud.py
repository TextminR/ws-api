from sqlalchemy.orm import Session

from model import schemas
from model import models


def get_text(db: Session, text_id: int):
    return db.query(models.Text).filter(models.Text.id == text_id).first()


def get_texts(db: Session, skip, limit):
    return db.query(models.Text).offset(skip).limit(limit).all()

def get_birthplace_by_author(db: Session, authorname: str):
    return db.query(models.Author).filter(models.Author.name == authorname).all()


def create_text(db: Session, text: schemas.TextCreate):
    db_text = models.Text(autor=text.autor, titel=text.titel, text=text.text)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text
