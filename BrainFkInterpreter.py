import sys

if(len(sys.argv) == 1):
    print("Run error: No source file")
    sys.exit()

inputFile = sys.argv[1]

with open(inputFile, "r") as f:
    src = "".join([line.strip() for line in f])

MEMORY_LEN = 1000
memory = [0 for x in range(0, MEMORY_LEN)]
masterPtr = 0
langChars = ['+', '-', '<', '>', '.', '?', ',', '[', ']']

class inputStream:
    def __init__(self):
        self.buffer = ""

    def nextChar(self):
        if(self.buffer == ""):
            self.buffer = input()
            if(self.buffer == ""):
                return '\0'
        nextChar = self.buffer[0]
        self.buffer = self.buffer[1:]
        return nextChar

iStream = inputStream()

def parse(src):
    global memory, masterPtr, MEMORY_LEN, iStream
    i = 0
    while i < len(src):
        if src[i] not in langChars:
            i += 1
            continue
        try:
            if(src[i] == '+'):
                memory[masterPtr] += 1
            elif(src[i] == '-'):
                memory[masterPtr] -= 1
            elif(src[i] == '<'):
                if(masterPtr == 0):
                    raise ValueError("You tried to go too far back my friend")
                masterPtr -= 1
            elif(src[i] == '>'):
                if(masterPtr == MEMORY_LEN-1):
                    raise ValueError("That's as far as it goes")
                masterPtr += 1
            elif(src[i] == '.'):
                print(chr(memory[masterPtr]), end='')
            elif(src[i] == '?'):
                print(memory[masterPtr], end='')
            elif(src[i] == ','):
                memory[masterPtr] = ord(iStream.nextChar())
            elif(src[i] == '['):
                i += 1
                loopBody = ""
                childLoops = 0
                while(src[i] != ']' or childLoops != 0):
                    if(src[i] == '['):
                        childLoops += 1
                    if(src[i] == ']'):
                        childLoops -= 1
                    loopBody += src[i]
                    i += 1
                while(memory[masterPtr]):
                    if not parse(loopBody):
                        return False
        except ValueError as ve:
            print("Value Error: " + str(ve))
            return False
        i += 1
    return True

parse(src)
