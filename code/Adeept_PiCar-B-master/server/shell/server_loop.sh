#!/bin/bash

# script to continuously restart PiCar server SW and log it's output

cd /home/pi/Adeept_PiCar-B-V1.0/code/Adeept_PiCar-B-master/server

while true
do
	echo -e "\n======================================================================================" >> /home/pi/Desktop/PiCar_log.txt
        echo "running cmd 'sudo python3 /home/pi/Adeept_PiCar-B/server/server.py' $(date)" >> /home/pi/Desktop/PiCar_log.txt
	sudo python3 -u /home/pi/Adeept_PiCar-B-V1.0/code/Adeept_PiCar-B-master/server/server.py >> /home/pi/Desktop/PiCar_log.txt 2>&1
done