#!/bin/sh
# created by Lizard
oscamconfpath="" # hier bitte Pfad zu Oscam Konfig zwischen den Anführungszeichen eingeben falls notwendig (z.B. "/var/keys").

if [[ $oscamconfpath == "" ]]; then
echo "... suche Konfig-Pfad in /usr"
oscamconfpath=$(find /usr -name "oscam.conf"|xargs dirname)
fi
if [[ $oscamconfpath == "" ]]; then
echo "... suche Konfig-Pfad in /var"
oscamconfpath=$(find /var -name "oscam.conf"|xargs dirname)
fi
if [[ $oscamconfpath == "" ]]; then
echo "... suche Konfig-Pfad in /etc"
oscamconfpath=$(find /etc -name "oscam.conf"|xargs dirname)
fi
echo "... Konfig-Pfad = "$oscamconfpath
user=$(grep "httpuser" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
pass=$(grep "httppwd" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
port=$(grep "httpport" $oscamconfpath/oscam.conf|cut -d "=" -f2|awk '{ print $1 }')
label=$(grep "EMMLOGFILE=" /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh|cut -d "\"" -f2|xargs -I"{}" basename {} _unique_emm.log)
echo "... Label = "$label
emm=$(cat /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm|awk '{ print $4 }')
echo "... EMM = "${emm:0:6}"..."
if [[ $emm != "" ]]; then
echo "... schreibe EMM"
curl -s -o /dev/null --digest -u $user:$pass "http://127.0.0.1:"$port"/emm_running.html?label="$label"&ep="$emm"&emmfile=&action=Launch"
rm /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm
echo "... EMM wurde geschrieben"
fi
echo ""
