import sys

myFile = open(sys.argv[1])
data = myFile.read().split("\n")

for i in data:
    string = ""
    for j in i:
        if j == "*": string += "1"
        else: string += "0"
    string += "0"*(8-len(string))
    print hex(int(string, 2))[2::].upper()

myFile.close()
