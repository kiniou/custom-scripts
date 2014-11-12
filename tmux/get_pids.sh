#!/bin/sh
tmux lsp -a -F "#{pane_pid}###{session_name}" | while read n; do _pid=$(echo $n | cut -f1 -d\#); echo $n|cut -f2 -d\#;ps --forest --no-headers -o pid,args --ppid ${_pid} -p ${_pid}; done
