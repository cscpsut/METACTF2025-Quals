# Cersei on autopilot

## Description: 
Autopilot took full control of the plane and gone insane, figure out what Cersei has to do with this and deactivate the autopilot to regain control.

## Author:
YASEEN

## Brief: 
Reverse the apk to find out how it checks for the flag, extrace native-lib, extract crc32 method and the hashed values, brute force the flag. Another solution would be to hook on frida and check when the validat input function returns 1 to count the character true. 

## Flag: 
`METACTF{10_s3conds_it_told_me_10_s3c0nd$_oh_no_it_didn't@!}`