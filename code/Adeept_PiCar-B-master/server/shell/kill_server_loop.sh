#!/bin/bash

pgrep -f "shell/server_loop.sh" | xargs kill
sudo killall -s SIGINT python3
