#AngServer
from User import User
import socket
import threading
from pathlib import Path
import os
from os.path import isfile, join
import json
#import pyping
import requests
import json
from collections.abc import Iterable
import pyaudio
import time
from datetime import datetime
from pydub import AudioSegment
PORT=55000
MusicPort=65000
userGroups={}
users={}
usercon=[]
frames=[]
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100
mypath="D:\\job\\Anghami\\songs\\"
#start broadcast for a group
def radioGroup(group):
    song=threading.Thread(target=setMusic,args=(group,),daemon=True)
    udpsock=CreateUDPs()
    radio=threading.Thread(target=Broadcastmusic,args=(udpsock,group),daemon=True)
    song.start()
    radio.start()

def buildPlayList(group):
    #mypath="D:\\job\\Anghami\\songs\\"
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    playlist=[]
    for filename in onlyfiles:
        if group.split('-')[0].lower() in filename.lower() or group.split('-')[1].lower() in filename.lower():
            playlist.append(filename)
    return playlist

def setMusic(group):
    print(group)
    PlayList=buildPlayList(group)
    p=pyaudio.PyAudio()
    stream=p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)
    #here
    #mypath="D:\\job\\Anghami\\songs\\"
    #onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    print(PlayList)
    for toplay in PlayList:
        if (toplay.split('.')[1]=='mp3' and toplay.split('.')[0]+'.wav' in PlayList) or (toplay.split('.')[1]=='wav' and toplay.split('.')[0]+'.mp3' in PlayList):
            toplay=toplay.split('.')[0]+'.wav'
            PlayList.remove(toplay.split('.')[0]+'.mp3')
            print(PlayList)
        else:
            if toplay.split('.')[1]=='mp3':
                dst=toplay.split('.')[0]+'.wav'
                sound=AudioSegment.from_mp3(toplay)
                sound.export(mypath+dst,format='wav')
                toplay=dst
        for conn in usercon:
            #conn.uid != ThisUser.uid and 
            if conn.group == group:
                conn.socket.sendall(("#"+toplay.split('-')[-1].split('.')[0]).encode('utf8'))
        with open(mypath+toplay,'rb') as fh:
            while fh.tell()!= os.path.getsize(mypath+toplay):
                Audio_Frame=fh.read(CHUNK)
                frames.append(Audio_Frame)
    

def Broadcastmusic(udpsock,group):
    #print(clientIp)
    while True:
        if len(frames)>0:
            for client in userGroups[group]:
                udpsock.sendto(frames[0],(client[1],MusicPort))
            frames.pop(0)
            
def CreateUDPs():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return udp

def compareStrings(str1, str2):   
    i = 0 
    while i < len(str1) - 1 and str1[i] == str2[i]:  
        i += 1 
    if str1[i] > str2[i]:  
        return -1 
    return str1[i] < str2[i] 
   
# Main function to find string 
def searchStr(arr, string, first, last):  
    if first > last: 
        return False 
    # Move mid to the middle  
    mid = (last + first) // 2 
    # If str is found at mid  
    if compareStrings(string, arr[mid]) == 0:  
        return True  
    # If str is greater than mid  
    if compareStrings(string, arr[mid]) < 0:  
        return searchStr(arr, string, mid+1, last)  
    # If str is smaller than mid  
    return searchStr(arr, string, first, mid-1)
#to print api response 
def prettyPrint(dictionary,ind):
    for sub in dictionary: 
        print(ind,sub,end=" : ") 
        if isinstance(dictionary[sub], list) :
            try:
                if isinstance(dictionary[sub][0],dict):
                    print('[')
                else:
                    print('[',end=" ")
            except IndexError:
                print('[]')
            except:
                print('{',end=" ")
            for i  in range(len(dictionary[sub])):
                if isinstance(dictionary[sub][i],dict):
                    print('--------------------------------------------------------------------------------------------')
                    prettyPrint(dictionary[sub][i],'\t')
                else:
                    if(i!=len(dictionary[sub])-1):
                        print(dictionary[sub][i],end=" , ")
                    else:
                        print(dictionary[sub][i],']')
        elif isinstance(dictionary[sub], dict):
            for sub2  in dictionary[sub]:
                print(ind,sub2,end=" : ") 
                if isinstance(dictionary[sub][sub2], list):
                    if isinstance(dictionary[sub][sub2][0],dict):
                        print('[')
                    else:
                        print('[',end=" ")
                    for i  in range(len(dictionary[sub][sub2])):
                        if isinstance(dictionary[sub][sub2][i],dict):
                            print('--------------------------------------------------------------------------------------------')
                            prettyPrint(dictionary[sub][sub2][i],'\t')
                        else:
                            if(i!=len(dictionary[sub][sub2])-1):
                                print(dictionary[sub][sub2][i],end=" , ")
                            else:
                                print(dictionary[sub][sub2][i],']')
        else:
            print(dictionary[sub])

