#!/bin/sh
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
echo "Checking for update from git"
echo "git -C $SCRIPTPATH pull"
git -C "$SCRIPTPATH" pull

python3 "$SCRIPTPATH"/chilli.py

