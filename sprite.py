import sys

myFile = open(sys.argv[1])
data = myFile.read().split("\n")

for i in data:
    string = ""
    for j in i:
        if j == " ": string += "0"
        elif j == "*": string += "1"
    string += "0"*(8-len(string))
    print hex(int(string, 2))[2::]

myFile.close()
