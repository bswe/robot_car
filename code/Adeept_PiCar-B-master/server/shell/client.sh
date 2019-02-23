#!/bin/bash

# script to start PiCar client SW and log it's output

cd /home/pi/Adeept_PiCar-B-V1.0/code/Adeept_PiCar-B-master/client

echo -e "\n======================================================================================" >> /home/pi/Desktop/Client_log.txt
echo "running cmd 'python3 /home/pi/Adeept_PiCar-B/client/client.py' $(date)" >> /home/pi/Desktop/Client_log.txt
python3 -u /home/pi/Adeept_PiCar-B-V1.0/code/Adeept_PiCar-B-master/client/client.py >> /home/pi/Desktop/Client_log.txt 2>&1
