from sqlalchemy import Column, Integer, String, DateTime
from app.model.database import Base


class Text(Base):
    __tablename__ = "textdata"

    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    text = Column(String)
    language = Column(String)
    year = Column(Integer)

    def __str__(self):
        return f"{self.id}: {self.author} {self.title} {self.year} {self.language}, {self.text}"

    def getText(self):
        return self.text

    def getAuthor(self):
        return self.author

    def getTitle(self):
        return self.title

    def getYear(self):
        return self.year

    def getLanguage(self):
        return self.language


class Author(Base):
    __tablename__ = "authors"

    name = Column(String, primary_key=True)
    birth_place = Column(String)

    def __str__(self):
        return f"{self.name}: {self.birthplace}"

    def getName(self):
        return self.name

    def getBirthplace(self):
        return self.birth_place


class NER_Data(Base):
    __tablename__ = "ner_data"

    id = Column(Integer, primary_key=True)
    prompt = Column(String)
    author = Column(String)
    date = Column(String)

    def __str__(self):
        return f"{self.id}: {self.prompt}, {self.author} {self.date}"


class Newsarticle(Base):
    __tablename__ = "newsarticle"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    datum = Column(DateTime)
    newspapername = Column(String)
    author = Column(String)
    text = Column(String)
    language = Column(String)
