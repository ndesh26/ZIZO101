#!/usr/bin/python
from _common import get_api
import time
import tweetpony
import twitter
from chatterbotapi import ChatterBotFactory, ChatterBotType
import cv2
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import thread
import time
import os
import signal
import sys
import time
from espeak import espeak
import record_audio
os.chdir('/home/nayan/Downloads/Desktop')
import serial 
from time import sleep
import sys

number = 0;
factory = ChatterBotFactory()
bot2 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
bot2session = bot2.create_session()
#connect to arduino by trying the following list of serial ports, mac need to be added
locations=['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3','/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',  
'/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3','COM6','COM4','COM3']    
connected =False #set connected to be false

#try each serial port, exit loop if one connects and set connected to True, else desplay failed to connect to any arduino
for device in locations:   
	#try to connect to current device 
    try:    
        #print ("Trying..."+device)  
        arduino = serial.Serial(device, 115200) 
        connected=True  
        break  
    except:    
        print ("Failed to connect on "+device)   

if connected ==False:
	 print ("\nFailed to connect on to any arduino")
else:
	print ("Successfully connected to arduino\n")

# Define a function for the thread
def face_tracking():
    counter=0
    num=0
    
    cap = cv2.VideoCapture(1)
    while (cap.isOpened()):
        ret,image = cap.read()
# Create the haar cascade
        faceCascade = cv2.CascadeClassifier('defaul.xml')
        time.sleep(0.005)
# Read the image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),

        )

        
# Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if(h>=80 and w>=80):
            
                    if(x>=200 and x<=280):
                        if(not (counter==1)):
                            arduino.write('s')
                            print 'center'
                            counter=1
                    elif(x>300):
                        if(not (counter==2)):
                            arduino.write('l')
                            #sleep(.05)
                            print 'left'
                            counter=2
                    else:
                        if(not (counter==3)):
                            arduino.write('r')
                           #sleep(.05)
                            print 'right'
                            counter=3 
                    
            
                
        cv2.imshow("Faces found", image)
        k=cv2.waitKey(10)
        if k==27:
            break
    cap.release()
    cv2.destroyAllWindows


   
def signal_handler(signal, frame):
    global number
    g = record_audio.main(number);
    
    if 'normal' in g:
        arduino.write('a')
    elif 'unhappy' in g:
        arduino.write('b')
    elif 'angry' in g:
        arduino.write('c')
    elif 'funny' in g:
        arduino.write('f')
    else:
        g = bot2session.think(g);
        print g
        i=0
        spaces=0
        while(i<len(g)):
            if g[i]==' ':
                spaces=spaces+1
            i=i+1
        arduino.write('p')
        espeak.synth(g)
        
        sleep((spaces+1)/3)
        arduino.write('q')
                   

               

    
# Create two threads as follows
try:
    thread.start_new_thread( face_tracking,() )
    thread.start_new_thread( twitter.twitter,() )
    print 'hi'
except:
   print "Error: unable to start thread"

signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C'
while True:
    time.sleep(1)
while 1:
   pass
