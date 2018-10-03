import sys, copy
from typing import Union, Tuple, List
myFile = open(sys.argv[1] + ".c8")
data = myFile.read().split("\n")
myFile.close()

keywords = {}
lines: List[str] = []
currLine = 0x200

#apply macros
data2 = copy.deepcopy(data)
for _i in data2:
    if len(_i) == 0: continue
    if _i[0] == "#":
        line = _i[1:].split()
        data.pop(0)
        for c, j in enumerate(data):
            data[c] = j.replace(line[0], line[1])

#expand multiple operations in a line
data2 = []
for _i in data:
    #expand multiple single-line assigments
    if "," in i:
        _i = _i.replace(",", "")
        _left, _right = _i.split("=")
        left = _left.split()
        right = _right.split()
        for c in range(len(left)):
            data2.append(" ".join([left[c], "=", right[c]]))
        continue

    #expand multiple operations to a single-var assignment
    line = _i.split()
    if len(line) >= 5 and line[1] == "=":
        if line[3] in ["+", "|", "&", "^", "-"]:
            data2.append(" ".join([line[0], "=", line[2]]))
            data2.append(" ".join([line[0], line[3]+"=", line[4]]))
        if line[3] in ["<<", ">>"]:
            data2.append(" ".join([line[0], "=", line[2]]))
            data2.append(" ".join([line[0], line[3], line[4]]))
        if line[3] == "*":
            data2.append(" ".join([line[0], "=", line[2]]))
            for cnt in range(int(line[4])-1):
                data2.append(" ".join([line[0], "+=", line[2]]))
        if len(line) > 5:
            for _j in range(5, len(line), 2):
                data2.append(" ".join([line[0], line[_j] + "=", line[_j + 1]]))
    else:
        data2.append(_i)
data = data2

for _i in data:
    i: str = _i.replace("\t", "")

    if len(i) == 0: continue

    while i[0] == " ": i = i[1:]
    
    if i == "" or i[0] == ":":
        continue

    if i[-1] == ":":
        keywords[i[:-1]] = currLine
        continue
    
    line = i.split()

    if "=" in line:
        if line[2] == "delay":
            i = "LD " + line[0] + " DT"
        elif line[2] == "key":
            i = "LD " + line[0] + " K"
        elif line[0] == "delay":
            i = "LD DT " + line[2]
        elif line[0] == "sound":
            i = "LD ST " + line[2]
        elif len(line) > 3:
            if line[3] == "font":
                i = "LD F " + line[2]
            elif line[3] == "BCD":
                i = "LD B " + line[2]
        else:
            i = "LD " + line[0] + " " + line[2]

    if "==" in line:
        i = "SNE " + line[1] + " " + line[3]

    if "!=" in line:
        i = "SE " + line[1] + " " + line[3]

    if "+=" in line:
        i = "ADD " + line[0] + " " + line[2]

    if "|=" in line:
        i = "OR " + line[0] + " " + line[2]

    if "&=" in line:
        i = "AND " + line[0] + " " + line[2]

    if "^=" in line:
        i = "XOR " + line[0] + " " + line[2]

    if "-=" in line:
        i = "SUB " + line[0] + " " + line[2]

    if "=-" in line:
        i = "SUBN " + line[0] + " " + line[2]

    if "<<" in line:
        cnt = int(line[2])
        i = (("SHL " + line[0] + "\n") * cnt)[:-1]
        currLine += 2 * (cnt - 1)

    if ">>" in line:
        cnt = int(line[2])
        i = (("SHR " + line[0] + "\n") * cnt)[:-1]
        currLine += 2 * (cnt - 1)
    
    if line[0] in ("JP", "CALL", "SYS"):
        if line[1][0] == "V":
            i = (line[0] + " " + line[1]) + ':' + (line[2][2:])
        else:
            i = (line[0]) + ':' + (line[1][2:])

    if "not" in line and "pressed" in line:
        i = "SKP " + line[1]
    elif "pressed" in line:
        i = "SKNP " + line[1]

    if "~=" in line:
        i = "RND " + line[0] + " " + line[2]

    if "return" in line:
        i = "RET"

    lines.append(i)
    currLine += 2

for c, ii in enumerate(lines):
    if ':' in ii:
        l, r = ii.split(':')
        lines[c] = l + " " + hex(keywords[r])[2:]

newFile = open(sys.argv[1] + ".c8c", "w")
newFile.write("\n".join(lines))
newFile.close()

import assembler
assembler.assemble("\n".join(lines), sys.argv[2])
