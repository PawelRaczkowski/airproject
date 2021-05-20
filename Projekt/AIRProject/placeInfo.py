import requests
import pyttsx3
from urllib.parse import urlparse
import urllib

def getInfoString(placeName):
    response = requests.get("https://pl.wikipedia.org/w/api.php?action=opensearch&format=json&search=" + urllib.parse.quote(placeName))#mo�na da� troch� wi�cej zda� :p
    #test kod odpowiedzi
    #if response.json()[1][0]:#pierwszy lepszy wynik
    if (len(response.json()[1]) > 0):
        querryParam =  urllib.parse.quote(response.json()[1][0])#pierwszy lepszy wynik
        response = requests.get("https://pl.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=3&exlimit=1&explaintext=1&formatversion=2&format=json&titles=" + querryParam)
        output = response.json()["query"]["pages"][0]["extract"].replace("\n", "").split("==")[0]#czaryy
        return output
    return None

def getInfoMP3(placeName): #zwraca nazw� pliku, je�li udane
    toRead = getInfoString(placeName)
    if toRead:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.save_to_file(toRead,placeName + ".mp3")
        engine.runAndWait()
        return placeName + ".mp3"
    return None