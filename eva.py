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
mix = mixer.music

def play(musicString : str):
    mix.load(directory+musicString)
    mix.play()




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
    mix.stop()


def pause():
    mix.pause()

def seek(pos2):
    mix.play(0,pos2)

@post('/')
def postMusic():
    state = ''
    #incoming raw data
    rawData = request.body.readlines() #turn raw data into json data 
    jsonData = json.loads(rawData[0].decode('utf-8')) 
    print(jsonData)
    if jsonData['command'] == 'play':
        state = 'playing'
        play(jsonData['music']) 
    elif jsonData['command'] == 'stop':
        state = 'stopped'
        stop()
    elif jsonData['command'] == 'pause':
        state = 'paused'
        pause()
    elif jsonData['command'] == 'resume':
        state = 'playing'
        mixer.music.unpause()
    elif jsonData['command'] == 'seek':
        state = 'playing'
        seek(30)
    #declaring global variables for metadatas 
    global music_duration , metadata
    metadata = ad.load(directory+jsonData['music']) # loading music metadata for api 
    music_length = metadata['streaminfo']['duration'] 
    music_duration = time.strftime('%M:%S', time.gmtime(music_length))
    def convert(sec): #HEHE I LOVE STEALING CODE FROM THE INTERNET 
        #OH I MEANT GETTING INSPIRED BY THE INTERNET :D
        sec = sec % (24 * 3600)
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02d" % (min, sec) 


    return {
            "duration":music_duration,
            "music":jsonData['music'],
            "state":state
            }

@route('/list')
def musiclistReturn():
    list_data = dbInterface("show_playlist")
    return template('music_list.tpl',list_data = list_data)

@post('/update_list')
def playListFunction():
    dbInterface('update_playlist')

@post('/list_get')
def listGetAPI():
    data = dbInterface("show_playlist")
    return {"music_list":data}

run(host='0.0.0.0',port=8000,reloader=True)

