#!/bin/bash

if [ -z $1 ]
then
  echo "Options:
    develop - install symlinks, for dev only
    install - real installation
  "
else
  python setup.py $1 --record files-installed.txt
fi
