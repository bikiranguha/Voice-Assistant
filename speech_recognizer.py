#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs
import nltk
nltk.download('averaged_perceptron_tagger')
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def jarvis(data):
    if "how are you" in data:
        speak("I am fine")
 
    if "what time is it" in data:
        speak(ctime())
 
    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Frank, I will show you where " + location + " is.")
        os.system("google-chrome https://www.google.nl/maps/place/" + location + "/&amp;")
    if "search for" in data:
        data = data.split(" ")
        search_term = data[2:]
        search_url = 'https://www.google.com/search?q=' + '+'.join(search_term)
        print(search_url)
        speak("Ok, here is what came up!")
        os.system("google-chrome "+ search_url)
    if "youtube" in data.lower():
        data = data.split()
        search_term = data[1:]
        search_url = 'https://www.youtube.com/results?search_query=' + '+'.join(search_term)
        print(search_url)
        speak("Ok, here is what came up on youtube!")
        os.system("google-chrome "+ search_url)
    if ("temperature" in data.lower()) or ("weather" in data.lower()):
        #data = data.split()
        tagged_sent = nltk.pos_tag(data.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
        city = ' '.join(propernouns)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = 'https://www.google.com/search?q=temperature+in+' + city.strip()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        temp = str(soup.find(class_="wob_t").get_text())
        cond = str(soup.find(id="wob_dc").get_text())
        speak("Currently the temperature at " + city + " is " + temp + "  degrees Fahrenheit. Weather condition is " + cond+".")

    """
    if ("temperature" in data.lower()) or ("weather" in data.lower()):
        data = data.split()
        city = ' '.join(data[2:])
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = 'https://www.google.com/search?q=temperature+in+' + city.strip()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        temp = str(soup.find(class_="wob_t").get_text())
        cond = str(soup.find(id="wob_dc").get_text())
        speak("Currently the temperature at " + city + " is " + temp + "  degrees Fahrenheit. Weather condition is " + cond+".")
    """



 
# initialization
time.sleep(2)
speak("Hey there, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)