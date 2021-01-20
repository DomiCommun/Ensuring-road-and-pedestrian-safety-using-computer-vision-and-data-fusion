#This code determine the location of points of interest on the video (example: crosswalk demarcations)
import numpy as np
import cv2
import pandas as pd
import imutils

Points=pd.DataFrame(columns=['Point_ID','location'])

cap = cv2.VideoCapture( 'Video1.avi')

nbreFrame=0

while(cap.isOpened()):
    
    ret, frame = cap.read()
    nbreFrame+=1
    frame = imutils.resize(frame, width=min(1100, frame.shape[1]))
    frame = imutils.resize(frame, width=600)

    r1 = cv2.selectROI(frame) #select point such as top left corner selection box is at CG object

    CG1=(int(r1[0]),int(r1[1]))
    point = cv2.circle(frame,CG1, 3, (0, 255, 0), 3)

    Points.loc[len(Points)] = [nbreFrame, CG1]

    Points.to_csv("Points.csv")

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
