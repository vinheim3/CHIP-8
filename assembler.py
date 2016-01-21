import sys
myFile = open(sys.argv[1])
data = myFile.read().split("\n")

fileBytes = []

def ANNN(a,n): return ((int(a,16)<<12)|(int(n,16)))
def AXYN(a,x,y,n): return ((int(a,16)<<12)|(int(x,16)<<8)|(int(y,16)<<4)|(int(n,16)))
def AXKK(a,x,kk): return ((int(a,16)<<12)|(int(x,16)<<8)|(int(kk,16)))

keywords = {}
spriteWords = {}
currLN = 0x200

for c,line in enumerate(data):
    if line == "" or line[0] == ":": continue
    if line[0] == "'":
        a = line.split()
        spriteWords[a[0][1:]] = a[1]
        continue
    
    lineData = line.split()
    i = lineData[0]
    lD = lineData[1:]
    byte = 0

    if len(lD)!= 0 and lD[-1][0] == "*":
        keywords[lD[-1][1:]] = currLN
    
    if i == "CLS":                                  #00E0 CLS
        byte = 0x00E0
    elif i == "RET":                                #00EE RET
        byte = 0x00EE
    elif i == "SYS":                                #0NNN SYS nnn->keyword
        part1 = '0'
        part2 = lD[0][2:]
    elif i == "JP":
        if lD[0][0] != "V":                         #1NNN JP nnn->keyword
            part1 = '1'
            part2 = lD[0][2:]
        else:                                       #BNNN JP V0 nnn->keyword
            part1 = 'B'
            part2 = lD[1][2:]
    elif i == "CALL":                               #2NNN CALL nnn->keyword
        part1 = '2'
        part2 = lD[0][2:]
    elif i == "SE":
        if lD[1][0] == 'V':                         #5XY0 SE VX VY
            byte = AXYN('5',lD[0][1],lD[1][1],'0')
        else:                                       #3XKK SE VX byte
            byte = AXKK('3',lD[0][1],lD[1])
    elif i == "SNE":
        if lD[1][0] == 'V':                         #9XY0 SNE VX VY
            byte = AXYN('9',lD[0][1],lD[1][1],'0')
        else:                                       #4XKK SNE VX byte
            byte = AXKK('4',lD[0][1],lD[1])
    elif i == "LD":
        if lD[0] == "I":                            #ANNN LD I nnn
            byte = ANNN('A',spriteWords[lD[1]])
        elif lD[0] == "DT":                         #FX15 LD DT VX
            byte = AXKK('F',lD[1][1],'15')
        elif lD[0] == "ST":                         #FX18 LD ST VX
            byte = AXKK('F',lD[1][1],'18')
        elif lD[0] == "F":                          #FX29 LD F VX
            byte = AXKK('F',lD[1][1],'29')
        elif lD[0] == "B":                          #FX33 LD B VX
            byte = AXKK('F',lD[1][1],'33')
        elif lD[0] == "[I]":                        #FX55 LD [I] Vx
            byte = AXKK('F',lD[1][1],'55')
        elif lD[1] == "[I]":                        #FX65 LD Vx [I]
            byte = AXKK('F',lD[0][1],'65')
        elif lD[1][0] == "V":                       #8XY0 LD VX VY
            byte = AXYN('8',lD[0][1],lD[1][1],'0')
        elif lD[1] == "DT":                         #FX07 LD VX DT
            byte = AXKK('F',lD[0][1],'07')
        elif lD[1] == "K":                          #FX0A LD VX K
            byte = AXKK('F',lD[0][1],'0A')
        else:                                       #6XKK LD VX byte
            byte = AXKK('6',lD[0][1],lD[1])
    elif i == "ADD":
        if lD[0] == "I":                            #FX1E ADD I VX
            byte = AXKK('F',lD[1][1],'1E')
        elif lD[1][0] == 'V':                       #8XY4 ADD VX VY
            byte = AXYN('8',lD[0][1],lD[1][1],'4')
        else:                                       #7XKK ADD VX byte
            byte = AXKK('7',lD[0][1],lD[1])
    elif i == "OR":                                 #8XY1 OR VX VY
        byte = AXYN('8',lD[0][1],lD[1][1],'1')
    elif i == "AND":                                #8XY2 AND VX VY
        byte = AXYN('8',lD[0][1],lD[1][1],'2')
    elif i == "XOR":                                #8XY3 XOR VX VY
        byte = AXYN('8',lD[0][1],lD[1][1],'3')
    elif i == "SUB":                                #8XY5 SUB VX VY
        byte = AXYN('8',lD[0][1],lD[1][1],'5')
    elif i == "SHR":                                #8X~6 SHR VX
        byte = AXKK('8',lD[0][1],'06')
    elif i == "SUBN":                               #8XY7 SUBN VX VY
        byte = AXYN('8',lD[0][1],lD[1][1],'7')
    elif i == "SHL":                                #8XYE SHL VX
        byte = AXKK('8',lD[0][1],'0E')
    elif i == "RND":                                #CXKK RND VX byte
        byte = AXKK('C',lD[0][1],lD[1])
    elif i == "DRW":                                #DXYN DRW VX VY N
        byte = AXYN('D',lD[0][1],lD[1][1],lD[2])
    elif i == "SKP":                                #EX9E SKP VX
        byte = AXKK('E',lD[0][1],'9E')
    elif i == "SKNP":                               #EXA1 SKNP VX
        byte = AXKK('E',lD[0][1],'A1')
    else:
        print "Invalid opcode: " + str(c + 1) + "\n"

    currLN += 2

    if byte != 0:
        fileBytes.append(byte>>8)
        fileBytes.append(byte&0xFF)
    else:
        fileBytes.append(int(part1,16))
        fileBytes.append(part2)

for c,i in enumerate(fileBytes):
    if i in keywords:
        fileBytes[c] = keywords[i]
        fileBytes[c-1] = ((fileBytes[c-1]<<4)|(keywords[i]>>8))
        fileBytes[c] &= 0xFF

allBytes = bytearray(fileBytes)
newFile = open(sys.argv[2], "wb")
newFile.write(allBytes)
newFile.close()
myFile.close()
