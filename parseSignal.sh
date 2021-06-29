#!/bin/bash

sudo apt update > /dev/null
sudo apt -y upgrade > /dev/null

sudo apt -y install python3 python3-pip git > /dev/null
sudo pip install flask

if [$1 -eq 0]
then
export SIGNAL_VERSION="old"
else
export SIGNAL_VERSION=$1
fi

flask run