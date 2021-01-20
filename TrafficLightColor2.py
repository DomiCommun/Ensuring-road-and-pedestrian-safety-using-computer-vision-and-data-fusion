
# Detect vehicle light color and store color and time in a table

import numpy as np
import cv2
import pandas as pd

cap = cv2.VideoCapture( 'VideoIntersection.avi')
LightColor=pd.DataFrame(columns=['frame','Green', 'Orange', 'red'])

out = cv2.VideoWriter('TrafficLightColorDetection.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (2592, 1944))

boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    # ([25, 146, 190], [62, 174, 250]),
]
Nframe=0

while(cap.isOpened()):
    ret, frame = cap.read()
    Nframe=Nframe+1

    imgCrop = frame[0:200, 750:1000]
    (h, w) = frame.shape[:2]

    #detect green
    lowerBoundGreen = np.array([33, 80, 40])
    upperBoundGreen = np.array([102, 255, 255])
    lowerBoundGreen = np.array(lowerBoundGreen, dtype="uint8")
    upperBoundGreen = np.array(upperBoundGreen, dtype="uint8")

    # detect red
    lowerBoundRed = np.array([17, 15, 100])
    upperBoundRed = np.array([50, 56, 200])
    lowerBoundRed = np.array(lowerBoundRed, dtype="uint8")
    upperBoundRed = np.array(upperBoundRed, dtype="uint8")

    #detect orange 255 165 0
    lowerBoundOrange = np.array([10, 100, 20])
    upperBoundOrange = np.array([25, 255, 255])
    lowerBoundYellow = np.array(lowerBoundOrange, dtype="uint8")
    upperBoundYellow = np.array(upperBoundOrange, dtype="uint8")
    #detect yellow
    lowerBoundYellow = np.array([25, 146, 190])
    upperBoundYellow = np.array([62, 174, 250])
    lowerBoundYellow = np.array(lowerBoundYellow, dtype="uint8")
    upperBoundYellow = np.array(upperBoundYellow, dtype="uint8")
    # convert the image to HSV
    imgHSV=imgCrop

    # create a filter - mask for each colors 
    maskGreen = cv2.inRange(imgHSV, lowerBoundGreen, upperBoundGreen)
    maskRed= cv2.inRange(imgHSV, lowerBoundRed, upperBoundRed)
    maskOrange = cv2.inRange(imgHSV, lowerBoundOrange, upperBoundOrange)
    # try to improve the quality of green color because trees might biase results
    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))
    maskOpen = cv2.morphologyEx(maskGreen, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)


    _, contoursGreen, _ = cv2.findContours(maskClose.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contoursRed, _ = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contoursOrange, _ = cv2.findContours(maskOrange.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    corner=[]
#detect light color and print output detetcion on video to see FP and FN
    if len(contoursRed)>2:
        x, y, w, h = cv2.boundingRect(contoursRed[1])
        cv2.putText(frame,'red',(150, 800),

        LightColor.loc[len(LightColor)]=[Nframe, 0, 0, 1]

    if len(contoursOrange)>3:

        LightColor.loc[len(LightColor)]=[Nframe, 0, 1, 0]
        x, y, w, h = cv2.boundingRect(contoursOrange[1])
  
        cv2.putText(frame,'orange',(150, 800),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0,0), 2)

    if len(contoursOrange)<=3 and len(contoursRed)<=2:
        LightColor.loc[len(LightColor)] = [Nframe, 1,0, 0]
        cv2.putText(frame,'green',(150, 800),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0,0), 2)


    cv2.imshow('frame', frame)

    out.write(frame)

    LightColor.to_csv("LightColor.csv") #essayer de le mettre autre part dans le code car prend du tps a computer je pense

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

LightColor.to_csv("LightColor.csv")
out.release()
cap.release()
cv2.destroyAllWindows()




