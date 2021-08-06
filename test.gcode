; *** G-code Prefix ***
; [mm] mode
G21

;Align coordinates to stirrer
G28 ; Home Position
G90 ; Absolute Positioning

;Position stirrer
G1 X85.0 Y100.0 F2400
G1 Z20.0 F2400

;Start Loop
M808 L32.0

;Stirring
G2 X85.0 Y100.0 I15.0 J0 F600.0

;End Loop
M808

;Raise stirrer
G1 Z50 F2400

