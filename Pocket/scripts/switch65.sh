#!/usr/bin/env bash
echo 65 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio65/direction
cat /sys/class/gpio/gpio65/value
echo 65 >/sys/class/gpio/unexport
