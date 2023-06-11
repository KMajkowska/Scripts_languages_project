from datetime import datetime
import sqlite3

CONNECTON = 'NotesDatabase.sqlite3'
class Note():
    def __init__(self, uid, title, text, time, last_edit,active, reminder):
        self.__title : str = title
        self.__text : str = text
        self.__time : datetime = time
        self.__last_edit: datetime = last_edit
        self.__active : bool = active
        self.__uid : str = uid
        self.__reminder : datetime = reminder

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
        return self.__title
        
    def setActive(self, active):
        self.__active = active

    def getActive(self):
        return self.__active
    
    def setLastEdit(self, last_edit):
        self.__last_edit = last_edit

    def getLastEdit(self):
        return self.__last_edit

    def addToDatabase(self):
        if self.__uid == -1:
            connection = sqlite3.connect(CONNECTON)
            cursor = connection.cursor()

            self.__uid = str(datetime.now())
            # Wstaw notatkę do bazy danych
            cursor.execute('INSERT INTO Notes (title, text, time, last_edit, active, uid, reminder) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (str(self.__title), str(self.__text), str(self.__time), str(self.__last_edit), int(self.__active), str(self.__uid), str(self.__reminder)))

            # Zatwierdź zmiany i zamknij połączenie
            connection.commit()
            connection.close()

        else:
            connection = sqlite3.connect(CONNECTON)
            cursor = connection.cursor()

            # Zaktualizuj notatkę w bazie danych
            cursor.execute('UPDATE Notes SET title=?, text=?, time=?, last_edit=?, active=?, reminder=? WHERE uid=?',
                        (str(self.__title), str(self.__text), str(self.__time), str(self.__last_edit), int(self.__active), str(self.__uid), str(self.__reminder)))

            # Zatwierdź zmiany i zamknij połączenie
            connection.commit()
            connection.close()

    def deleteFromDatabase(self):
        connection = sqlite3.connect(CONNECTON)
        cursor = connection.cursor()

        cursor.execute('DELETE FROM Notes WHERE uid = ?', (self.__uid,))

        connection.commit()
        connection.close()

    def update(self, title, text, time, last_edit, reminder):
        self.__title = title
        self.__text = text
        self.__time = time
        self.__last_edit = last_edit
        self.__active = True
        self.__reminder = reminder
        self.addToDatabase()
        return self

    def archive(self):
        self.__active = False
        self.addToDatabase()
        return self
    
    def setReminder(self, reminder):
        self.__reminder = reminder

    def getReminder(self):
        return self.__reminder

