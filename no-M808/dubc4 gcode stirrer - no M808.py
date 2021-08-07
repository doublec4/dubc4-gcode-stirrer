#Program to generate simple g-code per /u/dubc4 request in the /r/3dprinting subreddit
import math

#xMax: printer length (mm)
#yMax: printer width (mm)
#zMax: printer height (mm)
#zFinal: stirrer height at end of stirring (mm), must be less than zMax
#stirDiameter: diameter of the circle the stirrer will trace while stirring (mm), must be less than xMax and yMax
#stirSpeed: speed at which to stir (mm/sec)
#stirTime: duration of stirring (min)
#filename: file that will contain the generated g-code, existing files will be overwritten

class StirGCodeGenerator:
    def __init__(self, xMax, yMax, zMax, zFinal, stirDiameter, stirSpeed, stirTime, stirHeight, filename):
        self.center = [round(float(xMax) / 2, 2), round(float(yMax) / 2, 2), round(float(zMax) / 2, 2)]
        self.zFinal = round(float(zFinal))
        self.stirRadius = round(float(stirDiameter) / 2, 2)
        self.loops = round(float(stirTime) * 60 / (math.pi * float(stirDiameter) / float(stirSpeed)), 0)
        self.stirSpeed = round(float(stirSpeed) * 60, 2)
        self.stirHeight = round(float(stirHeight), 2)
        self.filename = filename

    def generate(self):
        print("loops: " + str(self.loops))
        #file writing
        f = open(self.filename, "w")

        #set unit system
        f.write("; *** G-code Prefix ***\n; [mm] mode\n")
        f.write("G21\n\n")

        #align the coordinates (home, set absolute positioning)
        f.write(";Align coordinates to stirrer\n")
        f.write("G28 ; Home Position\n")
        f.write("G90 ; Absolute Positioning\n\n")

        #Positions the stirrer
        f.write(";Position stirrer\n")
        f.write("G1 X" + str(self.center[0] - self.stirRadius) + " Y" + str(self.center[1]) + " F2400\n")
        f.write("G1 Z" + str(self.stirHeight) + " F2400\n\n")

        #Stirring
        f.write(";Stirring\n")
        for _ in range(self.loops):
            f.write("G2 X" + str(self.center[0] - self.stirRadius) + " Y" + str(self.center[1]) + " I" + str(self.stirRadius) + " J0 F" + str(self.stirSpeed) + "\n")

        #Raise stirrer
        f.write("\n;Raise stirrer\n")
        f.write("G1 Z" + str(self.zFinal) + " F2400\n\n")

        #end file writing
        f.close()

#Example run:
"""
xMax = 200
yMax = 200
zMax = 200
zFinal = 50
stirHeight = 20
stirDiameter = 30
stirSpeed = 10
stirTime = 5
fileName = "test.gcode"
"""
print("Please enter the following inputs.")

xMax         = input("Printer x length (mm): ")
yMax         = input("Printer y length (mm): ")
zMax         = input("Printer z length (mm): ")
stirDiameter = input("Stirring diameter (mm): ")
stirSpeed    = input("Stirring speed (mm/sec): ")
stirTime     = input("Stirring duration (min): ")
stirHeight   = input("Stirrer height (mm): ")
zFinal       = input("Final stirrer height (mm): ")
fileName     = input("Enter filename: ")

g = StirGCodeGenerator(xMax, yMax, zMax, zFinal, stirDiameter, stirSpeed, stirTime, stirHeight, fileName)
g.generate()
