from sqlalchemy import Column, Integer, String

from database import Base


class Text(Base):
    __tablename__ = "textdata"

    id = Column(Integer, primary_key=True)
    autor = Column(String)
    titel = Column(String)
    text = Column(String)
    year = Column(Integer)

    def __str__(self):
        return f"{self.id}: {self.autor} {self.titel}, {self.text} years old"

    def getText(self):
        return self.text

    def getAutor(self):
        return self.autor

    def getTitel(self):
        return self.titel

    def getYear(self):
        return self.year