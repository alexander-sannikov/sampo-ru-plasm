# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kio import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.solid import Solid

import httplib2 
from BeautifulSoup import BeautifulSoup
   
    
class SampoPlasmoid(plasmascript.Applet):
    """Applet main class"""

    def __init__(self, parent, args=None):
        self.stat_info = {'uid':'', 'money':'', 'daily_pay':'', 'speed':''}
        plasmascript.Applet.__init__(self, parent)
        
    def init(self):
        """Applet settings"""
	self.get_info()
	#TODO:add configuration interface
        #self.setHasConfigurationInterface(True)
        #self.setAspectRatioMode(Plasma.Square)
        
        #setup  background
	self.theme = Plasma.Svg(self)
	self.theme.setImagePath("widgets/background")
	self.setBackgroundHints(Plasma.Applet.DefaultBackground)
    
	#create layout
	self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
    
	#create UI-objects
	self.labelb = Plasma.Label(self.applet)
	self.labelb.setText(u"Номер счета: %s" % (self.stat_info['uid'].decode('utf-8')))
	self.labelm = Plasma.Label(self.applet)
	if float(self.stat_info['money'].split(" ")[0]) <= float(self.stat_info['daily_pay'].split(" ")[0]):
	    col = "c70028"
	else:
	    col = "008000"
	self.labelm.setText(u"На счету:<FONT COLOR=#%s><b> %s</b></FONT>" % (col,self.stat_info['money']))
	self.labeld = Plasma.Label(self.applet)
	self.labeld.setText(u"Расход: <b>%s</b>" % (self.stat_info['daily_pay']))
	self.labels = Plasma.Label(self.applet)
	self.labels.setText(u"Скорость: <b>%s</b>" % (self.stat_info['speed']))    
    
	#construct UI
	self.layout.addItem(self.labelb)
	self.layout.addItem(self.labelm)
	self.layout.addItem(self.labeld)
	self.layout.addItem(self.labels)
	
        self.applet.setLayout(self.layout)
        #self.resize(100, 100)
        
        #daa update timer
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout(bool)"), self.get_info)
        
    def postInit(self):
	    """Start timer and do first data fetching

	    Fired only if user opened access to KWallet"""
	    #update information one time in houre
	    self.timer.start(1000*60*60)
	    self.get_info()
	    
    def update(self, value):
	  """Update label text"""
	   
	  self.labelb.setText(u"Номер счета: %s" % (self.stat_info['uid'].decode('utf-8')))
	  if int(self.stat_info['money'].split(" ")[0]) <= int(self.stat_info['daily_pay'].split(" ")[0]):
	      col = "c70028"
	  else:
	      col = "008000"
	  self.labelm.setText(u"На счету:<FONT COLOR=#%s><b> %s</b></FONT>" % (col,self.stat_info['money']))
	  self.labeld.setText(u"Расход: %s" % (self.stat_info['daily_pay']))
	  self.labels.setText(u"Скорость: %s" % (self.stat_info['speed']))    
    


    def timerEvent(self, event):
	    """Create thread by timer"""

	    self.get_info()

    def get_info(self):
	    """Get statserv.sampo.ru page and extract buill state"""
	    try:
		cont=httplib2.Http().request("http://statserv.sampo.ru","GET")[1]
	    except httplib2.HttpLib2Error:
		print 'Network Error.'
		return None
	    soup = BeautifulSoup(cont, fromEncoding="cp-1251")
	    self.stat_info['money'] = soup.find('td','statMoney').div.string
	    self.stat_info['speed'] = soup.find('dl','speed').dd.string
	    self.stat_info['daily_pay'] = soup.find('dl','outlays').dd.string
	    self.stat_info['uid'] = str(soup.find('tr','grey')).split("<")[4].split(">")[1]
	    
	    
        
def CreateApplet(parent):
    return SampoPlasmoid(parent)