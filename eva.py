from bottle import *
import pygame.mixer as mixer
import os
import audio_metadata as ad
import json
import sqlite3 
import time 

mixer.init()
directory = 'music/'
sqldir = sqlite3.connect("database.db")

def play(musicString : str):
    mixer.music.load(directory+musicString)
    mixer.music.play()


def dbInterface(): # TEST FUNCTION 
    for file,file_id in enumerate(os.listdir('music')):
        query = 'INSERT INTO music(music_name, music_id) VALUES("{0}","{1}")'.format(file,file_id)
        print(query)
   #sql = sqldir.cursor()
   #sql.execute(query)
   #sqldir.commit()


def stop():
    mixer.music.stop()

@post('/')
def postMusic():
    state = ''
    #incoming raw data
    rawData = request.body.readlines()
    #turn raw data into json data
    jsonData = json.loads(rawData[0].decode('utf-8')) 
    #play music

    if jsonData['command'] == 'play':
        state = 'playing'
        play(jsonData['music'])
    elif jsonData['command'] == 'stop':
        state = 'stopped'
        stop()


    #declaring global variables for metadatas 
    global music_duration , metadata
    metadata = ad.load(directory+jsonData['music']) # loading music metadata for api 
    music_length = metadata['streaminfo']['duration'] 
    music_duration = time.strftime('%M:%S', time.gmtime(music_length))
  
    return {
            "duration":music_duration,
            "music":jsonData['music'],
            "state":state
            }

@route('/plist')
def playListFunction():
    dbInterface()
run(host='127.0.0.1',port=8000,reloader=True)

