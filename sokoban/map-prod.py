import sys
from typing import Tuple, List, Callable

map_file = sys.argv[1]
with open(map_file) as f:
    data = f.read().split()

GRID_WIDTH = 20
GRID_HEIGHT = 10
MAX_REGISTERS = 14

def hex2(n: int) -> str:
    return hex(n)[2:].upper()

def solidSym(n: str) -> str:
    if n == "b": return "2"
    elif n == "*": return "3"
    else: return "0"

def goalSym(n: str) -> str:
    if n == "g": return "1"
    else: return "0"

def printGrid(n: Callable[[str], str], binString: str, oldReg: List[str]) -> Tuple[str, List[str]]:
    for i in range(0, len(newGrid), MAX_REGISTERS):
        if i != 0: binString += "\tI += VE\n"
        newReg = [n(i) for i in newGrid[i: i + MAX_REGISTERS]]
        if newReg == defReg: continue
        left, right = [], []

        for j in range(len(newReg)):
            if oldReg[j] != newReg[j]:
                left.append("V" + hex2(j))
                right.append(newReg[j])

        if len(newReg) != MAX_REGISTERS:
            left.append("V" + hex2(len(newReg)))
            right.append("4")
            newReg.append("4")

        binString += "\t" + ", ".join(left) + " = " + ", ".join(right) + "\n"

        if len(newReg) != MAX_REGISTERS:
            binString += "\t[I] = " + left[-1] + "\n\n"
            newReg.extend(oldReg[len(newReg):])
        else:
            binString += "\t[I] = VD\n\n"

        oldReg = newReg[:]
    return binString, oldReg

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

defReg = ["0" for i in range(MAX_REGISTERS)]
oldReg = ["0" for i in range(MAX_REGISTERS)]

# store solid grid
binString = ":load solid map\n\tVE = E\n\tI = mLevel\n\n"
binString, oldReg = printGrid(solidSym, binString, oldReg)

# store goal grid
binString += ":load goal map\n\tI = mGoal\n\n"
binString, oldReg = printGrid(goalSym, binString, oldReg)

# store you
x, y = "", ""
found = False

for ii in range(0, len(newGrid), 20):
    for jj in range(20):
        if newGrid[ii + jj] == "y":
            y, x = hex2(ii // 20), hex2(jj)
            found = True
            break
    if found: break

binString += ":load you\n\tI = mYou\n\tV0, V1 = {}, {}\n\t[I] = V1".format(x, y)

with open('sokoban.c8.template') as f:
    template = f.read()

new_c8_file = 'sokoban-' + map_file.rpartition('.')[0]
with open(new_c8_file, 'w') as f:
    f.write(template.format(maps_and_you=binString))
