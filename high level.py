import sys
myFile = open(sys.argv[1])
data = myFile.read().split("\n")
myFile.close()

keywords = {}
memVars = {}
lines = []
currLine = 0x200

for i in data:
    if i == "" or i[0] == ":":
        continue
    
    line = i.split()
    
    if i[0] == "'":
        memVars[line[0][1:]] = line[1]
        continue

    if line[-1][0] == "*":
        keywords[line[-1][1:]] = currLine
        i = " ".join(line[:-1])
        
    if i[:4] == "LD I":
        lines.append("LD I " + memVars[line[2]])
        currLine += 2
        continue

    if line[0] in ("JP", "CALL", "SYS"):
        if line[1][0] == "V":
            lines.append([line[0] + " " + line[1], line[2][2:]])
        else:
            lines.append([line[0], line[1][2:]])
        currLine += 2
        continue

    lines.append(i)
    currLine += 2

for c, i in enumerate(lines):
    if len(i) == 2:
        lines[c] = lines[c][0] + " " + hex(keywords[lines[c][1]])[2:]

newFile = open(sys.argv[2], "w")
newFile.write("\n".join(lines))
newFile.close()
