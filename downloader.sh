#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <magnet> <location> [show]"
    exit 1
fi
tmpfile=$(mktemp)
chmod a+x $tmpfile
if [ -d "$2" ]; then
    mkdir -p "$2"
fi
echo "Downloading to $2"
RANDOM_PORT=$(($RANDOM%5000+1024))
if [ $3 -eq 1 ]; then
    transmission-cli -p $RANDOM_PORT -f $tmpfile -w "$2" $1 &
else
    transmission-cli -p $RANDOM_PORT -f $tmpfile -w "$2" $1 >/dev/null 2>&1 &
fi
PID=$!
echo "#!/bin/bash" > $tmpfile
echo "kill -9 $PID" >> $tmpfile
echo "rm -f $tmpfile" >> $tmpfile
echo "Waiting: $PID"
wait $PID
echo "Complete $PID"
exit 0
