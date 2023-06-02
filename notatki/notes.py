from datetime import datetime

class Note():
    def __init__(self, text, time):
        self.__text : str = text
        self.__time : datetime = time

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
