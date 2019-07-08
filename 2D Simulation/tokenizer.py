def readFile(path):
    with open(path, "rt") as f:
        return f.read()
actionsWithTo = ["go","talk"]
def tokenize(path):
    data = readFile("data.txt")
    instruction = []
    for line in data.splitlines():
        token = line.split()
        timestep = token[-1]
        token.pop()
        token.pop()
        entity = token[0]
        token.pop(0)
        if token[0] in actionsWithTo:
            action = token[0]
            token = token[2:]
        else:
            action = token[0]
            token = token[1:]
        if len(token) == 1:
            extraInfo = token[0]
            instruction += [(timestep,action,entity,extraInfo)]
        elif len(token) == 3:
            extraInfo = token[0]
            extraInfo1 = token[-1]
            instruction += [(timestep,action,entity,extraInfo,extraInfo1)]
    return instruction
