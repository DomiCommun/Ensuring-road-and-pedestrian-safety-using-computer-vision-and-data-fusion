#Detect people jaywalking, when they jaywalked and store number of people who jaywalked at each time 

import pandas as pd
from ast import literal_eval

#inputs
PedestrianLocation=pd.read_csv('LocationPedestrians.csv')
TrafficLightColor=pd.read_csv('LightColor.csv')
WalkingSignal=pd.read_csv('PedestrianLightColor.csv')
CrosswalkDemarcation=pd.read_csv('CrosswalkCorners.csv') 
frequence=15

#Outputs
Jaywalking=pd.DataFrame(columns=['frame', 'Person_ID'])

#Crosswalk coordinates - from crosswalkDemarcation code
#Crosswalk 1
corner1B = (129, 165)
corner2B = (269, 135)
corner3B = (334, 150)
corner4B = (145, 195)
# crosswalk 2
corner1F = (302, 275)
corner2F = (466, 188)
corner3F = (582, 250)
corner4F = (514, 393)


nbframe=-frequence

for index, line in PedestrianLocation.iterrows():

    Loca=[] #to store pedestrian locations
    time=index 

    for i in range (1, len(line)):
        if pd.isnull(line[i]):
            Loca.append(((0,0), i-1)) 
        else:
            Loca.append((literal_eval(line[i]),i-1))

    if WalkingSignal.iloc[time]['Red']==1: #Detect if a pedestrian start crossing the street while the walking signal is red
        for Person in Loca :
            P=Person[0]
            #check if the pedestrian is located on sidewalk or on crosswalk or road
            if (P[1] < int((corner1B[1]-corner4F[1])/(corner1B[0]-corner4F[0])*(P[0]-corner4F[0])+corner4F[1])) and (P[1] > int((corner2B[1]-corner3F[1])/(corner2B[0]-corner3F[0])*(P[0]-corner3F[0])+corner3F[1])):
                print('Pedestrian jaywalks')
                Jaywalking.loc[len(Jaywalking)]= [time, Person[1]]

            else:
                print("Pedestrian is okay")

Jaywalking.to_csv("Jaywalking.csv")
