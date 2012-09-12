#!/usr/bin/python
# -*- coding: utf_8 -*- 

__author__  = 'PtitBigorneau'
__version__ = 'beta2'

import wx
import os, sys, ConfigParser, time

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import paramiko
from contextlib import contextmanager

from pyquake3 import PyQuake3

import wxPython.lib.dialogs
import wx.lib.agw.pybusyinfo as PBI

def fexist(fichier):
    
    try:
    
        file(fichier)
     
        return True
   
    except:
  
        return False 

def testssh(host, port, user, pwd):
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
    
        ssh.connect(host, int(port), username=user, password=pwd, timeout=1)
      
        return True
   
    except:
        
        return False

def testcfg(fichier):
    
    try:
    
        cfg = ConfigParser.ConfigParser()
        cfg.read(fichier)
        section = cfg.sections()
        
        for x in section:
            
            cgame = cfg.get(x,"game")
            cadresse = cfg.get(x,"adresse")
            cport = cfg.get(x,"port")
            sshport = cfg.get(x,"sshport")
            cuser = cfg.get(x,"user")
            cpwd = cfg.get(x,"pwd")
            crconpwd = cfg.get(x,"rconpwd")
            ccmdstart = cfg.get(x,"cmdstart")
            ccmdstop = cfg.get(x,"cmdstop")
            cbotname = cfg.get(x,"botname")
            cbotstop = cfg.get(x,"botstop")
     
        return True
   
    except:
  
        return False

def testconnect(adresse):

    try:

        q = PyQuake3(adresse)
        q.update()

        return True
   
    except:
  
        return False

def testpwdrcon(adresse, pwdrcon):

    try:

        q = PyQuake3(adresse, rcon_password=pwdrcon)
        q.rcon('status')

        return True
   
    except:
  
        return False

def cara(test):
   
    try:
            
        if fexist('test.cfg') == True:

            os.remove('test.cfg')

        cfg = ConfigParser.ConfigParser()
        cfg.read('test.cfg')
        cfg.add_section('section')
        cfg.set('section', 'test', test)
        cfg.write(open('test.cfg','w'))   
        os.remove('test.cfg')

        return True
   
    except:
  
        return False

def meserreur(erreur):

    texte =u" %s valeur non valide"%(erreur)

    dlg = wx.MessageDialog(None, texte, 'Erreur !', style = wx.OK | wx.ICON_ERROR)
    retour = dlg.ShowModal()
    dlg.Destroy() 

