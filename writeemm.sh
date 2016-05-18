#!/bin/sh
# created by Lizard
oscamconfpath="" # falls notwendig hier bitte Pfad zu Oscam Konfig zwischen den Anführungszeichen eingeben (z.B. "/var/keys").

z=$1
function testoscamconfpath {
if [[ $oscamconfpath == "" ]]; then
	if [[ $z == "" ]]; then
		echo "... suche Konfig-Pfad in /usr"
	fi
	oscamconfpath=$(find /usr -name "oscam.conf"|xargs dirname)
fi
if [[ $oscamconfpath == "" ]]; then
	if [[ $z == "" ]]; then
		echo "... suche Konfig-Pfad in /var"
	fi
	oscamconfpath=$(find /var -name "oscam.conf"|xargs dirname)
fi
if [[ $oscamconfpath == "" ]]; then
	if [[ $z == "" ]]; then
		echo "... suche Konfig-Pfad in /etc"
	fi
	oscamconfpath=$(find /etc -name "oscam.conf"|xargs dirname)
fi
}

testoscamconfpath
if [[ $z == "" ]]; then
	echo "... Konfig-Pfad = "$oscamconfpath
fi
user=$(grep "httpuser" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
pass=$(grep "httppwd" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
port=$(grep "httpport" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
label=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel)
if [[ $z == "" ]]; then
	echo "... angegebenes Label = "$label
	echo "... Konfig wird auf angegebenes Label geprüft"
	count=0
	while read line
	do
		if [[ $(echo $line|grep "label"|awk '{ print $3 }') == $label ]]; then
			count=1
    		echo "... Label = "$label" wurde in Konfig gefunden"
    		break
		fi
	done < $oscamconfpath/oscam.server

	if [[ $count == 0 ]]; then
		echo "... angegebenes Label kommt nicht in der oscam.server vor"
		echo "... bitte angegebenes Label oder Konfig überprüfen."
		echo "... Prozedur wurde abgebrochen."
		echo ""
		exit
	fi
fi

if [[ $z == "" ]]; then
	emm=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm|awk '{ print $4 }')
	echo "... EMM = "${emm:0:6}"..."
	if [[ $emm != "" ]]; then
		echo "... schreibe EMM für Label = "$label
		curl -s -o /dev/null --digest -u $user:$pass "http://127.0.0.1:"$port"/emm_running.html?label="$label"&ep="$emm"&emmfile=&action=Launch"
		rm /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm
		echo "... EMM für Label = "$label" wurde geschrieben"
	fi
	echo ""
fi
if [[ $z == "expire" ]]; then
	curl -s -o /tmp/webif --digest -u $user:$pass "http://127.0.0.1:"$port"/entitlements.html?label="$label
	sed -n "/<TR CLASS=\"e_valid\">/,/<\/TABLE>/p" /tmp/webif > /tmp/webif1
	if [[ $(stat -c %s /tmp/webif1) == "0" ]]; then
		sed -n "/<TR CLASS=\"e_expired\">/,/<\/TABLE>/p" /tmp/webif > /tmp/webif1
		if [[ $(grep -c "Reader does not exist or is not started!" /tmp/webif) -gt 0 ]]; then
			echo "Reader existiert nicht oder ist nicht gestartet"
		else
			echo "... abgelaufen"
		fi
	fi
	expirecaid=$(cat /tmp/webif1|awk -F '<TD>' '{print $3}'|awk -F '</TD>' '{print $1}')
	expiretier=$(cat /tmp/webif1|awk -F '<TD>' '{print $5}'|awk -F '</TD>' '{print $1}')
	expiredate=$(cat /tmp/webif1|awk -F '<TD>' '{print $8}'|awk -F '</TD>' '{print $1}')
	a=0
	i=0
	for b in $expirecaid; do
		c[$i]=$b
		i=$(( $i + 1 ))
	done
	i=0
	for b in $expiretier; do
		t[$i]=$b
		i=$(( $i + 1 ))
	done
	i=0
	for b in $expiredate; do
		d[$i]=$b
		i=$(( $i + 1 ))
	done
	while [ $a -lt $i ]; do
		echo ${c[a]}":"${t[a]}":"${d[a]}
		a=$(( $a + 1 ))
	done
	rm /tmp/webif
	rm /tmp/webif1
fi
if [[ $z == "testconf" ]]; then
	testoscamconfpath
	if [[ $(grep "EMMLOGFILE=" /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh|cut -d "=" -f2|cut -d " " -f1|tr -d '"') == "" ]]; then
		logdir=$(grep "emmlogdir" $oscamconfpath/oscam.conf|awk '{ print $3 }')
		if [[ $logdir == "" ]]; then
			logdir=$oscamconfpath
		fi
		logfile=$logdir"/"$label"_unique_emm.log"
	else
		logfile=$(grep "EMMLOGFILE=" /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh|cut -d "=" -f2|cut -d " " -f1|tr -d '"')
	fi
	if [[ -f $logfile ]]; then
		echo $logfile
	else
		echo "none"
		nohup wget -O /dev/null -q 'http://127.0.0.1/web/message?text=Logfile%20existiert%20nicht.\n%20Bitte%20Label%20überprüfen.\n%20Falls%20ein%20separates%20Logfile%20angegeben%20wurde,\n%20bitte%20diesen%20Pfad/Datei%20überprüfen.&type=3&timeout=15' >output 2>&1 &
	fi
fi
