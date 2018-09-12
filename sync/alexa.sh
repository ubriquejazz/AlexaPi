#!/bin/bash
# Script to update the code in the Zedboard
# Raspberry Pi running on 192.168.100.1
sshpass -p "raspberry" rsync -avz -e ssh pi@192.168.100.1:/home/pi/AlexaPi/src ./
rm ./AlexaPi/src/alexapi/*.pyc
rm ./AlexaPi/src/alexapi/device_platforms/*.pyc
rm ./AlexaPi/src/alexapi/playback_handlers/*.pyc