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




def dbInterface(command:str):
    if command == 'update_playlist':
        query = 'SELECT * FROM music'
        sql = sqldir.cursor()
        sql.execute(query)
        data = sql.fetchall()
        for file,file_id in enumerate(os.listdir('music')): # IDK what im doing but im doing fine
            #this block of code here stops data duplicate whenever you refresh ("/update_list")
            if file in data:
                pass
            else:
                query = 'INSERT INTO music(music_name, music_id) VALUES("{0}","{1}")'.format(file_id,file)
                sql.execute(query)
        sqldir.commit()
    
    elif command == 'show_playlist':
        sql = sqldir.cursor()
        query = 'SELECT DISTINCT  * FROM music'
        sql.execute(query)
        musicTable = sql.fetchall()
        return musicTable

    elif commnad == 'append_playlist':
        pass
    
    sqldir.commit()


def stop():
    mixer.music.stop()

@post('/')
def postMusic():
    state = ''
    #incoming raw data
    rawData = request.body.readlines() #turn raw data into json data jsonData = json.loads(rawData[0].decode('utf-8')) 
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

@route('/list')
def musiclistReturn():
    list_data = dbInterface("show_playlist")
    return template('music_list.tpl',list_data = list_data)

@route('/update_list')
def playListFunction():
    dbInterface('update_playlist')

@post('/list_get')
def listGetAPI():
    data = dbInterface("show_playlist")
    return {"music_list":data}

run(host='0.0.0.0',port=8000,reloader=True)

