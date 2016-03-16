import tweetpony
import cv2
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

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

