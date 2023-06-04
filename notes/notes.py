from datetime import datetime
import sqlite3

class Note():
    def __init__(self, uid, title, text, time, active):
        self.__title : str = title
        self.__text : str = text
        self.__time : datetime = time
        self.__active : bool = active
        self.__uid : int = uid

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
        if self.__uid == -1:
            connection = sqlite3.connect('NotesDatabase.sqlite3')
            cursor = connection.cursor()

            # Wstaw notatkę do bazy danych
            cursor.execute('INSERT INTO Notes (title, text, time, active) VALUES (?, ?, ?, ?)',
                        (self.__title, self.__text, str(self.__time), int(self.__active)))

            # Zatwierdź zmiany i zamknij połączenie
            connection.commit()
            connection.close()

        else:
            connection = sqlite3.connect('NotesDatabase.sqlite3')
            cursor = connection.cursor()

            # Zaktualizuj notatkę w bazie danych
            cursor.execute('UPDATE Notes SET title=?, text=?, time=?, active=? WHERE uid=?',
                        (self.__title, self.__text, str(self.__time), int(self.__active), self.__uid))

            # Zatwierdź zmiany i zamknij połączenie
            connection.commit()
            connection.close()

    def update(self, text, time):
        self.__text = text
        self.__time = time
        self.addToDatabase()

    def archive(self):
        self.__active = False
        self.addToDatabase()