import cv2
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray

# Adjustable parameters
threshold_center=50   # Image centering sensitivity

# GPIO
servoPIN = 17  # Conect signal servo pin to GPIO 17 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
pwm=GPIO.PWM(servoPIN,50)
pwm.start(2.5)
pwm.ChangeDutyCycle(7.5) # center
angle=90;

# Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Classifier
cascPath = "lbpcascade_frontalface_default.xml" # haarcascade_frontalface_default.xml
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
            #print(gray.shape[0]/2-(faces[0][0]+faces[0][1]/2))
            if gray.shape[1]/2-(faces[0][0]+faces[0][1]/2) > threshold_center:
                if angle<180:
                    angle=angle+5
                    DutyCycle = 1/18* (angle) + 2
                    pwm.ChangeDutyCycle(DutyCycle)
            if gray.shape[1]/2-(faces[0][0]+faces[0][1]/2) < threshold_center:
                if angle>0:
                    angle=angle-5
                    DutyCycle = 1/18* (angle) + 2
                    pwm.ChangeDutyCycle(DutyCycle)
            
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

# When everything is done, release the capture
cv2.destroyAllWindows()
camera.close()





