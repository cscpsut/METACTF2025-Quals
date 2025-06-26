#!/bin/bash

echo $FLAG > flag.txt
socat TCP-LISTEN:7444,reuseaddr,fork EXEC:/app/hijack
