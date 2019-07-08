class Item(object):
    def __init__(self,id,location,servings_left,servings_max):
        self.id = id
        self.location = location
        self.servings_left = servings_left
        self.servings_max = servings_max

class CommunalItem(Item):
    def __init__(self,id,status,servings_left,servings_max):
        super().__init__(self,id,status,servings_left,servings_max)
        self.in_use = False

class IndividualItem(Item):
    def __init__(self,id,status,servings_left,servings_max):
        super().__init__(self, id, status, servings_left, servings_max)
        self.groupId = None
        self.individualId = None

class Menu(IndividualItem):
    def __init__(self,id):
        self.status = False
        super().__init__(self, id, status,0,0)
        self.size = 10
    def draw(self,canvas):
        canvas.create_rectangle(self.location)
    def inUse(self,User):
        assert(type(User) == Agent)
        self.individualId = User.id