class MyFrame2(wx.Frame):

    file = 'pb-gscontrol.cfg'

    def __init__(self, titre):    
         
        wx.Frame.__init__(self, None, -1, title = titre, size=(850,670))
        
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        
        self.choices=['urt','trem']
        section = []
        if (fexist(self.file) == False) or (testcfg(self.file) == False):

            self.configs = ['']
            x=0

            self.cgame = 'urt'
            self.cadresse = ''
            self.cport = ''
            self.sshport = ''
            self.cuser = ''
            self.cpwd = ''
            self.crconpwd = ''
            self.ccmdstart = ''
            self.ccmdstop = ''
            self.cbotname = ''
            self.cbotstart = ''
            self.cbotstop = ''
            self.testvide = 'vide'

        if (fexist(self.file) == True) and (testcfg(self.file) == True):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            section = cfg.sections()

            if len(cfg.sections())==0:

                self.configs = ['']

                x=0
                self.cgame = 'urt'
                self.cadresse = ''
                self.cport = ''
                self.sshport = ''
                self.cuser = ''
                self.cpwd = ''
                self.crconpwd = ''
                self.ccmdstart = ''
                self.ccmdstop = ''
                self.cbotname = ''
                self.cbotstart = ''
                self.cbotstop = ''
                
                self.testvide = 'vide'

            else:
 
                self.testvide = 'nonvide'
                
                for x in section:
              
                    namesection.append(x)
               
                self.configs = namesection
                x = len(cfg.sections()) - 1
                self.server = section[x]
                self.cgame = cfg.get(section[x],"game")
                self.cadresse = cfg.get(section[x],"adresse")
                self.cport = cfg.get(section[x],"port")
                self.sshport = cfg.get(section[x],"sshport")
                self.cuser = cfg.get(section[x],"user")
                self.cpwd = cfg.get(section[x],"pwd")
                self.crconpwd = cfg.get(section[x],"rconpwd")
                self.ccmdstart = cfg.get(section[x],"cmdstart")
                self.ccmdstop = cfg.get(section[x],"cmdstop")
                self.cbotname = cfg.get(section[x],"botname")
                self.cbotstart = cfg.get(section[x],"botstart")
                self.cbotstop = cfg.get(section[x],"botstop")
       
        menuFichier = wx.Menu(style = wx.MENU_TEAROFF) 
        menuFichier.Append(101, "&Nouveau serveur\tCtrl+N", "Nouveau serveur")
        menuFichier.Append(104, "&Enregistrer\tCtrl+R", "Enregistrer un serveur")
        menuFichier.Append(103, "&Effacer\tCtrl+E", "Effacer un serveur")
       

        menuFichier.AppendSeparator() 
        menuFichier.Append(105, "&Quitter\tCtrl+Q", "Quitter PB-GSControl Configation") 

        menuHelp = wx.Menu()
        menuHelp.Append(106, "A propos","A propos de PB-GSControl")

        menuBarre = wx.MenuBar() 
        menuBarre.Append(menuFichier, "&Fichier")
        menuBarre.Append(menuHelp, "?")

        self.barre = wx.StatusBar(self, -1) 
        self.barre.SetFieldsCount(2) 
        self.barre.SetStatusWidths([-1, -1]) 

        self.SetStatusBar(self.barre)

        self.SetMenuBar(menuBarre)        

        toolbar = self.CreateToolBar()
        toolbar.AddSeparator()
        toolbar.AddLabelTool(101, 'Nouveau', wx.Bitmap('./new.bmp'),shortHelp='Nouveau', longHelp="Nouveau serveur")
        toolbar.AddLabelTool(104, '', wx.Bitmap('./enr.bmp'),shortHelp='Enregister', longHelp="Enregistrer un serveur")
        toolbar.AddLabelTool(103, '', wx.Bitmap('./effa.bmp'),shortHelp='Effacer', longHelp="Effacer un serveur")
        
        toolbar.AddSeparator()
        toolbar.AddLabelTool(105, '', wx.Bitmap('./exit.bmp'),shortHelp='Quitter', longHelp="Quitter Configuration PB-GSControl")
        toolbar.AddSeparator()
        toolbar.Realize()

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(10, 10)

        sizer = wx.GridBagSizer(6, 6)

        font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        fontc = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.BOLD)

        text1 = wx.StaticText(panel, label="Configuration PB-GSControl")
        sizer.Add(text1, pos=(0, 0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM, 
            border=20)

        font3 = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD)
        text1.SetFont(font3)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('confpb-gscontrol.gif'))
        sizer.Add(icon, pos=(0, 5), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, 
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 6), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        self.tgame = wx.ComboBox(panel,1,self.cgame, choices=self.choices, style=wx.CB_READONLY)
        sizer.Add(self.tgame, pos=(2, 0), span=(1, 1), flag=wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, border=10)
        self.tgame.SetFont(fontc)

        self.tconfig = wx.ComboBox(panel,12,self.configs[x], choices=self.configs, style=wx.CB_READONLY)
        sizer.Add(self.tconfig, pos=(2, 1), span=(1, 4), 
            flag=wx.TOP|wx.EXPAND, border=10)
        self.tconfig.SetFont(fontc)
        
        button2 = wx.Button(panel,1, label="Nouveau")
        sizer.Add(button2, pos=(2, 5), flag=wx.TOP|wx.RIGHT, border=8)        

        self.host = wx.StaticText(panel, label=" Adresse :                     ")
        sizer.Add(self.host, pos=(4, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.host.SetFont(font)

        self.thost = wx.TextCtrl(panel, value=self.cadresse)
        sizer.Add(self.thost, pos=(4, 1), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.port = wx.StaticText(panel, label=" Port :          ")
        sizer.Add(self.port, pos=(4, 2), flag=wx.LEFT|wx.TOP, border=10)
        self.port.SetFont(font)

        self.tport = wx.TextCtrl(panel, value=self.cport)
        sizer.Add(self.tport, pos=(4, 3), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.portssh = wx.StaticText(panel, label=" Port ssh : ")
        sizer.Add(self.portssh, pos=(4, 4), flag=wx.LEFT|wx.TOP, border=10)
        self.portssh.SetFont(font)

        self.tportssh = wx.TextCtrl(panel, value=self.sshport)
        sizer.Add(self.tportssh, pos=(4, 5), span=(1, 1), flag=wx.TOP|wx.EXPAND|wx.RIGHT, border=10)

        self.login = wx.StaticText(panel, label=" Login :                          ")
        sizer.Add(self.login, pos=(5, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.login.SetFont(font)

        self.tlogin = wx.TextCtrl(panel, value=self.cuser)
        sizer.Add(self.tlogin, pos=(5, 1), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.pwd = wx.StaticText(panel, label=" Password : ")
        sizer.Add(self.pwd, pos=(5, 2), flag=wx.LEFT|wx.TOP, border=10)
        self.pwd.SetFont(font)

        self.tpwd = wx.TextCtrl(panel, value=self.cpwd)
        sizer.Add(self.tpwd, pos=(5, 3), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.pwdrcon = wx.StaticText(panel, label=" rcon :       ")
        sizer.Add(self.pwdrcon, pos=(5, 4), flag=wx.LEFT|wx.TOP, border=10)
        self.pwdrcon.SetFont(font)

        self.tpwdrcon = wx.TextCtrl(panel, value=self.crconpwd)
        sizer.Add(self.tpwdrcon, pos=(5, 5), span=(1, 1), flag=wx.TOP|wx.EXPAND|wx.RIGHT, border=10)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(7, 0), span=(1, 6), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        self.serv = wx.StaticText(panel, label=" SERVEUR                       ")
        sizer.Add(self.serv, pos=(8, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.serv.SetFont(font)

        self.tserv = wx.StaticText(panel, label=self.cadresse+ ':' + self.cport)
        sizer.Add(self.tserv, pos=(8, 1), flag=wx.LEFT|wx.TOP, border=10)
        self.tserv.SetFont(font)

        self.startserv = wx.StaticText(panel, label=" Start :                           ")
        sizer.Add(self.startserv, pos=(9, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.startserv.SetFont(font)

        self.tstartserv = wx.TextCtrl(panel, value=self.ccmdstart)
        sizer.Add(self.tstartserv, pos=(9, 1), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.stopserv = wx.StaticText(panel, label=" Stop :          ")
        sizer.Add(self.stopserv, pos=(9, 2), flag=wx.LEFT|wx.TOP, border=10)
        self.stopserv.SetFont(font)

        self.tstopserv = wx.TextCtrl(panel, value=self.ccmdstop)
        sizer.Add(self.tstopserv, pos=(9, 3), span=(1, 2), flag=wx.TOP|wx.EXPAND, border=10)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(11, 0), span=(1, 6), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        self.bot = wx.StaticText(panel, label=" Bot Administration :     ")
        sizer.Add(self.bot, pos=(12, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.bot.SetFont(font)

        self.tbot = wx.TextCtrl(panel, value=self.cbotname)
        sizer.Add(self.tbot, pos=(12, 1), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.startbot = wx.StaticText(panel, label=" Start :                           ")
        sizer.Add(self.startbot, pos=(13, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.startbot.SetFont(font)

        self.tstartbot = wx.TextCtrl(panel, value=self.cbotstart)
        sizer.Add(self.tstartbot, pos=(13, 1), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        self.stopbot = wx.StaticText(panel, label=" Stop :          ")
        sizer.Add(self.stopbot, pos=(13, 2), flag=wx.LEFT|wx.TOP, border=10)
        self.stopbot.SetFont(font)

        self.tstopbot = wx.TextCtrl(panel, value=self.cbotstop)
        sizer.Add(self.tstopbot, pos=(13, 3), span=(1, 2), flag=wx.TOP|wx.EXPAND, border=10)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(15, 0), span=(1, 6), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        button3 = wx.Button(panel,2, label="Enregistrer")
        sizer.Add(button3, pos=(16, 4), flag=wx.TOP|wx.RIGHT, border=10)

        button4 = wx.Button(panel,3, label="Effacer")
        sizer.Add(button4, pos=(16, 5), flag=wx.TOP|wx.RIGHT, border=10)

        sizer.AddGrowableCol(1)
        
        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#f0f0f0")

        self.Bind(wx.EVT_COMBOBOX, self.Changetask, id=12)
        self.Bind(wx.EVT_BUTTON, self.Clickenr, id=2)
        self.Bind(wx.EVT_BUTTON, self.Clicknew, id=1)
        self.Bind(wx.EVT_BUTTON, self.Clickeff, id=3)
        
        wx.EVT_MENU(self, 104, self.Clickenr)
        wx.EVT_MENU(self, 101, self.Clicknew)
        wx.EVT_MENU(self, 103, self.Clickeff)
        wx.EVT_MENU(self, 105, self.Quit)
        wx.EVT_MENU(self, 106, self.About)

    def Changetask(self, evt):

        selec = self.tconfig.GetSelection()

         
        if (fexist(self.file) == True) and (testcfg(self.file) == True) and (self.testvide != 'vide'):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)
            section = cfg.sections()
              
            for x in section:
              
                namesection.append(x)
               
            self.server = section[int(selec)]
            self.cgame = cfg.get(section[int(selec)],"game")
            self.cadresse = cfg.get(section[int(selec)],"adresse")
            self.cport = cfg.get(section[int(selec)],"port")
            self.sshport = cfg.get(section[int(selec)],"sshport")
            self.cuser = cfg.get(section[int(selec)],"user")
            self.cpwd = cfg.get(section[int(selec)],"pwd")
            self.crconpwd = cfg.get(section[int(selec)],"rconpwd")
            self.ccmdstart = cfg.get(section[int(selec)],"cmdstart")
            self.ccmdstop = cfg.get(section[int(selec)],"cmdstop")
            self.cbotname = cfg.get(section[int(selec)],"botname")
            self.cbotstart = cfg.get(section[int(selec)],"botstart")
            self.cbotstop = cfg.get(section[int(selec)],"botstop")

            self.pwd = self.cpwd

            self.tgame.SetValue(self.cgame)
            self.thost.SetValue(self.cadresse)
            self.tport.SetValue(self.cport)
            self.tportssh.SetValue(self.sshport)
            self.tlogin.SetValue(self.cuser)
            self.tpwd.SetValue(self.cpwd)
            self.tpwdrcon.SetValue(self.crconpwd)
            self.tstartserv.SetValue(self.ccmdstart)
            self.tstopserv.SetValue(self.ccmdstop)
            self.tbot.SetValue(self.cbotname)
            self.tstartbot.SetValue(self.cbotstart)
            self.tstopbot.SetValue(self.cbotstop)
            self.tserv.SetLabel(self.cadresse+ ":" + self.cport)
            evt.Skip()

        return

    def Clickenr(self, evt):

        if testcfg(self.file) == False:

            dlg = wx.MessageDialog(self, "Erreur Fichier configuration !", "Erreur !" , style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 

            return

        if self.testvide == 'vide':

            texte = u"Pas de Serveur à enregistrer !"
        
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()

            return

        csection = self.server

        cgame=self.tgame.GetValue()
        cadresse=self.thost.GetValue()
        cport = self.tport.GetValue()
        csshport = self.tportssh.GetValue()
        cuser = self.tlogin.GetValue()
        cpwd = self.tpwd.GetValue()
        crconpwd = self.tpwdrcon.GetValue()
        ccmdstart = self.tstartserv.GetValue()
        ccmdstop = self.tstopserv.GetValue()
        cbotname = self.tbot.GetValue()
        cbotstart = self.tstartbot.GetValue()
        cbotstop = self.tstopbot.GetValue()
       
        if cara(cadresse) == False:

            meserreur('ADRESSE')
            self.thost.SetValue('')
            evt.Skip()
            return

        if cara(cport) == False:

            meserreur('PORT')
            self.tport.SetValue('')
            evt.Skip()
            return

        if cport !='':

            if not cport.isdigit():

                meserreur('PORT')
                self.tport.SetValue('')
                evt.Skip()
                return
        
        if cara(csshport) == False:

            meserreur('PORT SSH')
            self.tportssh.SetValue('')
            evt.Skip()
            return

        if csshport !='':

            if not csshport.isdigit():

                meserreur('PORT SSH')
                self.tportssh.SetValue('')
                evt.Skip()
                return
        
        if cara(cuser) == False:

            self.tlogin.SetValue('')
            evt.Skip()
            meserreur('LOGIN')
            return        

        if cara(cpwd) == False:

            self.tpwd.SetValue('')
            evt.Skip()
            meserreur('MOT DE PASSE')
            return

        if cara(crconpwd) == False:

            self.tpwdrcon.SetValue('')
            evt.Skip()
            meserreur('MOT DE PASSE RCON')
            return 

        if cara(ccmdstart) == False:

            self.tstartserv.SetValue('')
            evt.Skip()
            meserreur('START SERVEUR')
            return        

        if cara(ccmdstop) == False:

            self.tstopserv.SetValue('')
            evt.Skip()            
            meserreur('STOP SERVEUR')
            return        
                
        if cara(cbotname) == False:

            self.tbot.SetValue('')
            evt.Skip()
            meserreur('BOT ADMINISTRATION')
            return 
        
        if cara(cbotstart) == False:

            self.tstartbot.SetValue('')
            evt.Skip()
            meserreur('START BOT')
            return        

        if cara(cbotstop) == False:

            self.tstopbot.SetValue('')
            evt.Skip()            
            meserreur('STOP BOT')
            return    

        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        
        cfg.set(csection,"game",cgame)
        cfg.set(csection,"adresse",cadresse)
        cfg.set(csection,"port",cport)
        cfg.set(csection,"sshport",csshport)
        cfg.set(csection,"user",cuser)
        cfg.set(csection,"pwd",cpwd)
        cfg.set(csection,"rconpwd",crconpwd)
        cfg.set(csection,"cmdstart",ccmdstart)
        cfg.set(csection,"cmdstop",ccmdstop)
        cfg.set(csection,"botname",cbotname)
        cfg.set(csection,"botstart",cbotstart)
        cfg.set(csection,"botstop",cbotstop)

        cfg.write(open(self.file,'w'))

        texte = u"Serveur enregistrée avec succés"

        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy()
        
        self.Changetask(evt)

    def Clicknew(self, evt):
        
        if fexist('test.cfg') == True:

            os.remove('test.cfg')        
        

        section = []
        if (fexist(self.file) == False) or (testcfg(self.file) == False):

            section = "server1"

        if (fexist(self.file) == True) and (testcfg(self.file) == True):
            
            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            if len(cfg.sections())==0:

                section = "server1"
            
            else:
 
                n = 1
                section = "server%s"%(n)

                while section in cfg.sections():

                    n = n + 1
                    section = "server%s"%(n)     
        
        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        cfg.add_section(section)
        cfg.set(section,"game",self.cgame)
        cfg.set(section,"adresse",'')
        cfg.set(section,"port",'')
        cfg.set(section,"sshport",22)
        cfg.set(section,"user",'')
        cfg.set(section,"pwd",'')
        cfg.set(section,"rconpwd",'')
        cfg.set(section,"cmdstart",'')
        cfg.set(section,"cmdstop",'')
        cfg.set(section,"botname",'')
        cfg.set(section,"botstart",'')
        cfg.set(section,"botstop",'')

        cfg.write(open(self.file,'w'))

        texte = u"Nouveau Serveur ajouté avec succés"
        
        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy()

        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-GSControl")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Clickeff(self, evt):
        
        if self.testvide == 'vide':

            texte = u"Pas de Server à effacer !"
        
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()

            return        

        csection = self.server
        
        self.configs = self.configs.remove(self.tconfig.GetLabel())

        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        cfg.remove_section(csection)
        cfg.write(open(self.file,'w'))
        
        texte = u"Serveur éffacé avec succés"
        
        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy() 
        
        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-GSControl")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)


    def Quit(self, evt):

        if fexist('test.cfg') == True:

            os.remove('test.cfg')
        
        self.Destroy()
        self.frame=Myframe(titre="PB-GSControl")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame.SetIcon(icone)
       
        self.frame.Show(True)
        self.Show(False)

    def About(self, evt):

        description = """
UrT Serveurs Control            

( Python 2.7, wxPython )

Python Quake 3 Library
http://misc.slowchop.com/misc/wiki/pyquake3
Copyright (C) 2006-2007 Gerald Kaszuba
"""
       
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO))
        info.SetName('PB-GSControl')
        info.SetVersion('beta.2')
        info.SetDescription(description)
        info.SetCopyright('(C) 2012 PtitBigorneau')
        info.SetWebSite('http://www.ptitbigorneau.fr')
               
        wx.AboutBox(info)    

class Myframe(wx.Frame):

    cfgfile = "pb-gscontrol.cfg"
    bot = 0

    def __init__(self, titre):    
        
        wx.Frame.__init__(self, None, -1, title = titre, size=(850,670))
        
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):

        section = []
        if (fexist(self.cfgfile) == False) or (testcfg(self.cfgfile) == False):

            self.configs = ['']

            self.testvide = 'vide'
            self.cbotname = ''            
            self.sname = ''
            self.map = ''
            self.gametype = ''
            self.players = ''

            if fexist(self.cfgfile) == False:

                self.cstatus ='down.jpg'
            
            if testcfg(self.cfgfile) == False:
              
                self.cstatus ='down.jpg'            
            
        if (fexist(self.cfgfile) == True) and (testcfg(self.cfgfile) == True):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.cfgfile)

            section = cfg.sections()
 
            
            if len(cfg.sections())==0:

                self.configs = ['']

                self.sname = ''
                self.map = ''
                self.gametype = ''
                self.players = ''
                self.cbotname = ''
                self.cstatus ='down.jpg'
                
                self.testvide = 'vide'

            else:
 
                self.testvide = 'nonvide'
                
                for x in section:
              
                    namesection.append(x + ' - ' + cfg.get(x,"game")+ ' - ' +cfg.get(x,"adresse")+ ':' + cfg.get(x,"port"))
               
                self.configs = namesection
                self.server = section[0]
                self.cgame = cfg.get(section[0],"game")
                self.cadresse = cfg.get(section[0],"adresse")
                self.cport = cfg.get(section[0],"port")
                self.sshport = cfg.get(section[0],"sshport")
                self.cuser = cfg.get(section[0],"user")
                self.cpwd = cfg.get(section[0],"pwd")
                self.crconpwd = cfg.get(section[0],"rconpwd")
                self.ccmdstart = cfg.get(section[0],"cmdstart")
                self.ccmdstop = cfg.get(section[0],"cmdstop")
                self.cbotname = cfg.get(section[0],"botname")
                self.cbotstart = cfg.get(section[0],"botstart")
                self.cbotstop = cfg.get(section[0],"botstop")
                
                self.gadresse = self.cadresse + ":" + self.cport
                self.pwd = self.cpwd

                if testssh(self.cadresse, self.sshport, self.cuser, self.cpwd) == True:

                    self.ctestpwd = "ok"

                if testssh(self.cadresse, self.sshport, self.cuser, self.cpwd) == False:

                    self.ctestpwd = "Erreur"
                
                if self.cbotname != '':

                    self.bot = 1

                else:

                    self.bot = 0

                if testconnect(self.gadresse)==False:

                    self.cstatus ='down.jpg'
                    self.sname = self.gadresse
                    self.map =''
                    self.gametype =''
                    self.players =''
                    self.configs= namesection

                if testconnect(self.gadresse)==True:

                    q = PyQuake3(self.gadresse)
                    q.update()

                    self.cstatus ='up.jpg'

                    self.configs= namesection
                    self.games()
                    self.map = q.vars['mapname']

                    if len(self.map)> 20:

                        self.map = self.map[0:20]

                    if "&" in self.servername:

                        self.sname = self.servername = self.servername.replace('&','&&')

                    else:

                        self.sname = self.servername

                    if len(self.sname)> 25:

                        self.sname = self.sname[0:25]

        menuFichier = wx.Menu(style = wx.MENU_TEAROFF) 
        menuFichier.Append(wx.ID_OPEN, "&Configuration\tCtrl+C", "Configurer PB-gscontrol") 
        menuFichier.Append(wx.ID_EXIT, "&Quitter\tCtrl+Q", "Quitter PB-gscontrol") 

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT, "A propos","A propos de PB-gscontrol")

        menuBarre = wx.MenuBar() 
        menuBarre.Append(menuFichier, "&Fichier")
        menuBarre.Append(menuHelp, "?")

        self.barre = wx.StatusBar(self, -1) 
        self.barre.SetFieldsCount(2) 
        self.barre.SetStatusWidths([-1, -1]) 

        self.SetStatusBar(self.barre)

        self.SetMenuBar(menuBarre)        

        toolbar = self.CreateToolBar()
        toolbar.AddSeparator()
        toolbar.AddLabelTool(wx.ID_OPEN, '', wx.Bitmap('./conf.bmp'),shortHelp='Configuration', longHelp="Configurer PB-gscontrol")
        toolbar.AddSeparator()
        toolbar.AddLabelTool(wx.ID_EXIT, '', wx.Bitmap('./exit.bmp'),shortHelp='Quitter', longHelp="Quitter PB-gscontrol")
        toolbar.AddSeparator()
        toolbar.Realize()

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(10, 10)

        sizer = wx.GridBagSizer(6, 6) 

        font1 = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(9, wx.NORMAL, wx.NORMAL, wx.BOLD)
        font3 = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.BOLD)
        
        text1 = wx.StaticText(panel, label="PB-GSControl")
        sizer.Add(text1, pos=(0, 0),span=(1, 2), flag=wx.TOP|wx.LEFT, 
            border=20)
        text1.SetFont(font1)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('pb-gscontrol.gif'))
        sizer.Add(icon, pos=(0, 5),span=(2, 1), flag=wx.TOP|wx.RIGHT|wx.BOTTOM|wx.ALIGN_RIGHT, 
            border=10)

        text2 = wx.StaticText(panel, label='UrT Serveurs Control')
        sizer.Add(text2 , pos=(1, 0),span=(1, 2), flag=wx.LEFT, border=20)
        text2.SetFont(font2)
        

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 6), flag=wx.EXPAND|wx.BOTTOM, border=5)

        textconf = wx.StaticText(panel, label='SERVEUR',style=wx.ALIGN_CENTER)
        sizer.Add(textconf, pos=(4, 0),span=(1, 1), flag=wx.ALL|wx.EXPAND, border=10)
        textconf.SetFont(font2)

        self.tconfig = wx.ComboBox(panel,1,self.configs[0] , choices=self.configs, style=wx.CB_READONLY)
        sizer.Add(self.tconfig, pos=(4, 1),span=(1, 4),  flag=wx.TOP|wx.EXPAND, border=5)
        self.tconfig.SetFont(font3)       

        buttonact = wx.Button(panel,1, label="Actualiser")
        sizer.Add(buttonact, pos=(4, 5), flag=wx.TOP|wx.RIGHT, border=5) 

        texts = wx.StaticText(panel, label='STATUS',style=wx.ALIGN_CENTER)
        sizer.Add(texts, pos=(6, 0),span=(1, 1), flag=wx.TOP|wx.LEFT|wx.EXPAND, border=15)
        texts.SetFont(font2)

        textns = wx.StaticText(panel, label='              SERVEUR              ', style=wx.ALIGN_CENTER)
        sizer.Add(textns, pos=(6, 1),span=(1, 1), flag=wx.TOP|wx.LEFT|wx.EXPAND, border=15)
        textns.SetFont(font2)

        textm = wx.StaticText(panel, label='            MAP            ', style=wx.ALIGN_CENTER)
        sizer.Add(textm, pos=(6, 2),span=(1, 1), flag=wx.TOP|wx.LEFT|wx.EXPAND, border=15)
        textm.SetFont(font2)


        textg = wx.StaticText(panel, label=' GAMETYPE ', style=wx.ALIGN_CENTER)
        sizer.Add(textg, pos=(6, 3),span=(1, 1), flag=wx.TOP|wx.LEFT|wx.EXPAND, border=15)
        textg.SetFont(font2)

        textp = wx.StaticText(panel, label=' JOUEUR(S) ', style=wx.ALIGN_CENTER)
        sizer.Add(textp, pos=(6, 4),span=(1, 1), flag=wx.LEFT|wx.TOP, border=15)
        textp.SetFont(font2)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(7, 0), span=(1, 6), flag=wx.EXPAND)
   
        self.icon2 = wx.StaticBitmap(panel, bitmap=wx.Bitmap(self.cstatus))
        sizer.Add(self.icon2, pos=(8, 0),span=(1, 1), flag=wx.TOP|wx.ALIGN_CENTER|wx.LEFT, border=15)
        
        self.tservername = wx.StaticText(panel, label=self.sname)
        sizer.Add(self.tservername, pos=(8, 1),span=(1, 1), flag=wx.TOP|wx.LEFT, border=15)
        self.tservername.SetFont(font3)        

        self.tmap = wx.StaticText(panel, label=self.map)
        sizer.Add(self.tmap, pos=(8, 2),span=(1, 1), flag=wx.TOP|wx.ALIGN_CENTER|wx.LEFT, border=15)
        self.tmap.SetFont(font3)
        
        self.tgametype = wx.StaticText(panel, label=self.gametype)
        sizer.Add(self.tgametype, pos=(8, 3),span=(1, 1), flag=wx.TOP|wx.ALIGN_CENTER|wx.LEFT, border=15)
        self.tgametype.SetFont(font3)
        
        self.tplayers = wx.StaticText(panel, label=self.players)
        sizer.Add(self.tplayers, pos=(8, 4),span=(1, 1), flag=wx.TOP|wx.ALIGN_CENTER|wx.LEFT, border=15)
        self.tplayers.SetFont(font3)

        button2 = wx.Button(panel,2, label=u"Démarrer")
        sizer.Add(button2, pos=(8, 5),span=(1, 1), flag=wx.LEFT|wx.RIGHT, border=5)
        
        button3 = wx.Button(panel,3, label=u"Arrêter")
        sizer.Add(button3, pos=(9, 5),span=(1, 1), flag=wx.LEFT|wx.RIGHT, border=5) 

        self.titrebot = wx.StaticText(panel, label="  Bot Administration  ")
        sizer.Add(self.titrebot, pos=(11, 0), flag=wx.TOP|wx.LEFT|wx.ALIGN_CENTER, border=15)
      
        self.titrebot.SetFont(font2)        

        self.tbot = wx.StaticText(panel, label=self.cbotname)
        sizer.Add(self.tbot, pos=(11, 1), flag=wx.TOP|wx.LEFT, border=15)
        self.tbot.SetFont(font3)

        self.button4 = wx.Button(panel,4, label=u"Démarrer")
        sizer.Add(self.button4, pos=(11, 5),span=(1, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT, border=5)
        
        self.button5 = wx.Button(panel,5, label=u"Arrêter")
        sizer.Add(self.button5, pos=(12, 5),span=(1, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT, border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(14, 0), span=(1, 6), flag=wx.EXPAND, border=5)

        buttonr1 = wx.Button(panel,6, label="Status")
        sizer.Add(buttonr1, pos=(16, 1), flag=wx.LEFT|wx.RIGHT, border=15)

        buttonr2 = wx.Button(panel,7, label="Reload")
        sizer.Add(buttonr2, pos=(16, 2), flag=wx.ALIGN_RIGHT|wx.RIGHT, border=15) 

        buttonr3 = wx.Button(panel,8, label="Restart")
        sizer.Add(buttonr3, pos=(16, 3), flag=wx.RIGHT, border=15) 

        buttonr4 = wx.Button(panel,9, label="Cyclemap")
        sizer.Add(buttonr4, pos=(16, 4), flag=wx.RIGHT, border=15)

        buttonr5 = wx.Button(panel,10, label="Map")
        sizer.Add(buttonr5, pos=(16, 5), flag=wx.RIGHT, border=15)

        tcmdrcon = wx.StaticText(panel, label="  Commande Rcon : ")
        sizer.Add(tcmdrcon, pos=(17, 0), flag=wx.TOP|wx.LEFT|wx.ALIGN_CENTER, border=15)
        tcmdrcon.SetFont(font2)       

        self.cmdrcon = wx.TextCtrl(panel, value='')
        sizer.Add(self.cmdrcon, pos=(17, 1), span=(1, 4),flag=wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, border=15)

        buttonrcon = wx.Button(panel,11, label="Envoyer")
        sizer.Add(buttonrcon, pos=(17, 5), flag=wx.TOP|wx.RIGHT, border=15) 

        sizer.AddGrowableCol(5)
        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#f0f0f0")
        
        wx.EVT_MENU(self, wx.ID_EXIT, self.Quit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.About)
        wx.EVT_MENU(self, wx.ID_OPEN, self.Configuration)
        self.Bind(wx.EVT_BUTTON, self.Changeserv, id=1)
        self.Bind(wx.EVT_BUTTON, self.Startserv, id=2)
        self.Bind(wx.EVT_BUTTON, self.Stopserv, id=3)
        self.Bind(wx.EVT_BUTTON, self.Startbot, id=4)
        self.Bind(wx.EVT_BUTTON, self.Stopbot, id=5)
        self.Bind(wx.EVT_BUTTON, self.Envoisstatus, id=6)
        self.Bind(wx.EVT_BUTTON, self.Envoisreload, id=7)
        self.Bind(wx.EVT_BUTTON, self.Envoisrestart, id=8)
        self.Bind(wx.EVT_BUTTON, self.Envoisnextmap, id=9)
        self.Bind(wx.EVT_BUTTON, self.Envoismap, id=10)
        self.Bind(wx.EVT_BUTTON, self.Envoisrcon, id=11)
        self.Bind(wx.EVT_COMBOBOX, self.Changeserv)

        if self.cbotname == '':

            self.bot = 0
            self.titrebot.SetLabel('')
            self.tbot.SetLabel('')
            self.button4.Hide()
            self.button5.Hide()


    def Configuration(self, evt):

        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-GSControl")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Changeserv(self, evt):

        selec = self.tconfig.GetSelection()
         
        if (fexist(self.cfgfile) == True) and (testcfg(self.cfgfile) == True)and (self.testvide != 'vide'):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.cfgfile)
            section = cfg.sections()
              
            for x in section:
              
                namesection.append(x + ' - ' + cfg.get(x,"game")+ ' - ' +cfg.get(x,"adresse")+ ':' + cfg.get(x,"port"))
               
            self.server = section[int(selec)]
            self.cgame = cfg.get(section[int(selec)],"game")
            self.cadresse = cfg.get(section[int(selec)],"adresse")
            self.cport = cfg.get(section[int(selec)],"port")
            self.sshport = cfg.get(section[int(selec)],"sshport")
            self.cuser = cfg.get(section[int(selec)],"user")
            self.cpwd = cfg.get(section[int(selec)],"pwd")
            self.crconpwd = cfg.get(section[int(selec)],"rconpwd")
            self.ccmdstart = cfg.get(section[int(selec)],"cmdstart")
            self.ccmdstop = cfg.get(section[int(selec)],"cmdstop")
            self.cbotname = cfg.get(section[int(selec)],"botname")
            self.cbotstart = cfg.get(section[int(selec)],"botstart")
            self.cbotstop = cfg.get(section[int(selec)],"botstop")
            self.gadresse = self.cadresse + ":" + self.cport
            self.pwd = self.cpwd

            if testssh(self.cadresse, self.sshport, self.cuser, self.cpwd) == True:

                self.ctestpwd = "ok"


            if testssh(self.cadresse, self.sshport, self.cuser, self.cpwd) == False:

                self.ctestpwd = "Erreur"

              
            if self.cbotname == '':

                self.bot = 0
                self.titrebot.SetLabel('')
                self.tbot.SetLabel('')
                self.button4.Hide()
                self.button5.Hide()
                evt.Skip()

            if self.cbotname != '':

                self.bot = 1
                self.titrebot.SetLabel("  Bot Administration  ")
                self.button4.Show()
                self.button5.Show()
                evt.Skip()                  
                
            if testconnect(self.gadresse)==False:

                self.cstatus ='down.jpg'
                self.sname = self.gadresse
                self.map =''
                self.gametype =''
                self.players =''
                self.configs=namesection

            if testconnect(self.gadresse)==True:

                q = PyQuake3(self.gadresse)
                q.update()

                self.cstatus ='up.jpg'


                self.configs = namesection

                self.games()

                self.map = q.vars['mapname']

                if len(self.map)> 20:

                    self.map = self.map[0:20]

                if "&" in self.servername:

                    self.sname = self.servername = self.servername.replace('&','&&')

                else:

                    self.sname = self.servername

                if len(self.sname)> 25:

                    self.sname = self.sname[0:25]
  
            self.icon2.SetBitmap(wx.Bitmap(self.cstatus))       
            self.tservername.SetLabel(self.sname)
            self.tmap.SetLabel(self.map)
            self.tgametype.SetLabel(self.gametype)
            self.tplayers.SetLabel(self.players)
            self.tbot.SetLabel(self.cbotname)
            evt.Skip()

        return

    def Quit(self, evt):

        self.Destroy()

    def About(self, evt):

        description = """
UrT Serveurs Control            

( Python 2.7, wxPython )

Python Quake 3 Library
http://misc.slowchop.com/misc/wiki/pyquake3
Copyright (C) 2006-2007 Gerald Kaszuba
"""
       
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO))
        info.SetName('PB-GSControl')
        info.SetVersion('beta.2')
        info.SetDescription(description)
        info.SetCopyright('(C) 2012 PtitBigorneau')
        info.SetWebSite('http://www.ptitbigorneau.fr')
               
        wx.AboutBox(info)                

    def games(self):

        q = PyQuake3(self.gadresse)
        q.update()

        if self.cgame == 'urt':

            self.servername = q.vars['sv_hostname']
            self.gametype = q.vars['g_gametype']

            if self.gametype == '3':

                self.gametype='TDM'
    
            if self.gametype == '4':

                self.gametype='TS'
    
            if self.gametype == '7':

                self.gametype='CTF'
    
            if self.gametype == '8':

                self.gametype='BOMB'
    
            if (self.gametype == '0') or (self.gametype == '2'):

                self.gametype='FFA'

            if (self.gametype == '1'):

                self.gametype='LMS'

            if self.gametype == '5':

                self.gametype='FTL'
    
            if self.gametype == '6':
 
                self.gametype='CandH'

            self.slots = int(q.vars['sv_maxclients']) - int(q.vars['sv_privateClients'])
            self.players = "%s / %s"%(len(q.players), self.slots)
            
        if self.cgame == 'trem':

            self.servername = q.vars['sv_hostname']
            self.gametype = ''
            self.slots = q.vars['sv_maxclients']
            self.players = "%s / %s"%(len(q.players), self.slots)
            
        self.servername = self.servername.replace('^1','')
        self.servername = self.servername.replace('^2','')
        self.servername = self.servername.replace('^3','')
        self.servername = self.servername.replace('^4','')
        self.servername = self.servername.replace('^5','')
        self.servername = self.servername.replace('^6','')
        self.servername = self.servername.replace('^7','')
        self.servername = self.servername.replace('^8','')
        self.servername = self.servername.replace('^9','')
        self.servername = self.servername.replace('^0','')
        self.servername = self.servername.replace('^','')

        return

    def Startserv(self, evt):

        if (self.sname != self.gadresse) and (self.map !=''):

            dlg = wx.MessageDialog(self, u"Serveur déjà en_ligne !" , style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return
        
        self.cmd =  self.ccmdstart

        self.texte = u"Serveur %s démarré avec succés"%(self.sname)

        self.envoiscmd(evt)    

    def Stopserv(self, evt):
                 
        if (self.sname == self.gadresse) and (self.map ==''):

            dlg = wx.MessageDialog(self, u"Serveur hors_ligne !" , style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return

        self.cmd =  self.ccmdstop
        self.texte = u"Serveur %s arrêté avec succés"%(self.sname)

        self.envoiscmd(evt)

    def Startbot(self, evt):
        
        self.cmd =  self.cbotstart
        self.texte = u"Bot %s démarré avec succés"%(self.cbotname)

        self.envoiscmd(evt)    

    def Stopbot(self, evt):
 
        self.cmd =  self.cbotstop
        self.texte = u"Bot %s arrêté avec succés"%(self.cbotname)

        self.envoiscmd(evt) 

    def envoiscmd(self, evt):
        
        if self.ctestpwd=="":
            
            return        

        if (self.testvide == 'vide') or (self.ctestpwd=="Erreur"):
            
            dlg = wx.MessageDialog(self, "Erreur connexion !" , style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return

        cmd1 = self.cmd
        host1 = self.cadresse
        port1= self.sshport
        user1 = self.cuser        
        pwd1 = self.cpwd
        
        texte = self.texte
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if cmd1 !='':
        
            try:
 
                ssh.connect(host1, int(port1), username=user1, password=pwd1, timeout=1)

                ssh.exec_command(cmd1)
            
            finally:

                ssh.close()
                 
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()
        
            
            self.Changeserv(evt)


    def Envoisrcon(self, evt):
        
        self.rconcmd = self.cmdrcon.GetLabel()

        if cara(self.rconcmd) == False:
        
            texte = u"Valeur Non Valide !"
        
            dlg = wx.MessageDialog(self, texte, "Erreur !",style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            self.cmdrcon.SetLabel('')
            evt.Skip()

            return

        if self.rconcmd == 'status':

            self.Envoisstatus(evt) 

        elif self.rconcmd != '':

            self.texte = u'Commande rcon "%s" exécutée avec succés'%(self.rconcmd)

            self.rcon(evt) 
    
    def Envoisreload(self, evt):
        
        self.rconcmd = 'reload'

        self.texte = u'Commande rcon "%s" exécutée avec succés'%(self.rconcmd)

        self.rcon(evt)

    def Envoisrestart(self, evt):
        
        self.rconcmd = 'restart'

        self.texte = u'Commande rcon "%s" exécutée avec succés'%(self.rconcmd)

        self.rcon(evt)

    def Envoisnextmap(self, evt):
        
        self.rconcmd = 'cyclemap'

        self.texte = u'Commande rcon "%s" exécutée avec succés'%(self.rconcmd)

        self.rcon(evt)

    def Envoismap(self, evt):
        
        addtache = wx.TextEntryDialog(self, u'Map : ', u'Nouvelle Map')
        addtache.ShowModal()
        self.ccmap = addtache.GetValue()
               
        if cara(self.ccmap) == False:
        
            texte = u"Valeur Non Valide !"
        
            dlg = wx.MessageDialog(self, texte, "Erreur !", style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return
           
        if self.ccmap != '':

            self.texte = u'Map "%s" changée avec succés'%(self.ccmap)
            
            self.rconcmd = 'map ' + self.ccmap

            self.rcon(evt) 
        
    def rcon(self, evt):

        pwdrcon = self.crconpwd
        adresse = self.cadresse + ":" + self.cport
        
        if testpwdrcon(adresse, pwdrcon) == True:

            q = PyQuake3(adresse, rcon_password = pwdrcon)
            q.rcon(str(self.rconcmd))

            dlg = wx.MessageDialog(self, self.texte, style = wx.OK)
            retour = dlg.ShowModal()
            self.cmdrcon.SetLabel('')
            evt.Skip()
            
            self.Changeserv(evt)

        else:

            dlg = wx.MessageDialog(self, 'ERREUR RCON !', "Erreur !",style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy()
       
    def Envoisstatus(self, evt):

        pwdrcon = self.crconpwd
        adresse = self.cadresse + ":" + self.cport
        
        if testpwdrcon(adresse, pwdrcon) == True:
            
            q = PyQuake3(adresse, rcon_password = pwdrcon)
            q.rcon_update()
            data = q.listplayers
            lines = data.split('\n')
            players = lines[3:]
        
            message = '\n'

            for line in players:

                if line !='':
        
                    ligne = line.split()
        
                    num = ligne[0]
                    score = ligne[1]
                    ping = ligne[2]
                    adresse = ligne[-3:]
                    adresse = adresse[0].split(':')
                    name = ligne[3]
                    
                    name = name.replace('^1','')
                    name = name.replace('^2','')
                    name = name.replace('^3','')
                    name = name.replace('^4','')
                    name = name.replace('^5','')
                    name = name.replace('^6','')
                    name = name.replace('^7','')
                    name = name.replace('^8','')
                    name = name.replace('^9','')
                    name = name.replace('^0','')
                    name = name.replace('^','')

                    ip=adresse[0]
                
                    message = message + name + '   Num : ' + num + '   Score : ' + score + '   Ping : ' + ping + '   IP : ' + ip +'\n'
            

            dlg = wx.lib.dialogs.ScrolledMessageDialog(self, message, "Status")
            retour = dlg.ShowModal()
            dlg.Destroy()
            
        else:

            dlg = wx.MessageDialog(self, 'ERREUR RCON !', "Erreur !",style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy()
 
if __name__ == '__main__':

    app = wx.App()
    frame=Myframe(titre="PB-GSControl")
    icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

    frame.SetIcon(icone)
    frame.Show()

    app.MainLoop()
