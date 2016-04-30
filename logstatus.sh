#!/bin/sh
# created by Lizard
SERIALFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial"
TIMEOUTFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout"
if [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -gt 0 ]; then
	echo "Log EMM läuft schon.\n"
fi
if [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -lt 1 ]; then
	nohup /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh >output 2>&1 &
	echo "Log EMM wurde gestartet, Laufzeit "$(cat $TIMEOUTFILE)" Sekunden und wird mit Serial "$(cat $SERIALFILE)" geloggt.\n"
fi
