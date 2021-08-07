; *** G-code Prefix ***
; Set unit system ([mm] mode)
G21

;Align coordinates to stirrer
G28 ; Home Position
G90 ; Absolute Positioning

;Position stirrer
G0 X85.0 Y100.0 F2400
G0 Z20.0 F2400

;Start Loop
M808 L32

;Stirring 32 times (~5.0 mins)
G2 X85.0 Y100.0 I15.0 J0 F600.0

;End Loop
M808

;Raise stirrer
G0 Z50 F2400

