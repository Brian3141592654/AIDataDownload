#!/usr/bin/bash
FILENAME='stocklist.txt'
HOST='192.168.1.3'
USER='user'
PASS='user'
REMOTEFOLDER='/DATA/share/cc2024'
LOCALFOLDER='/home/TakeGuess_data'

REMOTEFILE="${REMOTEFOLDER}/${FILENAME}"
LOCALFILE="${LOCALFOLDER}/${FILENAME}"
echo "ftp ${REMOTEFILE} --> ${LOCALFILE}"

rm $LOCALFILE.old || true
mv $LOCALFILE $LOCALFILE.old || true

echo .........
lftp -v -c "
open $HOST
user $USER $PASS
lcd $LOCALFOLDER
get1 $REMOTEFILE
bye
"

if test -f $LOCALFILE; then
    echo "ftp get ${LOCALFILE} done"
else
    zenity --error --text="ERROR: No ${FILENAME}"
fi

echo .........
