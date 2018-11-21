import cv2
from time import sleep
import serial
from picamera import PiCamera
from picamera.array import PiRGBArray


# Adjustable parameters
threshold_center=20  # Image centering sensitivity

# Arduino
arduino = serial.Serial('/dev/ttyACM0',9600)

# Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Classifier
cascPath = "lbpcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
   
    try:
        if abs(gray.shape[1]/2-(faces[0][0]+faces[0][1]/2)) > threshold_center:
            #print(gray.shape[1]/2-(faces[0][0]+faces[0][1]/2))
            if gray.shape[1]/2-(faces[0][0]+faces[0][1]/2) > threshold_center:
                arduino.write(str.encode('D'))
            if gray.shape[1]/2-(faces[0][0]+faces[0][1]/2) < threshold_center:
                arduino.write(str.encode('I'))
                    
            
    except:
        pass
	# show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# When everything is done, release the capture and Arduino
cv2.destroyAllWindows()
camera.close()





