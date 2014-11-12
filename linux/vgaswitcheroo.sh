#!/bin/sh

read USAGE <<EOF
allowed argument must be either ON or OFF
EOF

vgaswitcheroo="/sys/kernel/debug/vgaswitcheroo/switch"

case $1 in
ON|OFF) SWITCH=$1;;
STATE) cat $vgaswitcheroo; exit 0;;
*) echo $USAGE; exit 1;;
esac

if [ ! -e $vgaswitcheroo ]
then
    echo "$vgaswitcheroo does not exists!"
    exit 2
fi

if [ -w $vgaswitcheroo ]
then
    echo $SWITCH > $vgaswitcheroo
else
    echo "You can't write to $vgaswitcheroo !"
    exit 3
fi

