#!/bin/sh
# created by Lizard
EMMLOGFILE="" # falls notwendig hier bitte Pfad/Datei zur separaten Log-Datei zwischen den Anführungszeichen eingeben (z.B. "/usr/keys/sky_unique_emm.log").

SERIALFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial"
TIMEOUTFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout"
POPUPFILE="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/popup"
label=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel)
oscamversion=$(find -L /tmp -name "oscam.version" 2>/dev/null)
oscamconfpath=$(grep "ConfigDir:" $oscamversion|awk '{ print $2 }')

if [[ $EMMLOGFILE == "" ]]; then
	if [[ $oscamconfpath == "" ]]; then
		oscamconfpath=$(find /usr -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
	fi
	if [[ $oscamconfpath == "" ]]; then
		oscamconfpath=$(find /var -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
	fi
	if [[ $oscamconfpath == "" ]]; then
		oscamconfpath=$(find /etc -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
	fi
	logdir=$(grep "emmlogdir" $oscamconfpath/oscam.conf|awk '{ print $3 }')
	if [[ $logdir == "" ]]; then
		logdir=$oscamconfpath
	fi
	logfile=$logdir"/"$label"_unique_emm.log"
else
	logfile=$EMMLOGFILE
fi
rm -f /tmp/bp-emm-tmp.log
a=0
i=$(cat $SERIALFILE)
p=$(cat $POPUPFILE)
timenow=$(date +%s)
runseconds=$(cat $TIMEOUTFILE)
limit=$(($timenow+$runseconds))
while true
do
	while [ $(ps -ef|grep -v grep|grep -c 'dvbsnoop') -gt 0 ]
	do
		if [ "$timenow" -gt "$limit" ]; then
			pkill -9 dvbsnoop
			pkill -9 log.sh
		fi
		sleep 1
		timenow=$(date +%s)
	done
	egrep -v '^\s*$|^#' /tmp/bp-emm-tmp.log | tr -d " " | tr a-z A-Z | awk 'BEGIN { FIELDWIDTHS = "8 8 3000" } "^8270..41" {now=strftime("%Y/%m/%d %H:%M:%S"); printf "%s   %s00000000   %s%s%s bp-emmlog\n", now, $2, $1, $2, $3}' >> $logfile
	if [ $a -gt 0 ] && [ $p == "True" ]; then
		lastlog=$(tail -n 1 $logfile)
		emm=${lastlog:41:6}
		wget -O /dev/null -q 'http://127.0.0.1/web/message?text=Ein%20EMM%20wurde%20geloggt\n'$emm'...&type=1&timeout=5'
	fi
	dvbsnoop -devnr 0 -ph 2 -n 1 -npd -f 0x82.0x40.0x${i:0:2}.0x${i:2:2}.0x${i:4:2}.0x${i:6:2}.0.0.0.0.0.0.0.0.0.0 -m 0xff.0xc0.0xff.0xff.0xff.0xff.0.0.0.0.0.0.0.0.0.0 0x1008 >/tmp/bp-emm-tmp.log &
	a=1
done
