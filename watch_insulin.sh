#!/bin/bash
WATCH_DIR="/home/ec2-user/environment/insulin_data"
while inotifywait -e create "$WATCH_DIR"; do
    python3 /home/ec2-user/environment/AsamAminoClean/clean_insulin.py
done
