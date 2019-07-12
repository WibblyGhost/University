#!/bin/bash

for f in conf/*.txt
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  xterm -e ./controller.py $f &
done