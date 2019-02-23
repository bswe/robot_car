#!/bin/bash

# script to continuously display the robot output

cd /home/pi/Desktop

tail -f -c +1 PiCar_log.txt