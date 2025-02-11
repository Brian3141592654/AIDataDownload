#!/usr/bin/bash

cd /home/alilong/TakeGuess
./sync_from_net.sh

DESTPATH=~/TakeGuess_data/cc2024
SRCPATH=~/TakeGuess_data/csv

echo Remove old data
rm -rf $SRCPATH.old
mv $SRCPATH $SRCPATH.old
mkdir $SRCPATH

echo Run Program to Get TWSE Data......
./demo4.py

echo .
echo .
TODAY=`date '+%Y-%m-%d'`
export TODAY
D0=$DESTPATH/$TODAY

echo Copy $SRCPATH to Directory of Today: $D0
rm -rf $D0
mkdir $D0
cp $SRCPATH/* $D0/

./sync_to_net.sh
./remove_old_files.sh
