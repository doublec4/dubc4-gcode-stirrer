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
#travelSpeed: speed of travel moves (mm/sec)

class StirGCodeGenerator:
    def __init__(self, xMax, yMax, zMax, zFinal, stirDiameter, stirSpeed, stirTime, stirHeight, travelSpeed=2400):
        self.center = [round(float(xMax) / 2, 2), round(float(yMax) / 2, 2), round(float(zMax) / 2, 2)]
        self.zFinal = round(float(zFinal))
        self.stirRadius = round(float(stirDiameter) / 2, 2)
        self.loops = round(float(stirTime) * 60 / (math.pi * float(stirDiameter) / float(stirSpeed)), 0)
        self.stirSpeed = round(float(stirSpeed) * 60, 2)
        self.stirHeight = round(float(stirHeight), 2)
        self.travelSpeed = round(float(travelSpeed))

    def generate(self, filename):
        xOffset = self.center[0] - self.stirRadius
        yOffset = self.center[1]
        gcode = (
            ("; *** G-code Prefix ***"
             "; Set unit system ([mm] mode)",
             "G21"),
            (";Align coordinates to stirrer",
             "G28 ; Home Position"
             "G90 ; Absolute Positioning"),
            (";Position stirrer",
             f"G1 X{xOffset} Y{yOffset} F{self.travelSpeed}",
             f"G1 Z{self.stirHeight} F{self.travelSpeed}"),
            (";Start Loop",
             f"M808 L{self.loops}"),
            (";Stirring",
             f"G2 X{xOffset} Y{yOffset} I{self.stirRadius} J0 F{self.stirSpeed}"),
            (";End Loop",
             "M808"),
            (";Raise stirrer",
             f"G1 Z{self.zFinal} F{self.travelSpeed}")
        )
        
        #file writing
        with open(filename, "w") as output:
            for section in gcode:
                output.write('\n'.join(section))
                output.write('\n'*2) # delimit sections with a blank line in between

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

g = StirGCodeGenerator(xMax, yMax, zMax, zFinal, stirDiameter, stirSpeed, stirTime, stirHeight)
g.generate(fileName)
