#!/bin/sh

xargs rm -r <files-installed.txt
rm files-installed.txt
rm -r build/ DirtyRF.egg-info/ dist/
