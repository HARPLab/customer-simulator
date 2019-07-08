# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
import random

def randDrawTable(c):

    x, table = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/furniture/tables/customizable table.ttm", 0,
                                  vrep.simx_opmode_blocking)
    x, chair1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/furniture/chairs/dining chair.ttm", 0,
                                   vrep.simx_opmode_blocking)
    x, chair2 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/furniture/chairs/dining chair.ttm", 0,
                                   vrep.simx_opmode_blocking)
    x, spoon1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/household/spoon.ttm", 0,
                                   vrep.simx_opmode_blocking)
    x, fork1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/household/fork.ttm", 0,
                                   vrep.simx_opmode_blocking)
    x, pos = vrep.simxGetObjectPosition(clientID, spoon1, -1, vrep.simx_opmode_streaming)
    x, spoon2 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/household/spoon.ttm", 0,
                                   vrep.simx_opmode_blocking)
    x, fork2 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/household/fork.ttm", 0,
                                  vrep.simx_opmode_blocking)
    x, plate2 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/household/plate.ttm", 0,
                                   vrep.simx_opmode_blocking)
    x, plate1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/household/plate.ttm", 0,
                                           vrep.simx_opmode_blocking)
    x, plate1Pos = vrep.simxGetObjectPosition(clientID, plate1, -1, vrep.simx_opmode_streaming)
    vrep.simxSetObjectPosition(clientID, table, -1, (c[0], c[1], c[2]+0.65), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, plate2, -1, (c[0], c[1]+0.27, c[2]+0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, plate1, -1, (c[0], c[1]-0.27, c[2]+0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, spoon1, -1, (c[0] + 0.2, c[1] - 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)

    vrep.simxSetObjectPosition(clientID, fork1, -1, (c[0] - 0.2, c[1] - 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)

    vrep.simxSetObjectPosition(clientID, spoon2, -1, (c[0] - 0.2, c[1] + 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, fork2, -1, (c[0] + 0.2, c[1] + 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, spoon2, -1, (math.pi/2, 0, math.pi/2), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, fork2, -1, (math.pi/2,0, math.pi/2), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, chair2, -1, (0, 0, math.pi), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, chair2, -1, (c[0], c[1] - 0.82,c[2] + 0.45), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, chair1, -1, (c[0],c[1] + 0.82,c[2] + 0.45), vrep.simx_opmode_oneshot)
    #x, person1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/Sitting Bill.ttm", 0,vrep.simx_opmode_blocking)
    #vrep.simxSetObjectPosition(clientID, person1, -1, (c[0], c[1] + 0.5, c[2]), vrep.simx_opmode_oneshot)\

    #print(pos)
    r = 2
    #print(r)
    if r == 0:
        x, person1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/IK Bill.ttm", 0,
                                        vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(clientID, person1, -1, (c[0], c[1] + 0.45, c[2]), vrep.simx_opmode_oneshot)
    elif r == 1:
        x, person2 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/IK Bill.ttm", 0,
                                        vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(clientID, person2, -1, (c[0], c[1] - 0.45, c[2]), vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID, person2, -1, (0, 0, math.pi / 2), vrep.simx_opmode_oneshot)
    else:
        x, person2 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/IK Bill.ttm", 0,
                                        vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(clientID, person2, -1, (c[0], c[1] - 0.45, c[2]), vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID, person2, -1, (0, 0, math.pi / 2), vrep.simx_opmode_oneshot)
        x, person1 = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/IK Bill.ttm", 0,
                                        vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(clientID, person1, -1, (c[0], c[1] + 0.45, c[2]), vrep.simx_opmode_oneshot)
    time.sleep(40)
    x, pos = vrep.simxGetObjectPosition(clientID, spoon1, -1, vrep.simx_opmode_buffer)
    time.sleep(1)
    x, plate1Pos = vrep.simxGetObjectPosition(clientID, plate1, -1, vrep.simx_opmode_buffer)
    print(plate1Pos)
    print(pos)
    x, rightArm = vrep.simxGetObjectHandle(clientID, 'rightArm', vrep.simx_opmode_oneshot_wait)
    vrep.simxSetObjectPosition(clientID, rightArm, -1, pos, vrep.simx_opmode_oneshot)
    time.sleep(2)
    finalPos = [0, (-0.15) - 0.45, 0.95]
    diff = [finalPos[0] - pos[0], finalPos[1] - pos[1], finalPos[2] - pos[2]]
    for i in range(1,10):
        diff = [finalPos[0] - pos[0], finalPos[1] - pos[1], finalPos[2] - pos[2]]
        finalPos = [0 + random.uniform(-0.0025,-0.0025), (-0.155) - 0.45 + random.uniform(-0.0025,-0.0025), 1.1+ random.uniform(-0.0025,-0.0025)]
        diff = [finalPos[0] - pos[0], finalPos[1] - pos[1], finalPos[2] - pos[2]]
        for i in range(1,100):
            #vrep.simxSetObjectOrientation(clientID,rightArm,-1,(math.radians(-48)*(i/100),math.radians(-17)*(i/100),math.radians(78)*(i/100)),vrep.simx_opmode_oneshot)
            vrep.simxSetObjectPosition(clientID,rightArm,-1,[pos[0] + diff[0]*(i/100),pos[1] + diff[1]*(i/100),pos[2] + diff[2]*(i/100)],vrep.simx_opmode_oneshot)
            time.sleep(1/30)
        finalPos2 = [plate1Pos[0]+ random.uniform(-0.07,0.07),plate1Pos[1]+ random.uniform(-0.07,0.07),plate1Pos[2]]
        diff2 = [finalPos2[0]-finalPos[0],finalPos2[1]-finalPos[1],finalPos2[2]-finalPos[2]]
        for i in range(1,100):
            #vrep.simxSetObjectOrientation(clientID,rightArm,-1,(math.radians(-48)*(i/100),math.radians(-17)*(i/100),math.radians(78)*(i/100)),vrep.simx_opmode_oneshot)
            vrep.simxSetObjectPosition(clientID,rightArm,-1,[finalPos[0] + diff2[0]*(i/100),finalPos[1] + diff2[1]*(i/100),finalPos[2] + diff2[2]*(i/100)],vrep.simx_opmode_oneshot)
            time.sleep(1/30)
        pos = finalPos2[:]





print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')

    #generateTables()
    randDrawTable((0, 0, 0))


    time.sleep(2)
    vrep.simxGetPingTime(clientID)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
