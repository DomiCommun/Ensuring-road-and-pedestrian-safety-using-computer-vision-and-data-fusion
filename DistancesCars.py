#Detect and store in a database the vehicles that are too close while moving / near accident detection and the vehicles that run a red light
import pandas as pd
from ast import literal_eval
import numpy as np

VehicleLocation=pd.read_csv('LocationVehicle.csv')
Vitesse=pd.read_csv('VitessesVehicle.csv')
LightColor=pd.read_csv('LightColor.csv')

frequence=15
NbreFrameMax=10000

#Outputs
DistancesCars=pd.DataFrame(columns=['frame', 'Index such that <Dlimit'])
RedLightRunning=pd.DataFrame(columns=['frame', 'time', 'Index of vehicle'])

dist=3
conv=0.02

nbframe=-frequence 

for index, line in VehicleLocation.iterrows():
    if index <NbreFrameMax:

        Loca=[] #to store vehicle locations
        V=[] #to store vehicle speed in pixels per second to see if vehicle is stopped or parked or moving
        time=index 

        for i in range (2, len(line)):
            if pd.isnull(line[i]):
                Loca.append(((0,0), i-1))
                vitesse = literal_eval(str(Vitesse.iloc[time, i - 1]))
                V.append((vitesse, i - 1))
               
            else:
                Loca.append((literal_eval(line[i]),i-1)) 
                vitesse = literal_eval(str(Vitesse.iloc[time,i-1]))
                V.append((vitesse, i-1))
                
#compute the distance between two vehicles and store vehicle indices when the distance is too short: near collision
        D=[]
        for i in range (2, len(V)):
            for j in range(2, 7):
                if i!=j:
                    n=0
                    if V[i][0][0]*V[j][0][0]>0:

                        diff0 = (Loca[i][0][0]) - (Loca[j][0][0])
                        diff1 = (Loca[i][0][1]) - (Loca[j][0][1])
                        distance=np.sqrt(diff1*diff1+diff0*diff0)
                        distanceMeter=distance*conv
                        D.append([distanceMeter, i, j])
                        if distanceMeter<dist:

                            DistancesCars.loc[len(DistancesCars)+1] = [time, (i,j)] #store indices of vehicle that do not respect safety distance
                        n+=1
#Detection of red light running
                        
        if time<len(TrafficLightColor) and TrafficLightColor.iloc[time]['Red']==1: 
        for Cars in Loca :

            P=Cars[0]

            if (P[1] < int((corner3F[1]-corner4F[1])/(corner3F[0]-corner4F[0])*(P[0]-corner4F[0])+corner4F[1])) and (P[1] > int((corner2B[1]-corner1B[1])/(corner2B[0]-corner1B[0])*(P[0]-corner1B[0])+corner1B[1])):
                print("Car after the stop line")
                RedLightRunning.loc[len(RedLightRunning)]= [time, time*0.09, Cars[1]]

            else:
                print("Car is okay")

DistancesCars.to_csv("NearCollision.csv")
RedLightRunning.to_csv('RedLightRunning.csv')
