#!/usr/bin/python
from _common import get_api
import time
import tweetpony
from chatterbotapi import ChatterBotFactory, ChatterBotType
import cv2
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import thread
import time
import os
#import record_audio
import signal
import sys

import time
from espeak import espeak
import record_audio
os.chdir('/home/nayan/Downloads/Desktop')

#import modules
import serial 
from time import sleep
import cv2
import sys
number = 50;
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
    
    cap = cv2.VideoCapture(0)
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


   
def twitter():
    def take_image():
    # Camera 0 is the integrated web cam on my netbook
        camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
        ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
        camera = cv2.VideoCapture(camera_port)
 
# Captures a single image from the camera and returns it in PIL format
    
 
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
        for i in xrange(ramp_frames):
            retval, im = camera.read()
            temp = im
        print("Taking image...")
# Take the actual image we want to keep
        retval, im = camera.read()
        camera_capture = im
        file = "/home/nayan/Desktop/test_image.png"
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
        cv2.imwrite(file, camera_capture)
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
        del(camera)


        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() # 
        drive = GoogleDrive(gauth)

        file1 = drive.CreateFile()  # Create GoogleDriveFile instance with title 'Hello.txt'
        file1.SetContentFile('/home/nayan/Desktop/test_image.png') # Set content of the file from given string
        file1.Upload()
        return file1['webContentLink']

    def main():
        factory = ChatterBotFactory()
        print 'hi'
        bot2 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
        bot2session = bot2.create_session()

        api = get_api()
        if not api:
            return
        try:
            status = api.received_messages(count=1)
        except tweetpony.APIError as err:
            print "Oh no! Your tweet could not be sent. Twitter returned error #%i and said: %s" % (err.code, err.description)
        else:
           message_id=status[0]['id']
           user_id=status[0]['sender_screen_name']
        status = api.received_messages(since_id=message_id)
        while(1):
            if status:
                message_id=status[0]['id']
                user_id=status[0]['sender_screen_name']
                s = status[0]['text']
                if s=='Take':
                
                    s='You can download the image from the link - '+take_image();
                else:
                    s = bot2session.think(s);
                api.send_message(screen_name=user_id,text=s)
            time.sleep(60)
            status=api.received_messages(since_id=message_id)           
            
   # if __name__ == "__main__":
    main()        
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
    #thread.start_new_thread( face_tracking,() )
    #thread.start_new_thread( twitter,() )
    sleep(.5)
    arduino.write('a')
    espeak.set_voice('hindi')
    
    
    g='Hi I am zizo one oh one. I am a social robot. I can interact with people and track them. I can show various expressions like sadness, anger happiness etc. '
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
    
    arduino.write('b')
    sleep(1)
    arduino.write('c')
    sleep(1)
    arduino.write('f')
    sleep(1)
    arduino.write('b')
    sleep(1)
    arduino.write('c')
    sleep(1)
    arduino.write('f')
    sleep(1)
    arduino.write('e')
    sleep(1)
    arduino.write('a')
    g=' I can take pictures on demand and send them to you over internet and chat with you on twitter.'
    i=0
    spaces=0
    while(i<len(g)):
        if g[i]==' ':
            spaces=spaces+1
        i=i+1
    arduino.write('p')
    
    espeak.synth(g)
    sleep((spaces+1)/4)
    arduino.write('q')
except:
   print "Error: unable to start thread"

signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C'
while True:
    time.sleep(1)
while 1:
   pass
