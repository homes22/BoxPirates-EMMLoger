#!/bin/sh
# created by Lizard
oscamconfpath="" # hier bitte Pfad zu Oscam Konfig zwischen den Anführungszeichen eingeben falls notwendig (z.B. "/var/keys").

if [[ $oscamconfpath == "" ]]; then
	if [[ $1 == "" ]]; then
		echo "... suche Konfig-Pfad in /usr"
	fi
	oscamconfpath=$(find /usr -name "oscam.conf"|xargs dirname)
fi
if [[ $oscamconfpath == "" ]]; then
	if [[ $1 == "" ]]; then
		echo "... suche Konfig-Pfad in /var"
	fi
	oscamconfpath=$(find /var -name "oscam.conf"|xargs dirname)
fi
if [[ $oscamconfpath == "" ]]; then
	if [[ $1 == "" ]]; then
		echo "... suche Konfig-Pfad in /etc"
	fi
	oscamconfpath=$(find /etc -name "oscam.conf"|xargs dirname)
fi
if [[ $1 == "" ]]; then
	echo "... Konfig-Pfad = "$oscamconfpath
fi
user=$(grep "httpuser" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
pass=$(grep "httppwd" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
port=$(grep "httpport" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
label=$(grep "EMMLOGFILE=" /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh|cut -d "\"" -f2|xargs -I"{}" basename {} _unique_emm.log)
echo "... Label = "$label
if [[ $1 == "" ]]; then
	emm=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm|awk '{ print $4 }')
	echo "... EMM = "${emm:0:6}"..."
	if [[ $emm != "" ]]; then
		echo "... schreibe EMM"
		curl -s -o /dev/null --digest -u $user:$pass "http://127.0.0.1:"$port"/emm_running.html?label="$label"&ep="$emm"&emmfile=&action=Launch"
		rm /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm
		echo "... EMM wurde geschrieben"
	fi
	echo ""
fi
if [[ $1 == "expire" ]]; then
	curl -s -o /tmp/webif --digest -u $user:$pass "http://127.0.0.1:"$port"/entitlements.html?label="$label
	sed -n "/<TR CLASS=\"e_valid\">/,/<\/TABLE>/p" /tmp/webif > /tmp/webif1
	if [[ $(stat -c %s /tmp/webif1) == "0" ]]; then
		sed -n "/<TR CLASS=\"e_expired\">/,/<\/TABLE>/p" /tmp/webif > /tmp/webif1
		echo "... abgelaufen"
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
