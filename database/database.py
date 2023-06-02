from sqlalchemy import create_engine
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os

ENGINE = create_engine(f'sqlite:///NotesDatabase.sqlite3')

class Base(DeclarativeBase):
    pass

class Notes(Base):
    __tablename__ = 'Notes'
    uid:Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str]= mapped_column(String)
    text:Mapped[str] = mapped_column(String)
    time :Mapped[DateTime] = mapped_column(DateTime)
    active:Mapped[bool]= mapped_column(Boolean)
 
if __name__ == "__main__":
    Base.metadata.create_all(ENGINE)
    if os.path.exists(f'NotesDatabase.sqlite3'):
        print("Database created")
    else:
        print("Database not created")
