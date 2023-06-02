from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
import os

class Base(DeclarativeBase):
    pass

class NotesDatabase(Base):
    __tablename__ = 'Notes'
    uid:Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str]= mapped_column(String)
    text:Mapped[str] = mapped_column(DateTime)
    time :Mapped[DateTime] = mapped_column(DateTime)
    active:Mapped[bool]= mapped_column(Boolean)
 
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'NotesDatabase.sqlite3')
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    if os.path.exists(f'{db_path}'):
        print("Database created")
    else:
        print("Database not created")
