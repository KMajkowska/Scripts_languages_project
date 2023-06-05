import os
import speech_recognition as sr

CURRENT_NOTES_PATH = os.path.join(os.getcwd(),"notes\\notes.py")

def speech_to_text():
    r = sr.Recognizer()
    r.energy_threshold=4000 #Ustawiamy żeby mikrofon był bardziej czuły na wykrycie ciszy
    with sr.Microphone() as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language="pl-PL")
            return text
        except sr.UnknownValueError: print("Niezrozumiała treść, spróbuj jeszcze raz")
    
if __name__ == "__main__":
    speech_to_text()
   
