class Location(object):
    def __init__(self, id, location, corners, approach_area = [], total_area = []):
        self.id = id
        self.location = location
        self.corners = corners
        print(self.corners)
        self.approachArea = approach_area
        self.totalArea = total_area
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

class Chair(Location):
    def __init__(self, id, location, corners, approach_area = [], total_area = []):
        super().__init__(id, location, corners, approach_area, total_area)
        self.status = ["empty"]
        self.occupant = None
        self.color = "orange"
        self.text = self.id

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

def newTable(data,pos,size):
    corners = [(pos[0]+size//2,pos[1]+size//2),(pos[0]+size//2,pos[1]-size//2),(pos[0]-size//2,pos[1]-size//2),(pos[0]-size//2,pos[1]+size//2)]
    T = Table(len(data.objects),len(data.tables),pos,corners)
    data.tables += [T]
    data.objects += [T]
    return T

def newChair(data,id,pos,size):
    corners = [(pos[0] + size // 2, pos[1] + size // 2), (pos[0] + size // 2, pos[1] - size // 2),
               (pos[0] - size // 2, pos[1] - size // 2), (pos[0] - size // 2, pos[1] + size // 2)]
    C = Chair(id, pos, corners)
    data.objects += [C]
    return C

def newPodium(data,pos,width,height):
    corners = [(pos[0] + width // 2, pos[1] + height // 2), (pos[0] + width // 2, pos[1] - height // 2),
               (pos[0] - width // 2, pos[1] - height // 2), (pos[0] - width // 2, pos[1] + height // 2)]
    P = Podium(len(data.objects), pos, corners)
    data.objects += [P]
    return P

def newWaiterArea(data,id,pos,width,height):
    corners = [(pos[0] + width // 2, pos[1] + height // 2), (pos[0] + width // 2, pos[1] - height // 2),
               (pos[0] - width // 2, pos[1] - height // 2), (pos[0] - width // 2, pos[1] + height // 2)]
    P = WaiterArea(id, pos, corners)
    data.objects += [P]
    return P