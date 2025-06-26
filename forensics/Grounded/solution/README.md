# writer writeup 
1. The player must run volatility3 and analyze the processes and will notice that EXCEL.exe was open.
2. The player should analyze for the files using filescan, there the player will find a .xlsm file which indicates a suspicious macro being available. Upon investigating it the player will know the answers towards questions 1 and 2.
3. The player can use hivescan to answer question 3.
4. Using filescan, the player can answer the paths required for questions 4, 5, and 6; however must be able to identify which one is for which. The original file is in the Documents, the modified file is in the ProgramData, and the malicious macro is in the Downloads.
5. The malicious executable can be easily identified from the pslist plugin which is onedrivecmd.exe for question 7.
6. The description mentioned something about an email, the player should extract an eml file from filescan using dumpfiles. Once the email has been extracted, the answer for question 8 can be answered. The answer is "Rami Abdulsalam_People Operations".
