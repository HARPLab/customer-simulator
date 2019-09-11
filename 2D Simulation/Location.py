import vrep
clientID = 0
width = 800
height = 800

#Classes here for different objects in scene.

class Location(object):
    def __init__(self, id, location, corners, approach_area = [], total_area = []):
        self.id = id
        self.location = location
        self.corners = corners
        self.approach_area = approach_area
        self.total_area = total_area
        self.color = "white"
        self.text = ""
    def draw(self,canvas):
        canvas.create_polygon(self.corners,fill = self.color,width = 10)
        canvas.create_text(self.location[0],self.location[1], text = self.text,fill = "white")


class Table(Location):
    def __init__(self, id, tableId,location, corners,approach_area = [], total_area = []):
        super().__init__(id, location, corners, approach_area, total_area)
        self.tableId = tableId
        self.current_group = None
        self.status = ["clean"]
        self.color = "blue"
        self.text = "Table " + str(self.tableId)
    def createVrep(self,pos,orientation):
        error, self.vrepID = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/furniture/tables/table chef bot.ttm", 0,
                                  vrep.simx_opmode_blocking)
        self.vrepPos = pos
        self.vrepOrientation = orientation
        vrep.simxSetObjectPosition(clientID,self.vrepID,-1,(pos[0],pos[1],pos[2]),vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID,self.vrepID,-1,orientation,vrep.simx_opmode_oneshot)

class Chair(Location):
    def __init__(self, id, location, corners, approach_area = [], total_area = []):
        super().__init__(id, location, corners, approach_area, total_area)
        self.status = ["empty"]
        self.occupant = None
        self.color = "orange"
        self.text = self.id
    def createVrep(self,pos,orientation):
        error, self.vrepID = vrep.simxLoadModel(clientID, "/home/steelshot/vrep/models/furniture/chairs/dining chair.ttm", 0,
                                  vrep.simx_opmode_blocking)
        self.vrepPos = pos
        self.vrepOrientation = orientation
        vrep.simxSetObjectPosition(clientID,self.vrepID,-1,(pos[0],pos[1],pos[2]),vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID,self.vrepID,-1,orientation,vrep.simx_opmode_oneshot)

class WaiterArea(Location):
    def __init__(self,id,location,corners,approach_area = [],total_area = []):
        super().__init__(id,location,corners,approach_area,total_area)
        self.text = self.id
        self.color = "cyan"



class Podium(Location):
    def __init__(self,id,location,corners,approach_area = [],total_area = []):
        super().__init__(id,location,corners,approach_area,total_area)
        self.text = "Podium"
        self.color = "red"


class Register(Location):
    def __init__(self,id,location,corners,approach_area = [],total_area = []):
        super().__init__(id, location, corners, approach_area, total_area)
        self.status = None

#Functions to create the objects in VREP and the GUI

def newTable(data,id,pos,vrepOrientation = [0,0,0]):
    corners = [(pos[0]+60,pos[1]+40),(pos[0]+60,pos[1]-40),(pos[0]-60,pos[1]-40),(pos[0]-60,pos[1]+40)]
    T = Table(id,len(data.tables),pos,corners)
    vrepPos = [-(T.location[0]-data.width//2),T.location[1]-data.height//2,65] # 0.65 for height
    for i in range(len(vrepPos)):
        vrepPos[i] = vrepPos[i]/100
    T.createVrep(vrepPos,vrepOrientation)
    data.tables += [T]
    data.objects += [T]
    return T

def newChair(data,id,pos,vrepOrientation = [0,0,0]):
    size = 45
    corners = [(pos[0] + size//2, pos[1] + size // 2), (pos[0] + size // 2, pos[1] - size // 2),
               (pos[0] - size // 2, pos[1] - size // 2), (pos[0] - size // 2, pos[1] + size // 2)]
    approach_area = [(pos[0] + size//2-size, pos[1] + size // 2), (pos[0] + size // 2-size, pos[1] - size // 2),
               (pos[0] - size // 2-size, pos[1] - size // 2), (pos[0] - size // 2-size, pos[1] + size // 2)]
    C = Chair(id, pos, corners,approach_area)
    vrepPos = [-(C.location[0]-width//2),C.location[1]-height//2, 45] # 0.65 for height
    for i in range(len(vrepPos)):
        vrepPos[i] = vrepPos[i]/100
    C.createVrep(vrepPos, vrepOrientation)
    data.objects += [C]
    return C

def newPodium(data,id,pos,width,height):
    corners = [(pos[0] + width // 2, pos[1] + height // 2), (pos[0] + width // 2, pos[1] - height // 2),
               (pos[0] - width // 2, pos[1] - height // 2), (pos[0] - width // 2, pos[1] + height // 2)]
    P = Podium(id, pos, corners)
    data.objects += [P]
    return P

def newWaiterArea(data,id,pos,width,height):
    corners = [(pos[0] + width // 2, pos[1] + height // 2), (pos[0] + width // 2, pos[1] - height // 2),
               (pos[0] - width // 2, pos[1] - height // 2), (pos[0] - width // 2, pos[1] + height // 2)]
    P = WaiterArea(id, pos, corners)
    data.objects += [P]
    return P
