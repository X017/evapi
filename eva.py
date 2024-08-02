from bottle import *
import pygame.mixer as mixer
import os
import audio_metadata as ad
import json
import sqlite3 
import time 

mixer.init()
directory = 'music/'

    
def play(musicString : str):
    mixer.music.load(directory+musicString)
    mixer.music.play()


def stop():
    mixer.music.stop()

@post('/')
def postMusic():
    #incoming raw data
    rawData = request.body.readlines()
    #turn raw data into json data
    jsonData = json.loads(rawData[0].decode('utf-8')) 
    
    #play music 
    play(jsonData['music'])
    
    #declaring global variables for metadatas 
    global music_duration , metadata
    metadata = ad.load(directory+jsonData['music']) # loading music metadata for api 
    music_length = metadata['streaminfo']['duration'] 
    music_duration = time.strftime('%M:%S', time.gmtime(music_length))
    # added a comment
    return {
            "duration":music_duration,
            "music":jsonData['music']
            }


run(host='127.0.0.1',port=8000,reloader=True)

