# Chall_name 
Grounded

## Description: 
This is Rana from the HR department at AeroNimbus Airlines. A while ago, I received an email from someone I don’t remember. I think it had something to do with scheduling. I didn’t think much of it at the time.

But now IT says there may have been a breach, and they’re asking questions about my device. I’ve handed it over to the forensics team for investigation. I really hope I didn’t mess anything up. I’m honestly just worried I’ll get fired if this ends up being my fault.

The investigation team needs your help.

## Author: 
KAIOKEN

## Brief: 
This challenge is a memory dump of an HR employee's device in which the employee got phished through a spoofed email address that sent her an excel sheet that had macros enabled. The macros perform some sort of persistence in the run key which runs a dropper and exfiltrates a sensitive file that is renamed to avoid suspicion. The players must analyze all these events through the memory dump as well as find the attacker's name.

## Flag: 
METACTF{M4CR0S_AR3_D4NG3R0US_D0NT_G3T_PH1SH3D_[dynamic part]}
