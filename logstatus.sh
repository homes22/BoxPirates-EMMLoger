#!/bin/sh
# created by Lizard
SERIALFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial"
TIMEOUTFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout"
oscamversion=$(find -L /tmp -name "oscam.version" 2>/dev/null)
oscamconfpath=$(grep "ConfigDir:" $oscamversion|awk '{ print $2 }')
oscampid=$(grep "PID:" $oscamversion|awk '{ print $2 }')
label=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel)

if [[ ! -e /proc/$oscampid ]]; then
	wget -O /dev/null -q 'http://127.0.0.1/web/message?text=Oscam%20läuft%20nicht,\n%20bitte%20Oscam%20erst%20starten.&type=1&timeout=10'
	echo "Oscam läuft nicht,\nbitte Oscam erst starten.\n"
	exit
fi
echo "... bitte warten, überprüfe Label"
if [[ $oscamconfpath == "" ]]; then
	oscamconfpath=$(find /usr -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
fi
if [[ $oscamconfpath == "" ]]; then
	oscamconfpath=$(find /var -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
fi
if [[ $oscamconfpath == "" ]]; then
	oscamconfpath=$(find /etc -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
fi
count=0
while read line
do
	if [[ $(echo $line|grep "label"|awk '{ print $3 }') == $label ]]; then
		count=1
		break
	fi
done < $oscamconfpath/oscam.server
if [[ $count == 0 ]]; then 
   	nohup wget -O /dev/null -q 'http://127.0.0.1/web/message?text=Angegebenes%20Label%20existiert%20nicht%20in%20der%20Oscam-Konfig.\nBitte%20Label%20überprüfen.&type=3&timeout=15' >output 2>&1 &
	echo "\nAngegebenes Label existiert nicht in der Oscam-Konfig.\nBitte Label überprüfen.\n"
	exit
fi
if [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -gt 0 ]; then
	echo "Log EMM läuft schon.\n"
fi
if [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -lt 1 ]; then
	nohup /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh >output 2>&1 &
	echo "Log EMM wurde gestartet, Laufzeit "$(cat $TIMEOUTFILE)" Sekunden und wird mit Serial "$(cat $SERIALFILE)" geloggt.\n"
fi
