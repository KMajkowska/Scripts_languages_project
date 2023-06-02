from sqlalchemy.orm import Session
from datetime import datetime
from database import ENGINE, Notes


def load_new_notes():
    with Session(ENGINE) as session:
        note = Notes( 
            title = "Coś", 
            text = "test", 
            time = datetime.strptime("2023-06-02 10:30:00", "%Y-%m-%d %H:%M:%S"),
            active = True,
        )

        note2 = Notes( 
            title = "Coś", 
            text = "test", 
            time = datetime.strptime("2023-06-02 10:30:00", "%Y-%m-%d %H:%M:%S"),
            active = False,
        )
        
    session.add_all([note, note2])
    session.commit()

def read_notes():
    pass

if __name__ == "__main__":
    load_new_notes()

