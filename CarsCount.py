#count vehicles at intersection
import pandas as pd

VehicleLocation=pd.read_csv('PositionVehicles.csv')
PedestrianLocation=pd.read_csv('PositionPedestrians.csv')

VehicleCount=pd.DataFrame(columns=['frame', 'count'])
PedestrianCount=pd.DataFrame(columns=['frame', 'count'])



for i in range(0, len(VehicleLocation), 20): #tous les 20 frames
    
    line=VehicleLocation.iloc[i]
    nb=-1 #first column is frame number so do not count in number of vehicles
    for elem in line:
        if pd.isnull(elem)==False:
            nb=nb+1
            
    VehicleCount.loc[len(VehicleCount)]= [i, nb]


for i in range(0, len(PedestrianLocation), 20):
 
    line=PedestrianLocation.iloc[i]
    nb=-1 
    for elem in line:
        if pd.isnull(elem)==False:
            nb=nb+1
            
    PedestrianCount.loc[len(PedestrianCount)]= [i, nb]

VehicleCount.to_csv("VehcileCount.csv")
PedestrianCount.to_csv("PedestrianCount.csv")
