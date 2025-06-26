# Phantom Login 

## Description: 
Captain Osama, a pilot at Airnovex, received an email from the internal security team asking him to register on a "new secure portal". The email looked perfectly legitimate and even led him to what appeared to be the real Microsoft login page. Without suspecting anything, Captain Osama entered his credentials.

However, the Security Operations Center (SOC) was immediately alerted due to suspicious outbound network activity from Osama’s machine to a non-corporate IP address. Upon investigation, the team preserved two key artifacts:

- A disk image of Captain Osama’s machine
- A packet capture (PCAP) file of the suspicious network session

Your mission is to uncover how the attacker executed the phishing attack and extract key information from the evidence.

## Author: 
Yazam

## Brief: 
Disk forensics & Network forensics for a phishing case.

## Flag: 
METACTF{TLS_Mirror_Reveals_Proxy_Predator_[DYNAMIC_PART]}
