from Plugins.Plugin import PluginDescriptor
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

class emmlog(ConfigListScreen, Screen):
    skin = """<screen position="100,100" size="560,320" title="EMMLog (v1.5)" >
	<widget name="text" position="5,50" zPosition="2" size="520,60" font="Regular;20" />
	<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/images/key_ok.png" position="5,230" size="140,40" alphatest="on" />
	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/images/key_1.png" position="5,270" size="140,40" alphatest="on" />
	<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	<widget name="config" position="20,120" size="520,240" scrollbarMode="showOnDemand" />
	<widget name="key_ok" position="32,220" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	<widget name="key_1" position="32,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""


    def __init__(self, session, args = None):
        self.skin = emmlog.skin
        Screen.__init__(self, session)
        info = 'Bei der eingabe der Serial auf das \nrichtige Format achten. XXXXXXXX'
        self['text'] = Label(info)
        self.list = []
        self.list.append(getConfigListEntry(_('Card Serial'), config.plugins.emmlog.serial))
        self.list.append(getConfigListEntry(_('Log timeout (min)'), config.plugins.emmlog.emmlog_timeout))
        self.list.append(getConfigListEntry(_('EMM-Popup anzeigen'), config.plugins.emmlog.popup))
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Button(_('cancel'))		
        self['key_green'] = Button(_('Save Serial'))
        self['key_yellow'] = Button(_('Stop Log'))
        self['key_blue'] = Button(_('Start Log'))
        self['key_ok'] = Button(_('Load defaults'))
        self['key_1'] = Button(_('write EMM'))		
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'NumberActions'], {'green': self.save,
         'red': self.cancel,
         'yellow': self.stoplog,
         'blue': self.startlog,
		 'save': self.save,
         'cancel': self.cancel,
         'ok': self.defaults,
         '1': self.readsemm,}, -2)

    def save(self):
        for x in self['config'].list:
            x[1].save()
			

        self.close(True)

    def cancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close(False)

    def defaults(self):
        config.plugins.emmlog.serial.setValue('XXXXXXXX')
        config.plugins.emmlog.emmlog_timeout.setValue(10)
        config.plugins.emmlog.popup.setValue(False)
        for x in self['config'].list:
            x[1].save()

        self.close(True)		
		
    def startlog(self):
		timeout = str(config.plugins.emmlog.emmlog_timeout.value*60)
		popup = str(config.plugins.emmlog.popup.value)
		system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial')
		system('echo ' + config.plugins.emmlog.serial.value + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/serial')
		system('echo ' + popup + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/popup')
		system('echo ' + timeout + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/timeout')
		dom = config.plugins.emmlog.serial.value
		com = config.plugins.emmlog.serial.value
		system('/bin/chmod +x /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/log.sh')
		system('/bin/chmod +x /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/logstatus.sh')
		script = '/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/logstatus.sh'
		self.session.open(Console, _('emmlog: %s') % dom, [script])
		
	
    def stoplog(self):
		self.session.open(Console, _('EmmLog:'), ['echo "Log beendet" && pkill -9 dvbsnoop && pkill -9 sleep && pkill -9 log.sh'])
	
    def readsemm (self):
        self.session.open(reademm)
	
class reademm(Screen):

    skin ="""<screen name="reademm" position="center,center" size="1160,600" title="CR-Feed-CCcam-Download"  flags="wfNoBorder" >
	<widget name="list" position="20,20" size="1120,450" scrollbarMode="showOnDemand" transparent="1" zPosition="2" font="Regular;17"/>
	<widget name="key_blue" position="400,530" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
	</screen>"""


    def __init__(self, session):
        self.skin = reademm.skin
        Screen.__init__(self, session)
        self['key_blue'] = Button(_('schreibe EMM'))
        self.list = []
        self['list'] = MenuList([])
        self['info'] = Label()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'blue': self.okClicked,
         'ok': self.okClicked,
         'cancel': self.close}, -1)
        self.addon = 'emu'
        self.icount = 0
        self.timer = eTimer()
        self.timer.callback.append(self.openTest)
        self.timer.start(100, 1)

    def openTest(self):
        try:
            myfile = file('/usr/keys/sky_unique_emm.log')
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

    def okClicked(self):
        try:
            sel = self['list'].getSelectionIndex()
            addon = self.names[sel]
            ipk = self.data[sel]
            system('echo ' + ipk + ' > /usr/lib/enigma2/python/Plugins/Extensions/EMMLog/emm')
            writeemm = '/usr/lib/enigma2/python/Plugins/Extensions/EMMLog/writeemm.sh'
            self.session.open(Console,_('writeemm:'),[writeemm])			
        except:
            pass

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
    return [PluginDescriptor(name='BoxPirates-EmmLog', description=_('EmmLoggen for serial'), where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main, icon='plugin.png')]

