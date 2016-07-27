#!/usr/bin/python
#-*- coding:utf-8 -*-
from Plugins.Plugin import PluginDescriptor
import subprocess
import os
from os import system
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Button import Button
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigText, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigYesNo
from Components.MenuList import MenuList
from Components.ScrollLabel import ScrollLabel
from enigma import eTimer
config.plugins.emmlog = ConfigSubsection()
config.plugins.emmlog.serial = ConfigText('XXXXXXXX', fixed_size=False)
config.plugins.emmlog.emmlog_timeout = ConfigInteger(10, limits=(1, 180))
config.plugins.emmlog.popup = ConfigYesNo(default=False)
config.plugins.emmlog.oscamlabel = ConfigText('skyV14', fixed_size=False)
system('/bin/chmod +x /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh')
system('/bin/chmod +x /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/logstatus.sh')
system('/bin/chmod +x /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh')
system('/bin/chmod +x /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/deletelog.sh')
if ( not os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel')):
    system('echo ' + config.plugins.emmlog.oscamlabel.value + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel')

class emmlog(ConfigListScreen, Screen):
    </screen>"""

    def __init__(self, session, args = 0):
        self.session = session
		
        list = []
        list.append((_("Log Config"), "configscreen"))
        list.append((_("Emm Log"), "emmlogmanagement"))
        list.append((_("EMM read and write"), "emmread"))
        list.append((_("Expire Date"), "expiredate"))
		
        Screen.__init__(self, session)
        self["emmlog"] = MenuList(list)
        self["myActionMap"] = ActionMap(["SetupActions"],
        {
            "ok": self.go,
            "cancel": self.cancel
        }, -1)

    def go(self):
        returnValue = self["emmlog"].l.getCurrentSelection()[1]
        print "\n[emmlog] returnValue: " + returnValue + "\n"
		
        if returnValue is not None:
            if returnValue is "configscreen":
                self.session.open(configscreen)
				
            elif returnValue is "emmlogmanagement":
                self.session.open(emmlogmanagement)
					
            elif returnValue is "emmread":
                self.session.open(reademm)

            else:
                self.session.open(Console, _('Expire Date:'), ['echo "Expire Date" && /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh expire'])
	
    def cancel(self):
        self.close(None)
		
class configscreen(ConfigListScreen, Screen):
    skin = """<screen position="center,center" size="660,300" title="EMMLog config" >
	<widget name="text" position="5,20" zPosition="2" size="655,60" font="Regular;20" />
	<ePixmap pixmap="skin_default/buttons/yellow.png" position="190,250" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/green.png" position="330,250" size="140,40" alphatest="on" />
	<widget name="key_yellow" position="190,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	<widget name="key_green" position="330,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	<widget name="config" position="20,110" size="620,260" scrollbarMode="showOnDemand" />
	</screen>"""


    def __init__(self, session, args = None):
        self.skin = configscreen.skin
        Screen.__init__(self, session)
        info = 'Bei der Eingabe der Serial auf das richtige Format achten. XXXXXXXX \nBei der Eingabe des OSCam label auf Groß und Keinschreibung achten.'
        self['text'] = Label(info)
        self.list = []
        self.list.append(getConfigListEntry(_('Card Serial'), config.plugins.emmlog.serial))
        self.list.append(getConfigListEntry(_('Log timeout (min)'), config.plugins.emmlog.emmlog_timeout))
        self.list.append(getConfigListEntry(_('EMM-Popup anzeigen'), config.plugins.emmlog.popup))
        self.list.append(getConfigListEntry(_('OSCam reader Label'), config.plugins.emmlog.oscamlabel))
        ConfigListScreen.__init__(self, self.list)
        self['key_yellow'] = Button(_('Load defaults'))		
        self['key_green'] = Button(_('Save Config'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'NumberActions', 'HelpActions'], {'green': self.save,
         'yellow': self.defaults,
         'cancel': self.cancel}, -2)

    def save(self):
        for x in self['config'].list:
            x[1].save()
        timeout = str(config.plugins.emmlog.emmlog_timeout.value*60)
        popup = str(config.plugins.emmlog.popup.value)
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial')
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel')
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/popup')
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout')		
        system('echo ' + config.plugins.emmlog.serial.value + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial')
        system('echo ' + config.plugins.emmlog.oscamlabel.value + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel')		
        system('echo ' + popup + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/popup')
        system('echo ' + timeout + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout')
        system('/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh savetest')
        self.close(True)

    def cancel(self):
        for x in self['config'].list:
            x[1].cancel()
        
        self.close(False)

    def defaults(self):
        config.plugins.emmlog.serial.setValue('XXXXXXXX')
        config.plugins.emmlog.emmlog_timeout.setValue(10)
        config.plugins.emmlog.popup.setValue(False)
        config.plugins.emmlog.oscamlabel.setValue('SKYV14')
        for x in self['config'].list:
            x[1].save()

        self.close(True)

		
class emmlogmanagement(Screen):
    skin = """<screen position="center,center" size="660,80" title="EMMLog Management" >
	<ePixmap pixmap="skin_default/buttons/red.png" position="50,20" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/green.png" position="190,20" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/yellow.png" position="330,20" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/blue.png" position="470,20" size="140,40" alphatest="on" />
	<widget name="key_red" position="50,20" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	<widget name="key_green" position="190,20" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	<widget name="key_yellow" position="330,20" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	<widget name="key_blue" position="470,20" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	</screen>"""


    def __init__(self, session, args = None):
        self.skin = emmlogmanagement.skin
        Screen.__init__(self, session)
        info = 'Bei der Eingabe der Serial auf das richtige Format achten. XXXXXXXX \nBei der Eingabe des OSCam label auf Gross und Keinschreibung achten.'
        self['text'] = Label(info)
        self['key_red'] = Button(_('cancel'))
        self['key_green'] = Button(_('Clear Logfile'))		
        self['key_yellow'] = Button(_('Stop Log'))
        self['key_blue'] = Button(_('Start Log'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'NumberActions', 'HelpActions'], {'green': self.msgdeletelog,
         'red': self.cancel,
         'yellow': self.stoplog,
         'blue': self.startlog,
		 'cancel': self.cancel}, -2)

    def startlog(self):
        timeout = str(config.plugins.emmlog.emmlog_timeout.value*60)
        popup = str(config.plugins.emmlog.popup.value)
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial')
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel')
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/popup')
        system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout')		
        system('echo ' + config.plugins.emmlog.serial.value + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial')
        system('echo ' + config.plugins.emmlog.oscamlabel.value + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/oscamlabel')		
        system('echo ' + popup + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/popup')
        system('echo ' + timeout + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout')
        dom = config.plugins.emmlog.serial.value
        com = config.plugins.emmlog.serial.value
        script = '/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/logstatus.sh'
        self.session.open(Console, _('emmlog: %s') % dom, [script])
		
	
    def stoplog(self):
		self.session.open(Console, _('EmmLog:'), ['echo "Log beendet" && pkill -9 dvbsnoop && pkill -9 sleep && pkill -9 log.sh'])


    def cancel(self):
        print "\n[deletelog] cancel\n"
        self.close(None)

    def msgdeletelog (self):
        self.session.openWithCallback(self.deletelog, MessageBox, _("Willst du die Logdatei bereinigen loeschen??"), MessageBox.TYPE_YESNO)

    def deletelog (self, result):
        print "\n[deletelog] checking result\n"
        if result:
            try:
                deletelog = '/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/deletelog.sh'
                self.session.open(Console,_('deletelog:'),[deletelog])			
            except:
                pass		    
        else:
            print "\n[deletelog] OK pressed\n"
            self.close(None)
			
class reademm(Screen):

    skin ="""<screen name="reademm" position="center,center" size="1160,600" title="read EMM"  >
	<widget name="list" position="20,20" size="1120,450" scrollbarMode="showOnDemand" transparent="1" zPosition="2" font="Regular;17"/>
	<widget name="key_blue" position="553,522" size="140,40" halign="center" valign="center" font="Regular;19" backgroundColor="#9f1313" transparent="1" />
	<ePixmap pixmap="skin_default/buttons/blue.png" position="550,520" size="140,40" zPosition="-1" alphatest="on" />
	</screen>"""

    def __init__(self, session):
        self.skin = reademm.skin
        Screen.__init__(self, session)
        self['key_blue'] = Button(_('schreibe EMM'))
        a = ['/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh', 'testconf']
        y = subprocess.check_output(a).strip()
        if "none" == y:
            self.close(True)
        else:    
            self.list = []
            self['list'] = MenuList([])
            self['info'] = Label()
            self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'blue': self.Msgwriteemm,
             'ok': self.Msgwriteemm,
             'cancel': self.close}, -1)
            self.icount = 0
            self.timer = eTimer()
            self.timer.callback.append(self.openTest)
            self.timer.start(100, 1)

    def openTest(self):
        	    
        try:
            a = ['/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh', 'testconf']
            a = subprocess.check_output(a).strip()
            myfile = file(a)
            self.data = []
            self.names = []
            icount = 0
            list = []
            for line in myfile.readlines():
                self.data.append(icount)
                self.names.append(icount)
                self.data[icount] = line[:-10]
                emmname = self.data[icount]
                print 'icount, emm name =', icount, emmname
                self.names[icount] = emmname
                icount = icount + 1
                
            self['list'].setList(self.names)
        except:
            pass

    def okClicked(self, result):
        print "\n[okClicked] checking result\n"
        if result:
            try:
                sel = self['list'].getSelectionIndex()
                emmsel = self.names[sel]
                selemm = self.data[sel]
                system('echo ' + selemm + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm')
                writeemm = '/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh'
                self.session.open(Console,_('writeemm:'),[writeemm])			
            except:
                pass		    
        else:
            print "\n[okClicked] OK pressed\n"
            self.close(None)

    def Msgwriteemm(self):
        print "\n[okClicked] OK pressed\n"
        self.session.openWithCallback(self.okClicked, MessageBox, _("Willst du die EMM wirklich schreiben??"), MessageBox.TYPE_YESNO)
		
    def cancel(self):
        print "\n[okClicked] cancel\n"
        self.close(None)				
				
    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def keyNumberGlobal(self, number):
        print 'pressed', number
        self['text'].number(number)
		
def main(session, **kwargs):
    session.open(emmlog)


def Plugins(**kwargs):
    return [PluginDescriptor(name='BoxPirates-EmmLog', description=_('EmmLog for serial'), where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main, icon='plugin.png')]

