from sqlalchemy import Column, Integer, String
from .database import Base

class Books(Base):
    __tablename__ = 'books_data'
    
    Id = Column(Integer, primary_key=True, index=True)
    Book_Title = Column(String)
    Book_Author = Column(String)
    Year_Of_Publication = Column(Integer)
    Publisher = Column(String)

class Songs(Base):
    __tablename__ = 'songs_data'
    
    Id = Column(Integer, primary_key=True, index=True)
    Track_Name = Column(String)
    Artist_Name = Column(String)
    
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)