def getFromAnghami(token,Aurl):
    host="https://bus.anghami.com/"
    headers={'XAT':'interns','XATH':token}
    r=requests.get(host+Aurl,headers=headers)
    return r.json()

def build_User_Prefrences(userID):
    #userid{'token':token,'pref':
    #   {'genre':{'pop':3,'rock':2,'country':1}
    #   'keywords':{'jaja':3,'funky':10,'chill':20}
    #   }
    # }
    todo3='public/user/likes'
    userLikes=getFromAnghami(users[userID]['token'],todo3)
    users[userID]['pref']={'genre':{},'keywords':{}}
    genre=[]
    keywords=[]
    for song in userLikes:
        genre.append(song['genre'])
        keywords.extend(song['keywords'])
    
    for sgenre in set(genre):
        users[userID]['pref']['genre'][sgenre]=genre.count(sgenre)
    
    for keyw in set(keywords):
        users[userID]['pref']['keywords'][keyw]=keywords.count(keyw)

def placeInGroup(userID,Clientsock,clip):
    print(clip)
    if not bool(userGroups):
        ma=0
        topgenre=''
        topkey=''
        for genre in users[userID]['pref']['genre']:
            if users[userID]['pref']['genre'][genre]>ma:
                topgenre=genre
                ma=users[userID]['pref']['genre'][genre]
        ma=0
        for keyword in users[userID]['pref']['keywords']:
            if users[userID]['pref']['keywords'][keyword]>ma:
                topkey=keyword
                ma=users[userID]['pref']['keywords'][keyword]
        userGroups['-'.join([topgenre,topkey])]=[(userID,clip)]
        #here
        radioGroup('-'.join([topgenre,topkey]))
        return User(userID,'-'.join([topgenre,topkey]),Clientsock)
    else:
        ma=0
        topgenre=''
        topkey=''
        for genre in users[userID]['pref']['genre']:
            if users[userID]['pref']['genre'][genre]>ma:
                topgenre=genre
                ma=users[userID]['pref']['genre'][genre]
        ma=0
        for keyword in users[userID]['pref']['keywords']:
            if users[userID]['pref']['keywords'][keyword]>ma:
                topkey=keyword
                ma=users[userID]['pref']['keywords'][keyword]
        upref='-'.join([topgenre,topkey])
        if upref in userGroups:
            userGroups[upref].append((userID,clip))
            return User(userID,upref,Clientsock)
        else:
            userGroups[upref]=[(userID,clip)]
            #here
            radioGroup(upref)
            return User(userID,upref,Clientsock)

def ClientConnection(Clientsock,addr):
    global x
    print("Client Conn thread lunched")
    try:
        with Clientsock:
            print("Connected by : ",addr)
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            tosend='*['+current_time+']-> Welcome to the Anhgamy Server'
            Clientsock.sendall(tosend.encode('utf8'))#1
            userID_userToken=Clientsock.recv(1024).decode('utf8').split("-")
            users[userID_userToken[0]]={'token':userID_userToken[1]}
            # we need to build his prefrencses
            build_User_Prefrences(userID_userToken[0])
            ThisUser=placeInGroup(userID_userToken[0],Clientsock,addr[0])
            #now to handle chat rooms then music 
            usercon.append(ThisUser)
            while True:
                received=Clientsock.recv(1024)
                for conn in usercon:
                    if conn.group == ThisUser.group:
                        conn.socket.sendall(received)

        print("connection terminated")
    except Exception as e:
        print("Exception happened : user Disconnect\n")
        x-=1
        for i in range(len(userGroups[ThisUser.group])):
            if userGroups[ThisUser.group][i][0]==ThisUser.uid:
                userGroups[ThisUser.group].pop(i)
        for i in range(len(usercon)):
            if ThisUser.uid==usercon[i].uid:
                usercon.pop(i)
                break

with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as s:
    testip="192.168.1.107" #sever ip
    s.bind((testip,PORT))
    s.listen()
    x=0
    while True:
        print("Connections : ",x)
        client , addr=s.accept()
        #need only ip addres from addr[0] 
        print(addr," has connected")
        con=threading.Thread(target=ClientConnection,args=(client,addr),daemon=True)
        con.start()
        x+=1
