from datetime import datetime
import sqlite3

class Note():
    def __init__(self, opened, title, text, time, active):
        self.__title : str = title
        self.__text : str = text
        self.__time : datetime = time
        self.__active : bool = active
        self.__opened : str = opened

    def __str__(self):
        return self.__text + " " + str(self.__time)
    
    def setTime(self, time):
        self.__time = time

    def getTime(self):
        return self.__time
    
    def setText(self, text):
        self.__text = text

    def getText(self):
        return self.__text
    
    def setTitle(self, title):
        self.__title = title
        
    def getTitle(self):
        return self.__text
        
    def setActive(self, active):
        self.__active = active

    def getActive(self):
        return self.__active

    def addToDatabase(self):
        if self.__opened == "new":
            connection = sqlite3.connect('NotesDatabase.sqlite3')
            cursor = connection.cursor()

            # Wstaw notatkę do bazy danych
            cursor.execute('INSERT INTO Notes (title, text, time, active) VALUES (?, ?, ?, ?)',
                        (self.__title, self.__text, str(self.__time), int(self.__active)))

            # Zatwierdź zmiany i zamknij połączenie
            connection.commit()
            connection.close()
