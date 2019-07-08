class Agent(object):
    def __init__(self, id, type, location):
        self.id = id
        self.type = type
        # type 0 = Guest, type 1 = Waiter
        self.location = location


class Guest(Agent):
    def __init__(self, id, location, groupId):
        self.id = id
        self.size = 30
        self.location = location
        self.groupId = groupId
        self.current_status = "Idle"
        self.neediness_level = 0
        self.satisfaction = 0
        self.neediness_log = dict()
    def draw(self,canvas):
        canvas.create_oval(self.location[0]-self.size,self.location[1]-self.size,self.location[0]+self.size,self.location[1]+self.size,fill = "yellow")
        canvas.create_text(self.location[0], self.location[1], text=self.id + ":" + self.current_status)
    def move(self,place):
        #assert(isinstance(place,Location))
        self.current_status = "Idle"
        self.location = place.location
    def read(self,item):
        assert(isinstance(item,Item))
        self.current_status = "Reading"
    def talk(self,person):
        assert(isinstance(person,Agent))
        self.current_status = "Talking"
        person.current_status = "Talking"
        print(person.current_status)



class Waiter(Agent):
    def __init__(self, id, location):
        self.id = id
        self.size = 30
        self.location = location
        self.assignedTables = []
        self.task_log = []
        self.inventory = []
    def draw(self,canvas):
        canvas.create_oval(self.location[0]-self.size,self.location[1]-self.size,self.location[0]+self.size,self.location[1]+self.size,fill = "green")
        canvas.create_text(self.location[0],self.location[1],text = self.id)
    def move(self,place):
        self.location = place.location
    def give(self,item,person):
        assert(isinstance(item,Item) and isinstance(person,Agent))
        item.location = person.location

def newGuest(data,id,pos,groupId):
    guest = Guest(id,pos,groupId)
    data.guests += [guest]
def newWaiter(data,id,pos):
    waiter = Waiter(id, pos)
    data.guests += [waiter]