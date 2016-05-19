#!/bin/sh
# created by Lizard
SERIALFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial"
TIMEOUTFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout"
checkoscamrun=0
if [[ $checkoscamrun == 1 ]]; then
	oscamversion=$(find -L /tmp -name "oscam.version" 2>/dev/null)
	oscampid=$(grep "PID:" $oscamversion|awk '{ print $2 }')
	if [[ ! -e /proc/$oscampid ]]; then
		wget -O /dev/null -q 'http://127.0.0.1/web/message?text=Oscam%20läuft%20nicht,\n%20bitte%20Oscam%20erst%20starten.&type=1&timeout=10'
		exit
	fi
fi
if [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -gt 0 ]; then
	echo "Log EMM läuft schon.\n"
fi
if [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -lt 1 ]; then
	nohup /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh >output 2>&1 &
	echo "Log EMM wurde gestartet, Laufzeit "$(cat $TIMEOUTFILE)" Sekunden und wird mit Serial "$(cat $SERIALFILE)" geloggt.\n"
fi
