import tkinter as tk
from tkinter import *
from tkinter import ttk ,FLAT
from PIL import Image, ImageTk, ImageGrab
import cv2
import numpy as np
import threading
import pyaudio
import wave
import os
import subprocess
import time
from datetime import datetime

VIDEO_SIZE = (800 , 420)
p = ImageGrab.grab()
a, b = p.size
chunk = 1024 
sample_format = pyaudio.paInt16 
channels = 2
fs = 44100 
frames = []
g = pyaudio.PyAudio() 
filename=(f'C://Users/{os.getlogin()}/desktop/temp_vid.mp4')
fourcc = cv2.VideoWriter_fourcc(*'X264')
frame_rate = 10
out = cv2.VideoWriter()
cap = cv2.VideoCapture(0)
#screen_rec part

def screen_capturing():
    
    global capturing
    capturing = True

    while capturing:
            
        img = ImageGrab.grab()
        frame = np.array(img)
        sc = np.array(img)
        curpos = root.winfo_pointerx(), root.winfo_pointery()
        cv2.circle(frame, curpos, 10, (0,255,255), 2)
        sc = cv2.resize(sc, VIDEO_SIZE)
        tkimage.paste(Image.fromarray(sc))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
        
def start_screen_capturing():
    
    if not out.isOpened():
         out.open(filename,fourcc, frame_rate,(a,b))
         
    print(' screen started')
    t1=threading.Thread(target=screen_capturing, daemon=True)
    t1.start()

def stop_screen_capturing():
    
    global capturing
    capturing = False
    out.release()
    print(' screen complete')
    
#voice recording part
    
def voice_recording():
    
    global recording
    while recording:
        data = stream.read(chunk)
        frames.append(data)

def start_voice_recording():
    
    global stream 
    stream = g.open(format=sample_format,channels=channels,rate=fs,frames_per_buffer=chunk,input=True)
    global recording
    recording = True
    print('voice rec')
    t2 = threading.Thread(target=voice_recording)                
    t2.start()

def stop_voice_recording():

    recording =False 
    print(' voice complete')
    filename=(f'C://Users/{os.getlogin()}/desktop/temp_voice.wav')  
    wf = wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(g.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

#merge both file
    
now = datetime.now()            
dt_file_name = now.strftime('"Rec_%Y-%m-%d-%H-%M-%S.mp4"')
os.chdir(f'C://Users/{os.getlogin()}/desktop/')

def merge_all():
    
  global p
  p =subprocess.Popen('ffmpeg -i temp_vid.mp4 -i temp_voice.wav -c:v copy -c:a aac -strict experimental -strftime 1 ' + dt_file_name ,stdin=subprocess.PIPE,creationflags = subprocess.CREATE_NO_WINDOW)
  time.sleep(2)
  print('merging done')
  os.remove('temp_vid.mp4')
  os.remove('temp_voice.wav')
  print('file delete done')

# --- webcam

webcam = None
WEBCAM_SIZE = (280, 200)

def read_frame(imgbox):
       
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, WEBCAM_SIZE)
            image = Image.fromarray(frame)
            imgbox.image.paste(image)
        webcam.after(20, read_frame, imgbox)

def stop_webcam(event):
    
    global webcam
    
    if webcam:
        webcam.destroy()
        webcam = None
        cap.release()
        
def start_webcam():
    
    global webcam
    cap.open(0)
    
    if webcam is None:
        cap.isOpened()
        webcam = tk.Toplevel()
        webcam.attributes("-topmost", True) 
        webcam.geometry('{}x{}+5+520'.format(WEBCAM_SIZE[0], WEBCAM_SIZE[1]))
        webcam.overrideredirect(1)
        imgbox = tk.Label(webcam)
        imgbox.pack()
        imgbox.image = ImageTk.PhotoImage(image=Image.new('RGB',WEBCAM_SIZE,(0,0,0)))
        imgbox.config(image=imgbox.image)
        read_frame(imgbox)
        webcam._offsetx = 0
        webcam._offsety = 0
        webcam.bind('<Button-1>',clickwin)
        webcam.bind('<B1-Motion>',dragwin)
        
def dragwin(event):
    
        x = webcam.winfo_pointerx() - webcam._offsetx
        y = webcam.winfo_pointery() - webcam._offsety
        webcam.geometry('+{x}+{y}'.format(x=x,y=y))

def clickwin(event):
    
        webcam._offsetx = event.x
        webcam._offsety = event.y

def change_icon():
    
        if main_btn.image == st_icon:
            start_screen_capturing()
            start_voice_recording()
            main_btn.config(image=sp_icon)
            main_btn.image = sp_icon
        else:
            stop_screen_capturing()
            stop_voice_recording()
            merge_all()
            main_btn.config(image=st_icon)
            main_btn.image = st_icon
def change_w():
    
        if webcam_btn.image == cam_icon:
            start_webcam()
            webcam_btn.config(image=com_icon)
            webcam_btn.image = com_icon
        else:
            stop_webcam(None)
            webcam_btn.config(image=cam_icon)
            webcam_btn.image = cam_icon
'''def change_button():
    
     if start_cap['text'] == 'Start Recording':
            start_voice_recording()
            start_screen_capturing()
            start_cap.config(text="Stop Recoding")
     else:
            stop_voice_recording()
            stop_screen_capturing()
            merge_all()
            start_cap.config(text="Start Recording")'''

root = tk.Tk()
img = PhotoImage(file=r'E:\project\videos\icon\rec.png')
root.tk.call('wm', 'iconphoto', root._w, img)
root.title('                                                                                                                        Screen Recorder')
root.geometry('+260+70')
root.resizable(width=False,height=False)
st_icon = PhotoImage(file=r'E:\project\videos\icon\play.png')
sp_icon = PhotoImage(file=r'E:\project\videos\icon\stop.png')
cam_icon = PhotoImage(file=r'E:\project\videos\icon\webcam0.png')
com_icon = PhotoImage(file=r'E:\project\videos\icon\webcam1.png')


tkimage = ImageTk.PhotoImage(Image.new('RGB', VIDEO_SIZE, (0,0,0)))

w, h = VIDEO_SIZE
vbox = tk.Label(root, image=tkimage, width=w, height=h, bg='black')
vbox.pack(pady=10,padx=25)

frame = tk.Frame(root)
frame.pack()

#start_cap = tk.Button(frame, text='Start Recording', width=30, command=change_button)
#start_cap.grid(row=0, column=0)

webcam_btn = tk.Button(frame, image=cam_icon, width=70,height= 80, relief=FLAT ,command=change_w)
webcam_btn.grid(row=0,column=2)
webcam_btn.image = cam_icon

main_btn = tk.Button(frame, image=st_icon, width=70,height=80, relief=FLAT ,command=change_icon)
main_btn.grid(row=0,column=1)
main_btn.image = st_icon

root.mainloop()
