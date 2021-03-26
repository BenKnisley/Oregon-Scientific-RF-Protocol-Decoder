#!/bin/bash
## Author: Ben Knisley [benknisley@gmail.com]
## Date: 6 Jan, 2019

## Start reciving, convert audio signal, and port to processing
rtl_fm -g 36.0  -f 433.85300M -M am -s 48k -E deemp - | sox -r 48000 -t raw -b 16 -c 1 -e signed-integer /dev/stdin -r 48000 -t wav -b 16 -c 1 -e signed-integer - | ./exe4.py
