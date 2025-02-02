# dubc4-gcode-stirrer

Forked from the original version...

My version uses straight line segments instead of G2/G3 arc commands since my printer won't accept them.
I have also included the inputs to allow the user to enter the OctoPrint Enclosure plugin ID so the UV curing lights code will be automatically
input into the gcode output.

This python project was written to be used with the Marlin firmware: https://marlinfw.org/. As of writing, the Marlin firmware version is 2.0.9.1 and should work with Marlin firmware version 2.0.8 and up.

Notes on gcode M808:

1) It uses gcode M808 to repeat the stirring. To use command M808, the firmware's Configuration_adv.h file needs to be edited and the firmware re-flashed. To edit the Configuration_adv.h file, go to line 1327 and uncomment "#define GCODE_REPEAT_MARKERS".

2) M808 may only work when printing from an SD card. I have not tested it using any other method.

test.gcode is an example output created with the following inputs:  
- xMax = 200  
- yMax = 200  
- zMax = 200  
- zFinal = 50  
- stirHeight = 20  
- stirDiameter = 30  
- stirSpeed = 10  
- stirTime = 5  
- fileName = "test.gcode"  

DISCLAIMER...

This creates gcode to perform a function on your 3D printer that it was not intended to do. This is for the purpose of experimentation. I am not responsible for any damage to your printer through the use of this script. I would recommend standing by your printer ready to kill the power until you are sure that the script does not cause any unwanted behavior.
