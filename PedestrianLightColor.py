#Detect the walking signal color on video and store its state for each time in a table

import numpy as np
import cv2
import pandas as pd
import imutils

cap = cv2.VideoCapture( 'VideoTrafficSignal.avi')
LightColorWithOrange=pd.DataFrame(columns=['frame','Green', 'Orange', 'Red'])

out = cv2.VideoWriter('TrafficLightColorDetection.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (2592, 1944))

boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    # ([25, 146, 190], [62, 174, 250]),
]
Nframe=0
timer=0
TurnedOrange=[]

while(cap.isOpened()):
 
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=min(1100, frame.shape[1]))
    #frame = imutils.resize(frame, width=600)
    Nframe=Nframe+1

    imgCrop = frame[87:(87+46), 511:(511+26)] #focus where the light signal is located on the image
    (h, w) = frame.shape[:2]

    #detect green 
    lowerBoundGreen = np.array([0, 93, 77])
    upperBoundGreen = np.array([82, 255, 102])
    lowerBoundGreen = np.array(lowerBoundGreen, dtype="uint8")
    upperBoundGreen = np.array(upperBoundGreen, dtype="uint8")

    # detect red
    lowerBoundRed = np.array([17, 15, 100])
    upperBoundRed = np.array([50, 56, 200])
    lowerBoundRed = np.array(lowerBoundRed, dtype="uint8")
    upperBoundRed = np.array(upperBoundRed, dtype="uint8")

    #detect orange 
    lowerBoundOrange = np.array([10, 100, 20])
    upperBoundOrange = np.array([25, 255, 255])
    lowerBoundYellow = np.array(lowerBoundOrange, dtype="uint8")
    upperBoundYellow = np.array(upperBoundOrange, dtype="uint8")


    # convert the image to HSV
    imgRGB=imgCrop
    imgHSV = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
    #create a filter - mask for green, red and orange colors to detect the colors
    maskGreen = cv2.inRange(imgRGB, lowerBoundGreen, upperBoundGreen)
    maskRed= cv2.inRange(imgRGB, lowerBoundRed, upperBoundRed)
    maskOrange = cv2.inRange(imgRGB, lowerBoundOrange, upperBoundOrange)

    _, contoursGreen, _ = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contoursRed, _ = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contoursOrange, _ = cv2.findContours(maskOrange.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    corner=[]

#store light color and time in a table and print the color detection on the image to detect FP and FN
    if len(contoursRed)>=2:
        cv2.putText(frame,'red',(150, 800),cv2.FONT_HERSHEY_SIMPLEX,5, (255, 255,255),2)
        LightColorWithOrange.loc[len(LightColorWithOrange)] = [Nframe, 0, 0, 1]

    if len(contoursOrange)>3:

        LightColorWithOrange.loc[len(LightColor)]=[Nframe, 0, 1, 0]
        x, y, w, h = cv2.boundingRect(contoursOrange[1])

        cv2.putText(imgCrop,'orange',(110, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0,0), 2)

    if len(contoursOrange)<=3 and len(contoursRed)<=2:
        LightColorWithOrange.loc[len(LightColor)] = [Nframe, 1,0, 0]
        cv2.putText(frame,'green',(150, 800),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0,0), 2)


    #cv2.imshow("mask", imgCrop)
    cv2.imshow('frame', frame)
    out.write(frame)

    LightColorWitgOrange.to_csv("TrafficSignalColor.csv")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

LightColorWithOrange.to_csv("TrafficSignalColor.csv")
out.release()
cap.release()
cv2.destroyAllWindows()

