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
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

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
    vrep.simxSetObjectPosition(clientID, table, -1, (c[0], c[1], c[2] + 0.65), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, plate2, -1, (c[0], c[1] + 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, plate1, -1, (c[0], c[1] - 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, spoon1, -1, (c[0] + 0.2, c[1] - 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)

    vrep.simxSetObjectPosition(clientID, fork1, -1, (c[0] - 0.2, c[1] - 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)

    vrep.simxSetObjectPosition(clientID, spoon2, -1, (c[0] - 0.2, c[1] + 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, fork2, -1, (c[0] + 0.2, c[1] + 0.27, c[2] + 0.72), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, spoon2, -1, (math.pi / 2, 0, math.pi / 2), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, fork2, -1, (math.pi / 2, 0, math.pi / 2), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, chair2, -1, (0, 0, math.pi), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, chair2, -1, (c[0], c[1] - 0.82, c[2] + 0.45), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectPosition(clientID, chair1, -1, (c[0], c[1] + 0.82, c[2] + 0.45), vrep.simx_opmode_oneshot)
    r = random.randint(0,2)
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



import random


def generateCoordinates(size, minDistance):
    numTables = random.randint(size, (size * 1.5) // 1)
    Board = [([0] * size) for i in range(size)]
    Board[size // 2][size // 2] = 1
    options = []
    seen = [(size // 2, size // 2)]
    for i in range(size):
        for j in range(size):
            if i == size // 2 and j == size // 2: continue
            options += [(i, j)]
    random.shuffle(options)
    random.shuffle(options)

    def isLegalTableAdd(choice, seen):
        for item in seen:
            if abs(choice[0] - item[0]) <= 1 and abs(choice[1] - item[1]) <= 1:
                return False
        for item in seen:
            if abs(choice[0] - item[0]) <= 2 and abs(choice[1] - item[1]) <= 2:
                return True
        return False

    def addTables(Board, seen, options, depth):
        if depth == 0: return Board
        for i in range(len(options)):
            if isLegalTableAdd(options[i], seen):
                seen += [options[i]]
                newOptions = options[:i] + options[i + 1:]
                Board[options[i][0]][options[i][1]] = 1
                if addTables(Board, seen, newOptions, depth - 1) != None:
                    return Board
                else:
                    Board[options[i][0]][options[i][1]] = 0
                    seen.remove(options[i])
        return None

    FinalBoard = addTables(Board, seen, options, numTables - 1)
    coordinates = []
    for item in seen: coordinates += [((item[0] - size // 2) * minDistance, (item[1] - size // 2) * minDistance, 0)]
    print(coordinates)
    return coordinates


print('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1', 19990, True, True, 5000, 5)  # Connect to V-REP
if clientID != -1:
    print('Connected to remote API server')
    time.sleep(2)
    coordinates = generateCoordinates(random.randint(5,7), random.uniform(1.3,1.7))
    for c in coordinates:
        randDrawTable(c)
    time.sleep(3)
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)
else:
    print('Failed connecting to remote API server')
print('Program ended')
