import cv2
import sys
from time import sleep
import serial

# Adjustable parameters

threshold_center=50 
arduino = serial.Serial("COM4", 9600)


# Code
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(1)
sleep(5)

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame

    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
   
    try:
        if abs(gray.shape[0]/2-(faces[0][0]+faces[0][1]/2)) > threshold_center:
            print(gray.shape[0]/2-(faces[0][0]+faces[0][1]/2))
            if gray.shape[0]/2-(faces[0][0]+faces[0][1]/2) > threshold_center:
                arduino.write(str.encode('D'))
            if gray.shape[0]/2-(faces[0][0]+faces[0][1]/2) < threshold_center:
                arduino.write(str.encode('I'))

            
    except:
        pass
    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)


# When everything is done, release the capture and Arduino
video_capture.release()
cv2.destroyAllWindows()
arduino.close()
