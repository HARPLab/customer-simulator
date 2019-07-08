from tkinter import *
from Location import *
from Agent import *
from tokenizer import *

def init(data):
    data.timestep = 0
    data.objects = []
    data.tables =[]
    data.guests = []
    data.waiters = []
    newTable(data,(data.width//2,data.height//2),150)
    newWaiterArea(data,"waiter_area",(data.width//2-150,data.height//2),100,100)
    newChair(data,"seat_1",(data.width//2,data.height//2-130),75)
    newChair(data,"seat_2",(data.width//2,data.height//2+130),75)
    newPodium(data,(200,data.height-200//2),400,200)
    newGuest(data,"C_1",(100,data.height - 100),"group_1")
    newGuest(data,"C_2",(300,data.height - 100),"group_1")
    newWaiter(data,"W_1",(200,data.height - 100))
    data.instructions = tokenize("data.txt")
    print(data.instructions)



def mousePressed(event, data):
    pass


def keyPressed(event, data):
    if(event.keysym == "Right"):
        data.timestep += 1
        for instruction in data.instructions:
            if instruction[0] == str(data.timestep):

                instructionHandler(data,instruction)

def instructionHandler(data,instruction):
    print(instruction)
    for person in data.guests:
        if person.id == instruction[2]:
            entity = person
    if instruction[1] == "go":
        for area in data.objects:
            if instruction[3] == area.id:
                place = area
        entity.move(place)
    elif instruction[1] == "talk":
        for person in data.guests:
            if person.id == instruction[3]:
                entity2 = person
        entity.talk(entity2)
def timerFired(data):
    pass


def redrawAll(canvas, data):
    for table in data.tables:
        table.draw(canvas)
    for object in data.objects:
        if object not in data.tables:
            #print(object.id)
            object.draw(canvas)
    for guest in data.guests:
        guest.draw(canvas)
    for waiter in data.waiters:
        waiter.draw(canvas)
    canvas.create_text(data.width-130,50,text = "Timestep " + str(data.timestep),font = "Arial 20")


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()
    print("bye!")


run(1000, 1000)
