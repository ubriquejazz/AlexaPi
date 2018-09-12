#!/usr/bin/env bash
echo 64 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio64/direction
# parameter = 0 or 1
echo $1 >/sys/class/gpio/gpio64/value
echo 64 >/sys/class/gpio/unexport