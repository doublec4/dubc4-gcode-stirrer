#Program to generate simple g-code per /u/dubc4 request in the /r/3dprinting subreddit
import math

class StirGCodeGenerator:
    def __init__(self, printerDims, zFinal, stirDiameter, stirSpeed, stirTime, stirHeight,
                 travelSpeed=2400, compatibility=False):
        """ Creates a GCode generator for stirring a set amount of time.
        
        'printerDims' is a tuple of printer dimensions (length (x), width (y), height (z)) [mm]
        'zFinal' stirrer height at the end of stirring [mm], must be less than printer height
        'stirDiameter' diameter of the circle to trace while stirring [mm],
            Must be less than printer length and width.
        'stirSpeed' speed at which to stir [mm/sec]
        'stirTime' duration of stirring [mins]
        'travelSpeed' speed of travel moves [mm/sec]
        'compatibility' boolean for whether to support old firmwares (if True disallows M808 repeat)
            Defaults to False (M808 allowed).
        
        """
        xMax, yMax, zMax = printerDims
        self.center = [round(float(xMax) / 2, 2), round(float(yMax) / 2, 2), round(float(zMax) / 2, 2)]
        self.zFinal = round(float(zFinal))
        self.stirRadius = round(float(stirDiameter) / 2, 2)
        self.loops = round(float(stirTime) * 60 / (math.pi * float(stirDiameter) / float(stirSpeed)), 0)
        self.stirSpeed = round(float(stirSpeed) * 60, 2)
        self.stirHeight = round(float(stirHeight), 2)
        self.travelSpeed = round(float(travelSpeed))
        self.compatibility = compatibility

    def generate(self, filename):
        """ Generates gcode and writes to 'filename'.
        
        Existing files will be overwritten.
        
        """
        xOffset = self.center[0] - self.stirRadius
        yOffset = self.center[1]
        gcode = (
            *self.generate_setup(xOffset, yOffset),
            *self.generate_stirring(xOffset, yOffset),
            *self.generate_cleanup()
        )
        
        #file writing
        with open(filename, "w") as output:
            for section in gcode:
                output.write('\n'.join(section))
                output.write('\n'*2) # delimit sections with a blank line in between
                
    def generate_setup(self, xOffset, yOffset):
        return (
            ("; *** G-code Prefix ***",
             "; Set unit system ([mm] mode)",
             "G21"),
            (";Align coordinates to stirrer",
             "G28 ; Home Position",
             "G90 ; Absolute Positioning"),
            (";Position stirrer",
             f"G0 X{xOffset} Y{yOffset} F{self.travelSpeed}",
             f"G0 Z{self.stirHeight} F{self.travelSpeed}")
        )
    
    def generate_stirring(self, xOffset, yOffset):
        if self.compatibility:
            return (
                (";Stirring",
                 *(f"G2 X{xOffset} Y{yOffset} I{self.stirRadius} J0 F{self.stirSpeed}" 
                   for _ in range(self.loops)))
            )
        
        return (
            (";Start Loop",
             f"M808 L{self.loops}"),
            (";Stirring",
             f"G2 X{xOffset} Y{yOffset} I{self.stirRadius} J0 F{self.stirSpeed}"),
            (";End Loop",
             "M808")
        )
    
    def generate_cleanup(self):
        return (
            (";Raise stirrer",
             f"G0 Z{self.zFinal} F{self.travelSpeed}"),
        )

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
travelSpeed  = input("Travel speed (mm/sec - default 2400): ") or 2400
disable_M808 = input("Compatiblity mode (disable M808) [y/N]?: ").lower() == 'y'
fileName     = input("Enter filename: ")

g = StirGCodeGenerator((xMax, yMax, zMax), zFinal, stirDiameter, stirSpeed, stirTime, stirHeight,
                       travelSpeed, disable_M808)
g.generate(fileName)
