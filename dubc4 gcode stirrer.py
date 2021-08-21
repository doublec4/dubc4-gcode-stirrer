# Program to generate simple g-code per /u/dubc4 request in the /r/3dprinting subreddit
import math


class StirGCodeGenerator:
    def __init__(self, printerDims, zFinal, stirDiameter, stirSpeed, stirTime, stirHeight,
                 cureTime, UVid, compatibility=False):
        """ Creates a GCode generator for stirring a set amount of time.
        
        'printerDims' is a tuple of printer dimensions (length (x), width (y), height (z)) [mm]
        'zFinal' stirrer height at the end of stirring [mm], must be less than printer height
        'stirDiameter' diameter of the circle to trace while stirring [mm],
            Must be less than printer length and width.
        'stirSpeed' speed at which to stir [mm/sec]
        'stirTime' duration of stirring [mins], with straight line segments the calculated time must be increased 10%  therefore multiply time by 1.1
        'cureTime' amount of time to cure parts [mins]
        'UVid' the ID number generated for the GPIO output the UV lights are connected to using Octoprint Enclosure plugin
        'compatibility' boolean for whether to support old firmwares (if True disallows M808 repeat)
            Defaults to False (M808 allowed).
        
        """
        xMax, yMax, zMax = printerDims
        self.center = [round(float(xMax) / 2, 2), round(float(yMax) / 2, 2), round(float(zMax) / 2, 2)]
        self.zFinal = round(float(zFinal))
        self.stirRadius = round(float(stirDiameter) / 2, 2)
        self.stirTime = float(stirTime)
        self.loops = round((self.stirTime * 60)*1.1 / (math.pi * float(stirDiameter) / float(stirSpeed)))
        self.stirSpeed = round(float(stirSpeed) * 60, 2)
        self.stirHeight = round(float(stirHeight), 2)
        self.cureTime = int(cureTime)
        self.UVid = UVid
        self.compatibility = compatibility

    def generate(self, filename, endCode=None):
        """ Generates gcode and writes to 'filename'.
        
        Existing files will be overwritten.
        
        'endCode' is a gcode file that gets appended to the end of the generated one.
        
        """
        xOffset = self.center[0] - self.stirRadius
        yOffset = self.center[1]
        gcode = (
            *self.generate_setup(xOffset, yOffset),
            *self.generate_stirring(xOffset, yOffset),
            *self.generate_cleanup()
        )

        # file writing
        with open(filename, "w") as output:
            for section in gcode:
                output.write('\n'.join(section))
                output.write('\n' * 2)  # delimit sections with a blank line in between

            if not endCode:
                return  # finish now if no endcode to add

            with open(endCode) as addendum:
                for line in addendum:
                    output.write(line)

    def generate_setup(self, xOffset, yOffset):
        return (
            ("; *** G-code Prefix ***",
             "; Set unit system ([mm] mode)",
             "G21"),
            (";Align coordinates to stirrer",
             "G90 ; Absolute Positioning"),
            (";Position stirrer",
             f"G0 X{xOffset} Y{yOffset} F{self.stirSpeed}",
             f"G0 Z{self.stirHeight} F500")
        )

    def generate_stirring(self, xOffset, yOffset):
        heading = f";Stirring {self.loops} times (~{self.stirTime} mins)"
        if self.compatibility:
            return (
                (heading,
                 *(f"""G0 X{self.center[0]} Y{self.center[1] + self.stirRadius} F{self.stirSpeed}
G0 X{self.center[0] + self.stirRadius} Y{self.center[1]} F{self.stirSpeed}
G0 X{self.center[0]} Y{self.center[1] - self.stirRadius} F{self.stirSpeed}
G0 X{self.center[0] - self.stirRadius} Y{self.center[1]} F{self.stirSpeed}"""for _ in range(self.loops))),
            )

        return (
            (";Start Loop",
             f"M808 L{self.loops}"),
            (heading,
             f"G0 X{self.center[0]} Y{self.center[1] + self.stirRadius} F{self.stirSpeed}",
             f"G0 X{self.center[0] + self.stirRadius} Y{self.center[1]} F{self.stirSpeed}",
             f"G0 X{self.center[0]} Y{self.center[1] - self.stirRadius} F{self.stirSpeed}",
             f"G0 X{self.center[0] - self.stirRadius} Y{self.center[1]} F{self.stirSpeed}"),
            (";End Loop",
             "M808")
        )

    def generate_cleanup(self):
        return (
            (";Raise stirrer",
             f"G0 X{self.center[0]} Y{self.center[1]} F{self.stirSpeed}",
             f"G0 Z{self.zFinal} F500",
             f"G4 S1",
             f"ENC O{self.UVid} S1",
             f"G4 S{self.cureTime * 60}",
             f"ENC O{self.UVid} S0",
             f"M300 S500 P400"),
        )


# Example run:
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

xMax = input("Printer x length (mm): ")
yMax = input("Printer y length (mm): ")
zMax = input("Printer z length (mm): ")
stirDiameter = input("Stirring diameter (mm): ")
stirSpeed = input("Stirring speed (mm/sec): ")
stirTime = input("Stirring duration (min): ")
stirHeight = input("Stirring z position (mm): ")
zFinal = input("Curing z position (mm): ")
cureTime = input("Amount of time to cure parts (min): ")
UVid = input("OctoPrint Enclosure PlugIn output ID for UV Lights: ")
disable_M808 = input("Disable M808? Older versions of Marlin will not support it [y/n]?: ").lower() == 'y'
fileName = input("Enter filename (be sure to end with .gcode): ")
endCode = input("Enter custom end code filename (must be in same directory, leave blank to skip): ").strip()

g = StirGCodeGenerator((xMax, yMax, zMax), zFinal, stirDiameter, stirSpeed, stirTime, stirHeight,
                       cureTime, UVid, disable_M808)
g.generate(fileName, endCode)
