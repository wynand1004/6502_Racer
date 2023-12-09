; Default AI Racer
; The Default AI Racer has the following hardware and properties
; 8 Distance Sensors
; 8 Color and Team sensors
; 8 Track sensors

; Define memory locations for hardware IO
; 0 - 255
; Multiplied by 1.42 to get 3-260 heading
; 0 = 0
; 90 = 
; 180 =
; 270 = 
heading = $00

; Speed
; -127 to 127
; 127 $7F = 0 Speed
; 126 = -1
; 128 = +1
speed = $01
max_speed = $02 ; Read only

; Acceleration
acceleration = $03 ; Read only

; Color
; Can be thought of as a unique id
color = $03 ; Read only

; Distance sensors
; 0 - 255
; 255 means nothing detected
sensor_distance_n = $10
sensor_distance_ne = $11
sensor_distance_e = $12
sensor_distance_se = $13
sensor_distance_s = $14
sensor_distance_sw = $15
sensor_distance_w = $16
sensor_distance_nw = $17

; Team sensors
; 0 - 255
; Team is true/false $10000000 
; Color is the rest of the byte
; Color can be treated as an id
sensor_team_n = $20
sensor_team_ne = $21
sensor_team_e = $22
sensor_team_se = $23
sensor_team_s = $24
sensor_team_sw = $25
sensor_team_w = $26
sensor_team_nw = $27

; Track sensors
; 0 - 255
; 0 means no track boundary detected
sensor_track_n = $30
sensor_track_ne = $31
sensor_track_e = $32
sensor_track_se = $33
sensor_track_s = $34
sensor_track_sw = $35
sensor_track_w = $36
sensor_track_nw = $37

