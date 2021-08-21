# dubc4-gcode-stirrer

Forked from the original version...

My version uses straight line segments instead of G2/G3 arc commands since my printer won't accept them.
I have also included the inputs to allow the user to enter the OctoPrint Enclosure plugin ID so the UV curing lights code will be automatically
input into the gcode output.

python project to generate gcode for stirring from reddit discussion https://www.reddit.com/r/3Dprinting/comments/oxlzgl/looking_for_someone_to_make_a_program_script_that/.

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
