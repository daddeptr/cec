#!/bin/bash

if pgrep -x "/Users/pietrobo/PycharmProjects/CEC/run.py" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
    /Users/pietrobo/PycharmProjects/CEC/venv/bin/python3 /Users/pietrobo/PycharmProjects/CEC/run.py &
fi

# Windows:
# start filename_or_URL

# Borrowing some time for the application to start
sleep 5

# Launching the application on the browser
open http://127.0.0.1:5000