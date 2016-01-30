import sys, clipboard
myfile = open(sys.argv[1])
data = myfile.read().split()
myfile.close()

GRID_WIDTH = 20
GRID_HEIGHT = 10

def hex2(n):
    return hex(n)[2:].upper()

def solidSym(n):
    if n == "b": return "2"
    elif n == "*": return "3"
    else: return "0"

def goalSym(n):
    if n == "g": return "1"
    else: return "0"

def printGrid(n):
    global binString, oldReg, newReg

    for i in range(0, len(newGrid), 14):
        if i != 0: binString += "\tI += VE\n"
        newReg = [n(i) for i in newGrid[i: i + 14]]
        if newReg == defReg: continue
        left, right = [], []

        for j in range(len(newReg)):
            if oldReg[j] != newReg[j]:
                left.append("V" + hex2(j))
                right.append(newReg[j])

        if len(newReg) != 14:
            left.append("V" + hex2(len(newReg)))
            right.append("4")
            newReg.append("4")

        binString += "\t" + ", ".join(left) + " = " + ", ".join(right) + "\n"

        if len(newReg) != 14:
            binString += "\t[I] = " + left[-1] + "\n\n"
            newReg.extend(oldReg[len(newReg):])
        else:
            binString += "\t[I] = VD\n\n"

        oldReg = newReg[:]

xLen, yLen = 0, 0
for i in data:
    if i != "": yLen += 1
    xLen = max(xLen, len(i))

xOffset = int((GRID_WIDTH - xLen) / 2)
yOffset = int((GRID_HEIGHT - yLen) / 2)

# change grid
newGrid = "-" * GRID_WIDTH * yOffset
for i in data:
    nextLine = "-" * xOffset + i
    nextLine += "-" * (GRID_WIDTH - len(nextLine))
    newGrid += nextLine

defReg = ["0" for i in range(14)]
oldReg = ["0" for i in range(14)]

# store solid grid
binString = ":load solid map\n\tVE = E\n\tI = mLevel\n\n"
printGrid(solidSym)

# store goal grid
binString += ":load goal map\n\tI = mGoal\n\n"
printGrid(goalSym)

# store you
x, y = 0, 0
found = False

for i in range(0, len(newGrid), 20):
    for j in range(20):
        if newGrid[i + j] == "y":
            y, x = hex2(i / 20), hex2(j)
            found = True
            break
    if found: break

binString += ":load you\n\tI = mYou\n\tV0, V1 = " + x + ", " + y + "\n\t[I] = V1"
clipboard.copy(binString)
