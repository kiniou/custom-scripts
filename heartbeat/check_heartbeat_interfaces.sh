#!/bin/sh

HARESSOURCES="./haressources"
ERROR=0
cat ${HARESSOURCES} | sed -n -r -e "s/^.*IPaddr::([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*$/\1/p" | while read n; do

    if [ -z "$(ip addr show to $n)" ]; then
        echo "${n} is not correctly setted up !!"
        ERROR=1
    fi

    if [ ${ERROR} -ne 0 ]; then
        echo "ERROR: Heartbeat failed to setup some interfaces."
        echo "You must restart the service like the following: "
        echo "sudo /etc/init.d/heartbeat stop"
        echo "sudo /etc/init.d/heartbeat start"
    fi
done
