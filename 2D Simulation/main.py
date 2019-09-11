from tkinter import *
from Location import *
from Agent import *
from tokenizer import *
import vrep
import time
import math
import random
import csv

def init(data):
    #Initializing all state variables and adding all relevant agents into the scene
    data.timestep = 0
    data.objects = []
    data.tables =[]
    data.guests = []
    data.bills = set()
    data.waiters = []
    newTable(data,"table_1",(data.width//2,data.height//2))
    newWaiterArea(data,"waiter_area",(data.width//2-150,data.height//2),100,100)
    newChair(data,"seat_1",(data.width//2,data.height//2-85),(0, 0, math.pi))
    newChair(data,"seat_2",(data.width//2,data.height//2+85),(0, 0, 0))
    newPodium(data,"podium",(150,data.height-200//2),300,200)
    newGuest(data,"C_1","group_1",(50,data.height - 100))
    newGuest(data,"C_2","group_1",(150,data.height - 100))
    newWaiter(data,"W_1",(600,data.height - 100))
    data.instructions = tokenize("data.txt")
    data.output = []
    data.output += [["timestep","objects","agents"]]
    time.sleep(1)



def mousePressed(event, data):
    pass


def keyPressed(event, data):
    #Move through the timesteps faster by pressing right key
    if(event.keysym == "Right"):
        data.timestep += 1
        for instruction in data.instructions:
            if instruction[0] == str(data.timestep):

                instructionHandler(data,instruction)

def instructionHandler(data,instruction):
    #Switch case to parse through different possible instructions
    for person in data.guests:
        if person.id == instruction[2]:
            entity = person
    if instruction[1] == "go":
        for area in data.objects:
            if instruction[3] == area.id: entity.move(area)
    elif instruction[1] == "talk":
        for person in data.guests:
            if person.id == instruction[3]: entity.talk(person)
    elif instruction[1] == "sit":
        for chair in data.objects:
            if instruction[3] == chair.id: entity.seat(data,chair)
    elif instruction[1] == "look":
        for object in data.guests + data.objects:
            if instruction[3] == object.id: entity.lookAnimate(object)


def timerFired(data):
    #Increments timesteps per second accodring to timerDelay
    people = dict()
    for guest in data.guests:
        people[guest.id] = guest.getJointValues()
    objects = dict()
    for object in data.objects:
        objects[object.id] = object.location
    data.output += [[data.timestep,objects,people]]
    data.timestep += 1
    for instruction in data.instructions:
        if instruction[0] == str(data.timestep):
            instructionHandler(data, instruction)


def redrawAll(canvas, data):
    #Drawing all variables
    for table in data.tables:
        table.draw(canvas)
    for object in data.objects:
        if object not in data.tables:
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
    with open('person2.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data.output)
    csvFile.close()
    print("bye!")

#Program still runs through GUI even if not connected to VREP

clientID = vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    run(800, 800)
    time.sleep(2)
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)

else:
    print ('Failed connecting to remote API server')
    run(800, 800)
print ('Program ended')


