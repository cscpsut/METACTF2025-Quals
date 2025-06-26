#!/bin/bash

# Write flag to file
echo $FLAG > flag.txt

# Set proper terminal settings
stty sane 2>/dev/null || true

# Start socat with pseudo-terminal support for ASCII art and animations
socat TCP-LISTEN:7444,reuseaddr,fork EXEC:"/app/pilot",pty,stderr,setsid,sigint,sane
