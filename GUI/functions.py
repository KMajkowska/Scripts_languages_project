import os
import speech_recognition as sr
import emoji
from pathlib import Path 

if os.path.basename(sys.argv[0]) == "GUI.exe":
    # Kod uruchomiony jako plik wykonywalny (.exe)
    CURRENT_NOTES_PATH = Path(__file__).resolve().parent.parent.parent.parent / 'notes/notes.py'
else:
    # Kod uruchomiony z Visual Studio Code lub innego kontekstu
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
    

def get_emoji_list():
    emoji_dict = str(emoji.EMOJI_DATA)
    emojis = emoji.distinct_emoji_list(emoji_dict)
    return emojis



