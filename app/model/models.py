from sqlalchemy import Column, Integer, String

from app.model.database import Base


class Text(Base):
    __tablename__ = "textdata"

    id = Column(Integer, primary_key=True)
    autor = Column(String)
    titel = Column(String)
    text = Column(String)
    year = Column(Integer)

    def __str__(self):
        return f"{self.id}: {self.autor} {self.titel} {self.year}, {self.text}"

    def getText(self):
        return self.text

    def getAutor(self):
        return self.autor

    def getTitel(self):
        return self.titel

    def getYear(self):
        return self.year


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
