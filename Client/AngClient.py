import socket
import threading
import requests
import json
from collections.abc import Iterable
from gui import Gui
import time
import tkinter as tk
from datetime import datetime
import sys
import select
import pyaudio
myAfile=open("access token.txt",'r')
token=myAfile.read()
ServerPORT=55000
ServerIP='192.168.1.107'
MusicPort=65000
frames=[]
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100

def createUdpS():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('192.168.1.107',MusicPort))
    return udp

def music(udpsock):
    while True:
        sound,addr=udpsock.recvfrom(CHUNK*CHANNELS*2)#for clarity
        frames.append(sound)

def play():
    time.sleep(0.2)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK
                    )
    Buffer=10
    while True:
        print(len(frames))
        if len(frames)>Buffer:
            while True:
                if len(frames)>0:
                    stream.write(frames.pop(0))
                else:
                    break

def ServerConnection(Ssock):
    print("Client Conn thread lunched")
    try:
        with Ssock:
            print("Connected to server")
            while True:
                if gui.GuiElements['window'].state()!='normal' or not ui.is_alive():
                    break
                else:
                    ready = select.select([Ssock], [], [],5)
                    if ready[0]:
                        msg=Ssock.recv(1024).decode('utf8')
                        if msg[0]=='#':
                            gui.setLabel1("Playing: "+msg[1:])
                        else:
                            gui.addtobox(msg)
                    
            
        print("connection terminated")
    except Exception as e:
        print(e)

udpsock=createUdpS()
tempsocket=''
def connect():
    global tempsocket
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as s:
        #s.setblocking(0)
        tempsocket=s
        gui.GuiElements["input_box"].bind("<Key>", handle_keypres)
        gui.GuiElements["send_button"].configure(command=sendB)
        gui.GuiElements["input_box"].configure(state=tk.NORMAL)
        s.connect((ServerIP,ServerPORT))
        gets=threading.Thread(target=music,args=(udpsock,),daemon=True)
        pl=threading.Thread(target=play,daemon=True)
        gets.start()
        pl.start()
        gui.addtobox(s.recv(1024).decode('utf8'))
        s.sendall((uid+'-'+token).encode('utf8'))
        ServerConnection(s)


def sendB():
    text=gui.GuiElements["input_box"].get()
    tosend='['+getTimestamp()+']'+uid+'-> '+text
    tempsocket.sendall(tosend.encode('utf8'))
    gui.GuiElements["input_box"].delete(0,tk.END)
    print(text)
def handle_keypres(event):
    if event.char=='\r':
        text=gui.GuiElements["input_box"].get()
        tosend='['+getTimestamp()+']'+uid+'-> '+text
        tempsocket.sendall(tosend.encode('utf8'))
        gui.GuiElements["input_box"].delete(0,tk.END)
def getTimestamp():
    now = datetime.now()
    return now.strftime("%H:%M")

def connectb():
    gui.GuiElements["side_frame_sub_cred_uid"].configure(state='readonly')
    gui.GuiElements["side_frame_sub_cred_sip"].configure(state='readonly')
    gui.GuiElements["connect_button"].configure(state='disabled')

gui=Gui('client')
ui=threading.Thread(target=gui.initGui,daemon=True)
ui.start()
uid=''

#gui.GuiElements["connect_button"].configure(command=connectb)
try:
    while True:
        time.sleep(1.0)
        if gui.GuiElements['connect_button']['state']==tk.DISABLED:
            #take the uid
            uid=gui.GuiElements["side_frame_sub_cred_uid"].get()
            ServerIP=gui.GuiElements["side_frame_sub_cred_sip"].get()
            connect()
            break
except Exception as e:
    print('Program terminated wiht : \n',e)
    