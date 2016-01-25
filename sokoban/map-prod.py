import sys
myfile = open(sys.argv[1])
data = myfile.read().split()
myfile.close()

def retSym(i):
    if i == "-": return "0"
    if i == "*": return "3"
    if i == "b": return "2"

def hex2(n):
    return hex(n)[2:].upper()

def printChanges(string, oldString):
    changed = False
    for c, i in enumerate(string):
        if i != oldString[c]:
            print "LD V" + hex2(c) + " " + retSym(i)
            changed = True
    if changed:
        print "LD [I] V" + hex2(len(string)-1)

for c, i in enumerate(data):
    data[c] = i + "-" * (20 - len(i))

data = "".join(i for i in data)

for c,i in enumerate(data):
    print i,
    if (c+1)%14==0: print ""
sys.exit()

print "LD VE E"
print "LD I mLevel"
line = data[:14]
printChanges(line, "-" * 20)

newI = 14
while 1:
    newLine = data[newI : newI + 14]
    print "ADD I VE"
    printChanges(newLine, line)
    if len(newLine) == 14:
        newI += 14
        line = newLine
    else:
        break

    
