#!/bin/sh
# created by Lizard
label=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel)
oscamversion=$(find -L /tmp -name "oscam.version" 2>/dev/null)
oscamconfpath=$(grep "ConfigDir:" $oscamversion|awk '{ print $2 }')
if [[ $oscamconfpath == "" ]]; then
	oscamconfpath=$(find /usr -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
fi
if [[ $oscamconfpath == "" ]]; then
	oscamconfpath=$(find /var -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
fi
if [[ $oscamconfpath == "" ]]; then
	oscamconfpath=$(find /etc -name "oscam.conf" 2>/dev/null|xargs dirname 2>/dev/null)
fi
if [[ $(grep "EMMLOGFILE=" /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh|cut -d "=" -f2|cut -d " " -f1|tr -d '"') == "" ]]; then
	logdir=$(grep "emmlogdir" $oscamconfpath/oscam.conf|awk '{ print $3 }')
	if [[ $logdir == "" ]]; then
		logdir=$oscamconfpath
	fi
	logfile=$logdir"/"$label"_unique_emm.log"
else
	logfile=$(grep "EMMLOGFILE=" /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh|cut -d "=" -f2|cut -d " " -f1|tr -d '"')
fi
bakfile=$(basename $logfile .log)".bak"
cat $logfile >> $logdir/$bakfile
rm $logfile
touch $logfile
echo "EMM's wurden nach $bakfile übertragen\nLogfile ist nun leer.\n"
