#!/usr/bin/bash
HOST='192.168.1.3'
USER='user'
PASS='user'
TARGETFOLDER='/DATA/share/YY_F1/cc2024'/$TODAY
SOURCEFOLDER='/home/alilong/TakeGuess_data/cc2024'/$TODAY

echo .........
echo Mirror $HOST$TARGETFOLDER
echo From localhost $SOURCEFOLDER

lftp -v -c "
open $HOST
user $USER $PASS
lcd $SOURCEFOLDER
mirror --reverse --delete --verbose=3 --no-perms $SOURCEFOLDER $TARGETFOLDER
bye
"

echo ...end of mirror...
