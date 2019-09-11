import vrep
clientID = 0
width = 800
height = 800
import math
import threading
import numpy as np
import time
import random


#Defining rotation matrices for calculations
def Ry(y):
    return np.array([[math.cos(y), 0, math.sin(y), 0],
                   [0, 1, 0, 0],
                   [-math.sin(y), 0, math.cos(y), 0],
                   [0, 0, 0, 1]])
def Rx(x):
    return np.array([[1, 0, 0, 0],
                   [0, math.cos(x), -math.sin(x), 0],
                   [0, math.sin(x), math.cos(x), 0],
                   [0, 0, 0, 1]])
def Rz(z):
    return np.array([[math.cos(z), -math.sin(z), 0, 0],
                   [math.sin(z), math.cos(z),0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
def Rt(xt,yt,zt):
    return np.asarray(Rz(zt).dot(Ry(yt).dot(Rx(xt)))).reshape(-1)[:12]
def rotationMatrix(angs):
    return np.asarray(Rz(math.radians(angs[2])).dot(Ry(math.radians(angs[1])).dot(Rx(math.radians(angs[0]))))).reshape(-1)[:12]



class Agent(object):
    def __init__(self, id, type, location):
        self.id = id
        self.type = type
        # type 0 = Guest, type 1 = Waiter
        self.location = location


class Guest(Agent):
    def __init__(self, id, location, groupId):
        self.id = id
        self.size = 20
        self.type = None
        self.location = location
        self.groupId = groupId
        self.billID = "" #Used to control the animated dolls in VREP
        self.current_status = "Idle"
        self.neediness_level = 0
        self.satisfaction = 0
        self.neediness_log = dict()
    def draw(self,canvas): #for drawing guest in the GUI
        canvas.create_oval(self.location[0]-self.size,self.location[1]-self.size,self.location[0]+self.size,self.location[1]+self.size,fill = "yellow")
        canvas.create_text(self.location[0], self.location[1], text=self.id + ":" + self.current_status)
    def move(self,place): #Updates position in the GUI and VREP
        self.current_status = "Idle"
        if place.approach_area != []:
            center = [abs(place.approach_area[0][0] + place.approach_area[2][0])//2,abs(place.approach_area[0][1] + place.approach_area[2][1])//2]
            self.location = center
        else: self.location = place.location
        self.vrepPos = (-(self.location[0]-width//2)/100,(self.location[1]-height//2)/100,0) #Updating VREP Position
        vrep.simxSetObjectPosition(clientID, self.moveBoxID, -1, self.vrepPos, vrep.simx_opmode_oneshot)
    def read(self,item): #Set state to read. Need to add animation in VREP
        assert(isinstance(item,Item))
        self.current_status = "Reading"
    def talk(self,person): #Set state to talking, Also sets the person who is being talked with to talking as well.
        assert(isinstance(person,Agent))
        self.current_status = "Talking"
        person.current_status = "Talking"
        self.lookAnimate(person)
        person.lookAnimate(self)
        self.talkAnimate()
        person.talkAnimate()


    def lookAnimate(self,object): #Vrep animation making person look at desired objectc
        ang = -math.atan2((self.location[1]-object.location[1]),(self.location[0]-object.location[0])) - self.vrepOrientation[2]
        if self.type == "Seated":
            self.currNeckPos = [0,0,math.degrees(ang)]
            vrep.simxSetSphericalJointMatrix(clientID, self.neckID, rotationMatrix(self.currNeckPos),
                                         vrep.simx_opmode_streaming)
    def talkAnimate(self): #Vrep animation making person talk (moves head up and down)
        def talkThread():
            currOrient = self.currNeckPos
            while self.current_status == "Talking":
                upAng = random.uniform(15, 20)
                tiltAng = random.uniform(-3, 3)
                finalUpperOrient = np.array([tiltAng, upAng, 0])
                diff = finalUpperOrient - currOrient
                for step in range(1, 100):
                    matrix = rotationMatrix(currOrient + diff * (step / 100))
                    e = vrep.simxSetSphericalJointMatrix(clientID, self.neckID, matrix,
                                                         vrep.simx_opmode_streaming)
                    time.sleep(0.02)
                currOrient = finalUpperOrient
                downAng = random.uniform(-15, -20)
                tiltAng = random.uniform(-3, 3)
                finalLowerOrient = np.array([tiltAng, downAng, 0])
                diff = finalLowerOrient - currOrient
                for step in range(1, 100):
                    matrix = rotationMatrix(currOrient + diff * (step / 100))
                    e = vrep.simxSetSphericalJointMatrix(clientID, self.neckID, matrix,
                                                         vrep.simx_opmode_streaming)
                    time.sleep(0.04)
                currOrient = finalLowerOrient
        threading.Thread(target=talkThread).start()


    def createVrep(self,pos,orientation): #Initializes VREP model of person
        error, self.vrepID = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/Walking Bill Chef Bot.ttm", 0,
                                  vrep.simx_opmode_blocking)
        self.type = "Walking"
        error,self.moveBoxID = vrep.simxGetObjectHandle(clientID,"Bill_goalDummy"+getBillString(self.billID),vrep.simx_opmode_oneshot_wait)
        self.vrepPos = pos
        self.vrepOrientation = orientation
        error,self.rightLegID = vrep.simxGetObjectHandle(clientID, 'Bill_rightLegJoint'+getBillString(self.billID), vrep.simx_opmode_oneshot_wait)
        error, self.leftLegID = vrep.simxGetObjectHandle(clientID, 'Bill_leftLegJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.rightKneeID = vrep.simxGetObjectHandle(clientID, 'Bill_rightKneeJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftKneeID = vrep.simxGetObjectHandle(clientID, 'Bill_leftKneeJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.rightAnkleID = vrep.simxGetObjectHandle(clientID, 'Bill_rightAnkleJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftAnkleID = vrep.simxGetObjectHandle(clientID, 'Bill_leftAnkleJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.neckID = vrep.simxGetObjectHandle(clientID, 'Bill_neck' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.rightArmID = vrep.simxGetObjectHandle(clientID, 'Bill_rightShoulderJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftArmID = vrep.simxGetObjectHandle(clientID, 'Bill_leftShoulderJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.rightElbowID = vrep.simxGetObjectHandle(clientID, 'Bill_rightElbowJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftElbowID = vrep.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        vrep.simxSetObjectPosition(clientID,self.vrepID,-1,(pos[0],pos[1],pos[2]),vrep.simx_opmode_oneshot)
        vrep.simxSetObjectPosition(clientID, self.moveBoxID, -1, (pos[0], pos[1], pos[2]), vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID,self.vrepID,-1,orientation,vrep.simx_opmode_oneshot)

    def seat(self,data,chair): #Seats person at desired chair. In VREP, switches model from a standing bill to a sitting bill
        data.bills.remove(self.billID)
        data.billID = getBillID(data.bills)
        self.type = "Seated"
        self.location = chair.location
        self.vrepOrientation = [0,0,chair.vrepOrientation[2]-math.pi/2]
        if self.vrepID != None:
            vrep.simxRemoveModel(clientID,self.vrepID,vrep.simx_opmode_oneshot)
        self.vrepPos = [chair.vrepPos[0],chair.vrepPos[1]-math.cos(chair.vrepOrientation[2])*-0.05,0]
        error, self.vrepID = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/IK Bill.ttm", 0,
                                  vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(clientID, self.vrepID, -1, (self.vrepPos[0], self.vrepPos[1], self.vrepPos[2]-0.4), vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID, self.vrepID, -1, self.vrepOrientation, vrep.simx_opmode_oneshot)
        error, self.rightLegID = vrep.simxGetObjectHandle(clientID, 'Bill_rightLegJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, rLeg = vrep.simxGetJointPosition(clientID, self.rightLegID, vrep.simx_opmode_streaming)
        error, self.leftLegID = vrep.simxGetObjectHandle(clientID, 'Bill_leftLegJoint' + getBillString(self.billID),
                                                         vrep.simx_opmode_oneshot_wait)
        error, self.rightKneeID = vrep.simxGetObjectHandle(clientID, 'Bill_rightKneeJoint' + getBillString(self.billID),
                                                           vrep.simx_opmode_oneshot_wait)
        error, self.leftKneeID = vrep.simxGetObjectHandle(clientID, 'Bill_leftKneeJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.rightAnkleID = vrep.simxGetObjectHandle(clientID,
                                                            'Bill_rightAnkleJoint' + getBillString(self.billID),
                                                            vrep.simx_opmode_oneshot_wait)
        error, self.leftAnkleID = vrep.simxGetObjectHandle(clientID, 'Bill_leftAnkleJoint' + getBillString(self.billID),
                                                         vrep.simx_opmode_oneshot_wait)
        error, self.neckID = vrep.simxGetObjectHandle(clientID, 'Bill_neck' + getBillString(self.billID),
                                                      vrep.simx_opmode_oneshot_wait)
        error, self.rightArmID = vrep.simxGetObjectHandle(clientID,
                                                          'Bill_rightShoulderJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftArmID = vrep.simxGetObjectHandle(clientID,
                                                         'Bill_leftShoulderJoint' + getBillString(self.billID),
                                                         vrep.simx_opmode_oneshot_wait)
        error, self.rightElbowID = vrep.simxGetObjectHandle(clientID,
                                                            'Bill_rightElbowJoint' + getBillString(self.billID),
                                                            vrep.simx_opmode_oneshot_wait)
        error, self.leftElbowID = vrep.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint' + getBillString(self.billID),
                                                           vrep.simx_opmode_oneshot_wait)

    def getJointValues(self): #Returns joint values in a tuple format from VREP
        error,rLeg = vrep.simxGetJointPosition(clientID, self.rightLegID, vrep.simx_opmode_streaming)
        error,lLeg = vrep.simxGetJointPosition(clientID, self.leftLegID, vrep.simx_opmode_streaming)
        error,rKnee = vrep.simxGetJointPosition(clientID, self.rightKneeID, vrep.simx_opmode_streaming)
        error,lKnee = vrep.simxGetJointPosition(clientID, self.leftKneeID, vrep.simx_opmode_streaming)
        error,rAnkle = vrep.simxGetJointPosition(clientID, self.rightAnkleID, vrep.simx_opmode_streaming)
        error,lAnkle = vrep.simxGetJointPosition(clientID, self.leftAnkleID, vrep.simx_opmode_streaming)
        error,rElbow = vrep.simxGetJointPosition(clientID, self.rightElbowID, vrep.simx_opmode_streaming)
        error,lElbow = vrep.simxGetJointPosition(clientID, self.leftElbowID, vrep.simx_opmode_streaming)
        error,rShoulder = vrep.simxGetJointMatrix(clientID, self.rightArmID, vrep.simx_opmode_streaming)
        error,lShoulder = vrep.simxGetJointMatrix(clientID, self.leftArmID, vrep.simx_opmode_streaming)
        error,neck = vrep.simxGetJointMatrix(clientID, self.neckID, vrep.simx_opmode_buffer)
        return (rLeg, lLeg, rKnee, lKnee, rAnkle, lAnkle, rElbow, lElbow, rShoulder, lShoulder, neck)

    def setJointPosition(self,jointID,pos): #Set a certain joint to given position
        vrep.simxSetJointPosition(clientID,jointID,pos,vrep.simx_opmode_streaming)

    def followJointAngles(self,AngleFunctions,timestep,numTimeStep): #Makes the model follow joint angles from a given function
        frequency = 25
        timeDelay = frequency/1000
        for currTime in range(0,frequency*(numTimeStep-1)):
            time.sleep(timeDelay)
            sampleTime = (currTime)/(frequency*(timestep/1000))
            print(sampleTime)
            self.setJointPosition(self.rightLegID,AngleFunctions[0](sampleTime))
            self.setJointPosition(self.leftLegID,AngleFunctions[1](sampleTime))
            self.setJointPosition(self.rightKneeID,AngleFunctions[2](sampleTime))
            self.setJointPosition(self.leftKneeID,AngleFunctions[3](sampleTime))
            self.setJointPosition(self.rightAnkleID,AngleFunctions[4](sampleTime))
            self.setJointPosition(self.leftAnkleID,AngleFunctions[5](sampleTime))


class Waiter(Agent):
    def __init__(self, id, location):
        self.id = id
        self.billID = ""
        self.size = 30
        self.location = location
        self.assignedTables = []
        self.task_log = []
        self.inventory = []
        self.current_status = "Idle"
    def draw(self,canvas): #draw waiter in GUI
        canvas.create_oval(self.location[0]-self.size,self.location[1]-self.size,self.location[0]+self.size,self.location[1]+self.size,fill = "green")
        canvas.create_text(self.location[0],self.location[1],text = self.id)
    def move(self,place): #move waiter in GUI and VREP
        self.location = place.location
        self.vrepPos = (-(self.location[0] - width // 2) / 100, (self.location[1] - height // 2) / 100, 0)
        vrep.simxSetObjectPosition(clientID, self.moveBoxID, -1, self.vrepPos, vrep.simx_opmode_oneshot)
    def give(self,item,person): #Not implemented yet
        assert(isinstance(item,Item) and isinstance(person,Agent))
        item.location = person.location
    def lookAnimate(self,object): #Same as for agent
        ang = -math.atan2((self.location[1]-object.location[1]),(self.location[0]-object.location[0]))
        self.vrepOrientation = [self.vrepOrientation[0],self.vrepOrientation[1],ang]
        vrep.simxSetObjectOrientation(clientID,self.vrepID,-1,self.vrepOrientation,vrep.simx_opmode_oneshot)

    def createVrep(self,pos,orientation): #Create waiter model
        error, self.vrepID = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/people/Walking Bill Chef Bot.ttm", 0,
                                  vrep.simx_opmode_blocking)
        self.type = "Walking"
        error,self.moveBoxID = vrep.simxGetObjectHandle(clientID,"Bill_goalDummy"+getBillString(self.billID),vrep.simx_opmode_oneshot_wait)
        self.vrepPos = pos
        self.vrepOrientation = orientation
        vrep.simxSetObjectPosition(clientID,self.vrepID,-1,(pos[0],pos[1],pos[2]),vrep.simx_opmode_oneshot)
        vrep.simxSetObjectPosition(clientID, self.moveBoxID, -1, (pos[0], pos[1], pos[2]), vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID,self.vrepID,-1,orientation,vrep.simx_opmode_oneshot)
        error, self.rightLegID = vrep.simxGetObjectHandle(clientID, 'Bill_rightLegJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftLegID = vrep.simxGetObjectHandle(clientID, 'Bill_leftLegJoint' + getBillString(self.billID),
                                                         vrep.simx_opmode_oneshot_wait)
        error, self.rightKneeID = vrep.simxGetObjectHandle(clientID, 'Bill_rightKneeJoint' + getBillString(self.billID),
                                                           vrep.simx_opmode_oneshot_wait)
        error, self.leftKneeID = vrep.simxGetObjectHandle(clientID, 'Bill_leftKneeJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.rightAnkleID = vrep.simxGetObjectHandle(clientID,
                                                            'Bill_rightAnkleJoint' + getBillString(self.billID),
                                                            vrep.simx_opmode_oneshot_wait)
        error, self.leftAnkleID = vrep.simxGetObjectHandle(clientID, 'Bill_leftAnkleJoint' + getBillString(self.billID),
                                                         vrep.simx_opmode_oneshot_wait)
        error, self.neckID = vrep.simxGetObjectHandle(clientID, 'Bill_neck' + getBillString(self.billID),
                                                      vrep.simx_opmode_oneshot_wait)
        error, self.rightArmID = vrep.simxGetObjectHandle(clientID,
                                                          'Bill_rightShoulderJoint' + getBillString(self.billID),
                                                          vrep.simx_opmode_oneshot_wait)
        error, self.leftArmID = vrep.simxGetObjectHandle(clientID,
                                                         'Bill_leftShoulderJoint' + getBillString(self.billID),
                                                         vrep.simx_opmode_oneshot_wait)
        error, self.rightElbowID = vrep.simxGetObjectHandle(clientID,
                                                            'Bill_rightElbowJoint' + getBillString(self.billID),
                                                            vrep.simx_opmode_oneshot_wait)
        error, self.leftElbowID = vrep.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint' + getBillString(self.billID),
                                                           vrep.simx_opmode_oneshot_wait)
    def getJointValues(self): #Store values of waiter
        error, rLeg = vrep.simxGetJointPosition(clientID, self.rightLegID, vrep.simx_opmode_streaming)
        error, lLeg = vrep.simxGetJointPosition(clientID, self.leftLegID, vrep.simx_opmode_streaming)
        error, rKnee = vrep.simxGetJointPosition(clientID, self.rightKneeID, vrep.simx_opmode_streaming)
        error, lKnee = vrep.simxGetJointPosition(clientID, self.leftKneeID, vrep.simx_opmode_streaming)
        error, rAnkle = vrep.simxGetJointPosition(clientID, self.rightAnkleID, vrep.simx_opmode_streaming)
        error, lAnkle = vrep.simxGetJointPosition(clientID, self.leftAnkleID, vrep.simx_opmode_streaming)
        error, rElbow = vrep.simxGetJointPosition(clientID, self.rightElbowID, vrep.simx_opmode_streaming)
        error, lElbow = vrep.simxGetJointPosition(clientID, self.leftElbowID, vrep.simx_opmode_streaming)
        error, rShoulder = vrep.simxGetJointMatrix(clientID, self.rightArmID, vrep.simx_opmode_streaming)
        error, lShoulder = vrep.simxGetJointMatrix(clientID, self.leftArmID, vrep.simx_opmode_streaming)
        error, neck = vrep.simxGetJointMatrix(clientID, self.neckID, vrep.simx_opmode_buffer)
        return (rLeg,lLeg,rKnee,lKnee,rAnkle,lAnkle,rElbow,lElbow,rShoulder,lShoulder,neck)

def newGuest(data,id,groupId,pos,orientation = [0,0,-math.pi/2]): #Creates new guest and places in VREP
    guest = Guest(id,pos,groupId)
    guest.billID = getBillID(data.bills)
    vrepPos = [-(guest.location[0]-data.width//2)/100,(guest.location[1]-data.height//2)/100,0]
    guest.createVrep(vrepPos,orientation)
    data.guests += [guest]
def newWaiter(data,id,pos,orientation = [0,0,-math.pi/2]): #Creates new waiter and places in VREP
    waiter = Waiter(id, pos)
    waiter.billID = getBillID(data.bills)
    vrepPos = [-(waiter.location[0]-data.width//2)/100,(waiter.location[1]-data.height//2)/100,0]
    waiter.createVrep(vrepPos, orientation)
    data.guests += [waiter]

def getBillID(bills): #Used to calculate appropiate Bill ID for models
    start = -1
    while start in bills:
        start += 1
    bills.add(start)
    print(bills)
    return start

def getBillString(billId): #Used to format BillID in appropiate manner
    if billId == -1: return ""
    else: return "#" + str(billId)
