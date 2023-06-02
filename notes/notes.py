from datetime import datetime

class Note():
    def __init__(self):
        self.__title : str = ""
        self.__text : str = ""
        self.__time : datetime = ""
        self.__active : bool = True

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
    
    def openedNote(self, title, text, time, active):
        self.__title = title
        self.__text = text
        self.__time = time
        self.__active = active

