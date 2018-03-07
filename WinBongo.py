# -*- coding: utf-8 -*-

#WinBongo.py   D.Senciall  April 2015
# update June 1 2015 to fix incorrect pressure conversion in realtime data reader for std-12
"""
Elements BASED ON CODE SAMPLE FROM: matplotlib-with-wxpython-guis by E.Bendersky
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 31.07.2008

seee   http://eli.thegreenplace.net/2008/08/01/matplotlib-with-wxpython-guis/

Also
 Code Borrowed from seawater-3.3.2-py.27.egg for the density calcuations
"""
import os
import pprint
import random
import sys
import wx

import time
import serial
import datetime

#import WINAQU_GUI_BONGO

# The recommended way to use wx graphics and matplotlib (mpl) is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
#from mpl_toolkits.axes_grid.parasite_axes import HostAxes, ParasiteAxes   DEPRECIATED
from mpl_toolkits.axes_grid1.parasite_axes import HostAxes, ParasiteAxes
#from mpl_toolkits.axes_grid.parasite_axes import SubplotHost, ParasiteAxes
import matplotlib.pyplot as plt
import numpy as np
# import pylab

import wxSerialConfigDialog_NAFC as wxSerialConfigDialog
import wxTerminal_NAFC
#import wxTerminal_NAFC

ID_START_RT = wx.NewId()
ID_STOP_RT = wx.NewId()
ID_START_ARC = wx.NewId()
ID_STOP_ARC = wx.NewId()
ID_SER_CONF = wx.NewId()

VERSION = "V2.0 March 2018"
TITLE = "WinBongo"
DEFAULT_COM = "COM8"
DEFAULT_BAUD = 1200
DEFAULT_RATE = 1   # scans per second

SIMULATOR = False

###########################################################################
# READS DATA FROM A FILE :PASS 1 LINE at a atime back via the next method

class DataGen2(object):
    def __init__(self, FileName,init=50):
        self.data = self.init = init
        self.Convert=ConvertClass()
#        self.temp = 0.0
        self.FileName = FileName
        self.f = open(self.FileName,"r")
        self.scannum=0
        self.scan = dict()

        self.readheader()

    def next(self):
        text=self.f.readline()

        if text =="" :
            self.scan["OK"] = False
            return(self.scan)
        else :
            self.scannum+=1
            line = text.split()
            scan = self.Convert.convert_simulation_b95(line)
#            scan = self.Convert.convert_archived(line)
            scan["Et"]=str(self.scannum * DEFAULT_RATE)

            return (scan)

    def readheader(self):

            text=self.f.readline()
            text=self.f.readline()
            text=self.f.readline()
            text=self.f.readline()
            text=self.f.readline()
            text=self.f.readline()
                                                                

    def flush(self):    #dummy
        return()
    
    def close_infile(self):
        self.f.close()

########################################################################################
#  SERIAL PORT STD READER CLASS
# non threaded version  reads data from port when asked via next method
#initialization
#
# for linux
# ser.port = "/dev/ttyS2"
# for windows
# ser.port ="COM1"
#
# Possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
#
#ser.timeout = None          #blocking read when using radline
#ser.timeout = 0             #non-block read
########################################################################################
class SerialSource_STD12():
     
    def __init__(self,parent,serial):
        self.parent = parent                # needed to call the flash status bar method of Graphframe
        self.ser = serial
        self.StartTime = 0
        self.set_default()
        self.Convert=ConvertClass()
        self.scan = dict()
        
    def set_default (self):
        self.ser.port = DEFAULT_COM
        self.ser.baudrate = DEFAULT_BAUD
        self.ser.bytesize = serial.EIGHTBITS    #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE    #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        self.ser.timeout = 5                    #timeout block read
        self.ser.xonxoff = True                 #disable software flow control
        self.ser.rtscts = False                 #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False                 #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2               #timeout for write

    def open_Port(self):
        try: 
          self.ser.open()
        except Exception as e:
#          print "error open serial port: "+self.ser.port+" " + str(e)
          return(False)
        self.parent.flash_status_message("PORT OPEN "+self.ser.getPort())

        return (True)

    def flush (self):
        self.ser.flushInput()
        line = self.ser.readline()  # ensure a full line is in buffer by discarding any stub

    def next(self):

        if self.StartTime == 0:
            self.StartTime = time.time()
            
        text = self.ser.readline()
        if text == "":              # this is due to Cr-Lf show as 2 lines which requires the (LF)to be flushed
           text = self.ser.readline()

        if text =="" :
            self.scan["OK"] = False
            return(self.scan)
        else :
            line = text.split()
            if SIMULATOR :
             scan = self.Convert.convert_simulation_b95(line)
#             scan = self.Convert.convert_archived(line)
             scan["Et"]= str(time.time() - self.StartTime)             
            else:
             scan = self.Convert.convert_STD12_raw(line)

        return (scan)

    def send_wake(self):
        self.parent.flash_status_message("WAKING STD")
        self.ser.write("\r\r\r")
        print("WAKE= " + self.ser.readline())
        
    def send_Real(self):

        self.send_wake()
        self.parent.flash_status_message("SENDING REAL")
        self.ser.write("REAL\r")
        self.ser.readline()     # echo plus Cr-Lf which requires the 2nd read
        self.ser.readline()
        time.sleep(1.0)

    def send_Start_Data(self):
        self.send_wake()
        self.ser.write("M\r")
        time.sleep(2.0)
        self.flush()
        self.parent.flash_status_message("STD DATA STARTED")

    def send_Stop_Data(self) :
        self.ser.write ("\r")
        self.flush()
        self.parent.flash_status_message("STD DATA STOPPED")

    def send_Set_DataRate(self,rate):
        self.parent.flash_status_message("SETTING STD DATA RATE = "+ rate+" SCANS PER SECOND")
        self.ser.write("SET S "+rate+"\r")
        self.ser.readline()

    def close_Port(self):
        self.parent.flash_status_message("PORT CLOSSING")
        self.ser.close()

    def is_port_open(self):
        return (self.ser.isOpen())
    
#*** END OF SerialSource_STD12 Class ******************
#*******************************************  SBE19PLUS *********************************************
class SerialSource_SBE19p():

    def __init__(self, parent, serial):
        self.parent = parent  # needed to call the flash status bar method of Graphframe
        self.ser = serial
        self.StartTime = 0
        self.set_default()
        self.Convert = ConvertClass()
        self.scan = dict()

    def set_default(self):
        self.ser.port = DEFAULT_COM
        self.ser.baudrate = DEFAULT_BAUD
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        self.ser.timeout = 5  # timeout block read
        self.ser.xonxoff = True  # disable software flow control
        self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2  # timeout for write

    def open_Port(self):
        try:
            self.ser.open()
        except Exception as e:
            print ("error open serial port: "+self.ser.port+" " + str(e))
            return (False)
#        self.parent.flash_status_message("PORT OPEN " + self.ser.getPort())

        return (True)

    def flush(self):
        self.ser.flushInput()
        line = self.ser.readline()  # ensure a full line is in buffer by discarding any stub

    def next(self):

        if self.StartTime == 0:
            self.StartTime = time.time()

        text = self.ser.readline()
        if text == "":  # this is due to Cr-Lf show as 2 lines which requires the (LF)to be flushed
            text = self.ser.readline()

        if text == "":
            self.scan["OK"] = False
            return (self.scan)
        else:
            print (text)
            line = text.split(',')
            if SIMULATOR:
                scan = self.Convert.convert_simulation_b95(line)
                #             scan = self.Convert.convert_archived(line)
                scan["Et"] = str(time.time() - self.StartTime)
            else:
                scan = self.Convert.convert_SBE19p_raw(line)
        return (scan)
    #################
    def Send_Wake(self):

        if self.ser.isOpen():
            try:
                self.ser.flushInput()  # flush input buffer, discarding all its contents
                self.ser.flushOutput()  # flush output buffer, aborting current output

                # and discard all that is in buffer

                # write data
                self.ser.write("\r")
                print("write data: CR CR CR")
                response = ""
                status = ""
                trys = 0
                sleeps = 0
                MAX_TRYS = 5
                while (response != "S>\r\n") and (trys <= MAX_TRYS):
                    #              self.ser.flushInput() #flush input buffer, discarding all its contents
                    self.ser.write("\r")
                    time.sleep(0.1)
                    while (self.ser.inWaiting() < 4) and (sleeps < MAX_TRYS):
                        time.sleep(0.5)
                        sleeps += 1

                    if (sleeps < MAX_TRYS):
                        response = self.ser.readline()
                    sleeps = 0

                    trys += 1

                self.ser.flushInput()  # flush input buffer, discarding all its contents

                if (trys > MAX_TRYS):
                    status = "FAIL: CAN NOT AWAKEN AFTER " + str(trys) + " TRYS : CHECK PORT,CABLES & SWITCHES"
                else:
                    status = "PASS: CTD AWAKE"

                print("awake " + status + response + " " + str(trys))

            except Exception as e1:
                print (                "error communicating...: " + str(e1))
                status = "FAIL: Error COMMUNICATING ON WAKEUP: CHECK SERIAL PORT#/ADAPTER " + self.ser.port

        else:
            print ("cannot open serial port " + self.ser.port)
            status = "FAIL: PORT NOT OPEN: CHECK SERIAL PORT#/ADAPTER" + self.ser.port
        return status



    def send_Real(self):
        self.parent.flash_status_message("SETTING CTD TO REAL TIME")
        self.parent.flash_status_message("SENDING IGNORESWITCH")
        self.ser.write("IGNORESWITCH=Y\r")
        print (self.ser.readline())  # echo plus Cr-Lf which requires the 2nd read
#        self.ser.readline()
        self.parent.flash_status_message("SENDING OUTPUTFORMAT=3")
        self.ser.write("OUTPUTFORMAT=3\r")
        print (self.ser.readline())  # echo plus Cr-Lf which requires the 2nd read
#        self.ser.readline()
        self.parent.flash_status_message("SENDING OUTPUTSAL")
        self.ser.write("OUTPUTSAL=Y\r")
        print (self.ser.readline())  # echo plus Cr-Lf which requires the 2nd read
#        self.ser.readline()
#        self.ser.write("OUTPUTUCSD=Y\r")
#        self.ser.readline()  # echo plus Cr-Lf which requires the 2nd read
#        self.ser.readline()

        time.sleep(1.0)

    def send_Start_Data(self):
        self.ser.write("STARTNOW\r")
        print (self.ser.readline())
        time.sleep(1.0)
        self.flush()
        self.parent.flash_status_message("CTD DATA STARTED")

    def send_Stop_Data(self):
        self.ser.write("STOP\r")
        print ("SENDING STOP")
        print (self.ser.readline())
        self.flush()
        self.parent.flash_status_message("CTD DATA STOPPED")

    def send_Clear_Data(self):
        self.ser.write("INITLOGGING\r")
        print (self.ser.readline())
        self.flush()
        self.parent.flash_status_message("CTD MEMORY CLEARED")

    def send_Set_DataRate(self, rate):
        avg = str(rate*4)
        self.parent.flash_status_message("SETTING CTD DATA RATE = " + rate + " SCANS PER SECOND")
        self.ser.write("NAVG=" + '4' + "\r")
        self.ser.readline()

    def close_Port(self):
        self.parent.flash_status_message("RESETTING CTD TO SELF CONTAINED")
        self.ser.write("IGNORESWITCH=N\r")
        self.ser.readline()  # echo plus Cr-Lf which requires the 2nd read
        self.ser.readline()
        self.ser.write("OUTPUTFORMAT=0\r")
        self.ser.readline()  # echo plus Cr-Lf which requires the 2nd read
        self.ser.readline()

        self.parent.flash_status_message("PORT CLOSSING")
        self.ser.close()

    def is_port_open(self):
        return (self.ser.isOpen())


# *** END OF SerialSource_SBE19p Class ******************
## smoothed rate over Avg_interval scans
    
class SmoothRate(object):
    def __init__(self,interval):
        self.Avg_interval = interval
        self.rolling_list =  l = [0.0] * self.Avg_interval
        self.n = 0
        self.OldPres = 0.0
        self.PSum =0.0

    def get_rate(self,pres):
           self.n = (self.n  + 1)% self.Avg_interval  
           deltaP = pres - self.OldPres
           self.PSum = self.PSum + deltaP - self.rolling_list[self.n]
           the_rate = (60. *self.PSum/self.Avg_interval)
#           print self.n,pres,self.OldPres,deltaP, self.PSum,self.Avg_interval, Rstr          
           self.rolling_list[self.n] = deltaP
           self.OldPres = pres  
           return (the_rate)
#*** END of SmoothRate Class ******************************

        

    
class RollingDialBox(wx.Panel):
    """ Displays the realtime data values, even when graph is paused. size = 50 for most
    """
    def __init__(self, parent, ID, label, initval,size):
        wx.Panel.__init__(self, parent, ID)
        
        self.value = initval

        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

              
        self.Data_text = wx.TextCtrl( self, wx.ID_ANY, self.value, wx.DefaultPosition,
            wx.Size( size,-1 ), wx.TE_READONLY )
        self.Data_text.SetMaxLength( 8 ) 
        self.Data_text.SetFont( wx.Font( 10, 74, 90, 92, False, "Arial" ) )

        sizer.Add(self.Data_text, 0, wx.ALL, 10)        
        
        self.SetSizer(sizer)
        sizer.Fit(self)
#*** END of RollingDial Box Class **************************

class BoundControlBox(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a 
        manual mode with an associated value.
    """
    def __init__(self, parent, ID, label, initval,start_val):
        wx.Panel.__init__(self, parent, ID)
        
        self.value = initval
        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        if (start_val == 0) :        
            self.radio_auto = wx.RadioButton(self, -1, 
                label="Auto " +"("+initval+")", style=wx.RB_GROUP)
        else :
            self.radio_auto = wx.RadioButton(self, -1, 
                label="Auto", style=wx.RB_GROUP)
            
        self.radio_manual = wx.RadioButton(self, -1,
            label="Manual")
        self.manual_text = wx.TextCtrl(self, -1, 
            size=(35,-1),
            value=str(initval),
            style=wx.TE_PROCESS_ENTER)
             
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)
        
        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)

   
        sizer.Add(self.radio_auto, 0, wx.ALL, 10)
        sizer.Add(manual_box, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.radio_manual.SetValue(start_val)  # 1 is manual enabled, 0 is auto enabled
    
    def on_update_manual_text(self, event):
        self.manual_text.Enable(self.radio_manual.GetValue())
    
    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()
    
    def is_auto(self):
        return self.radio_auto.GetValue()
        
    def manual_value(self):
        return self.value
    
#*** End of Rolling DialBoxClass *************************************

####################################################################
#   GraphFrame  -  Build the main frame of the application
#####################################################################
class GraphFrame(wx.Frame):

    title = TITLE +" "+VERSION
   
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)

        self.ser = serial.Serial()  # Create a serial com port access instance
        CTD = "SBE"

        print ("HELLO")

        if (CTD == "STD"):
            self.SSource = SerialSource_STD12(self, self.ser)
        elif (CTD == "SBE"):
            self.SSource = SerialSource_SBE19p(self, self.ser)


        self.SSource.set_default()
        self.Serial_In = None
        
        self.SRate = SmoothRate(5)  # Create a rate smoother instance

        self.port_open = False
        self.DataSource = None

# Some state variables
        self.GraphRun = False
        self.MonitorRun = False

        self.RT_source = False
        self.ARC_source = False
        self.runlogfile=""
        self.LogFileName ="Not Logging"


        self.hd1=dict(SHIP="XX",TRIP="YYY",STN="000")
        self.hship = "YY"
# some default scales
        self.ymin= -200.0
        self.Dslope = 20.0
        self.Uslope = 10.0
        self.StartTime = 0
        self.ScanNum = 0
        
        SlopeTime1 = (self.ymin/self.Dslope)*-60.0
        SlopeTime2 = SlopeTime1+(self.ymin/self.Uslope)*-60.0
        
        self.SlopeLineX = np.array([0.0,SlopeTime1,SlopeTime2])
        self.SlopeLineY = np.array([0.0,self.ymin,0.0])

# storage for the data
        self.data = dict(Pres=[0],Temp=[0],Cond=[0],Sal=[0],F1=[0],F2=[0],L=[0],V=[0],Rate=[0],Et=[0])

# Build the display       
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()

# the redraw timer is used to add new data to the plot and update any changes via
# the on_redraw_timer method
#10 ms; if you call at slower rate (say 100ms)the manual scale box entries don't respond well
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(10)

#**************************** End of GraphFrame Init **********************
#*** GraphFrame Methods ***************************************************

    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_ser_config = menu_file.Append(ID_SER_CONF, "Serial Config", "Serial Config")
        self.Bind(wx.EVT_MENU, self.on_ser_config, m_ser_config)
        menu_file.AppendSeparator()
        m_term = menu_file.Append(-1, "Launch Terminal", "Terminal")
        self.Bind(wx.EVT_MENU, self.on_term, m_term)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        menu_realtime = wx.Menu()
        m_rtstart = menu_realtime.Append(ID_START_RT, "Start", "Start realtime data")
        self.Bind(wx.EVT_MENU, self.on_start_rt, m_rtstart)
        menu_realtime.AppendSeparator()
        m_rtstop = menu_realtime.Append(ID_STOP_RT, "End", "End realtime data")
        self.Bind(wx.EVT_MENU, self.on_stop_rt, m_rtstop)

        menu_archived = wx.Menu()
        m_arcstart = menu_archived.Append(ID_START_ARC, "Start", "Start archived data")
        self.Bind(wx.EVT_MENU, self.on_start_arc, m_arcstart)
        menu_archived.AppendSeparator()
        m_arcstop = menu_archived.Append(ID_STOP_ARC, "End", "End archived data")
        self.Bind(wx.EVT_MENU, self.on_stop_arc, m_arcstop)

        menu_option = wx.Menu()
        m_basehead = menu_option.Append(-1, "Set ship trip stn", "shiptripstn")
        self.Bind(wx.EVT_MENU, self.on_set_base_header, m_basehead)
        menu_option.AppendSeparator()
        m_edithead = menu_option.Append(-1, "Edit File Header", "Edit File Header")
        self.Bind(wx.EVT_MENU, self.on_edit_head, m_edithead)
        menu_option.AppendSeparator()
        menu_option.AppendSeparator()
        self.cb_grid = menu_option.Append (-1,"Ghow Grid","Grid",kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.on_cb_grid, self.cb_grid)
#        m_grid.SetValue(True) need syntax ??

        menu_help = wx.Menu()
#        m_help = menu_help.Append(-1, "help", "help")
#        self.Bind(wx.EVT_MENU, self.on_help, m_help)
#        menu_help.AppendSeparator()
        m_about = menu_help.Append(-1, "About", "About WinBongo")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_realtime, "RealTime")
        self.menubar.Append(menu_archived, "Archived")
        self.menubar.Append(menu_option, "Options")
        self.menubar.Append(menu_help,"Help")
        self.SetMenuBar(self.menubar)

        self.cb_grid.Check(True)
        m_rtstop.Enable(False)
        m_arcstop.Enable(False)
        m_term.Enable (False)  # leave off for now
        m_basehead.Enable(False)

# ***********************************************************************************
    def create_main_panel(self):
        
        self.panel = wx.Panel(self)  # Create a Panel instance

# The Plot-  init_pot sets up the MatPlotLib graph
        self.init_plot()
        
# Create a Canvas
        self.canvas = FigCanvas(self.panel, -1, self.fig)

# Build the basic controls and buttons
        self.xmax_control = BoundControlBox(self.panel, -1, "Time (sec)", '1800',0)
        self.ymin_control = BoundControlBox(self.panel, -1, "Max Depth (m)", '-200',1)

        self.tmin_control = BoundControlBox(self.panel, -1, "T min", '-2',1)
        self.tmax_control = BoundControlBox(self.panel, -1, "T max", '10',1)
        
        self.DownSlope_control = BoundControlBox(self.panel, -1, "Descent Slope m/min",'20',0)
        self.UpSlope_control = BoundControlBox(self.panel, -1, "Ascent Slope m/min", '10',0)

        self.et_text = RollingDialBox(self.panel, -1, "ET (secs)", '0',50)          
        self.r_text = RollingDialBox(self.panel, -1, "Rate (m/min)", '0',50)     
     
        self.GraphRun_button = wx.Button(self.panel, -1, "Start Graph/Logging")
        self.Bind(wx.EVT_BUTTON, self.on_GraphRun_button, self.GraphRun_button)

        self.monitor_button = wx.Button(self.panel, -1, "Start CTD Monitor")
        self.Bind(wx.EVT_BUTTON, self.on_monitor_button, self.monitor_button)

        self.monitor_button.Enable(False)
        self.GraphRun_button.Enable(False)
        
# Row 0 - the data monitor display
        self.hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.t_text = RollingDialBox(self.panel, -1, u"Temp (°C)", '0',50)
        self.p_text = RollingDialBox(self.panel, -1, "Pres (dB)", '0',50)
        self.c_text = RollingDialBox(self.panel, -1, "Cond  (S/m)", '0',50)
        self.s_text = RollingDialBox(self.panel, -1, "Sal ((PSU)", '0',50)
        self.d_text = RollingDialBox(self.panel, -1, "Sigma-t", '0',50)
        self.f1_text = RollingDialBox(self.panel, -1, "Flow1 ()", '0',50)
        self.f2_text = RollingDialBox(self.panel, -1, "Flow2 ()", '0',50)
        self.l_text = RollingDialBox(self.panel, -1, "Light ()", '0',50)
        self.v_text = RollingDialBox(self.panel, -1, "Batt. Volts", '0',50)

        self.hbox0.Add(self.p_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.t_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.c_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.s_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.d_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.f1_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.f2_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.l_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.Add(self.v_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox0.AddSpacer(20)
        
# Row 1   - buttoms and rate     
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.ctd_clock_text = RollingDialBox(self.panel, -1, "CTD Clock", '0',60)
       
        self.hbox1.Add(self.monitor_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(2)
        self.hbox1.Add(self.GraphRun_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.et_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.r_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.ctd_clock_text, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
# Row 2  - scaling controls
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.hbox2.Add(self.xmax_control, border=5, flag=wx.ALL)
        self.hbox2.AddSpacer(10)
        self.hbox2.Add(self.ymin_control, border=5, flag=wx.ALL)
        self.hbox2.AddSpacer(10)
        self.hbox2.Add(self.tmin_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.tmax_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.DownSlope_control, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox2.AddSpacer(10)
        self.hbox2.Add(self.UpSlope_control, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox2.AddSpacer(10) 

# Put it all together
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)        
        self.vbox.Add(self.hbox0, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox2, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
#***********************************************************   
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()
        
#***********************************************************
#*********** Setup MatPlotLib graph of data ****************
    def init_plot(self):
        
        self.dpi = 100
        self.fig = Figure((3.0, 4.5), dpi=self.dpi)
  
        self.host = HostAxes(self.fig, [0.15, 0.1, 0.65, 0.8])
        self.par1 = ParasiteAxes(self.host, sharex=self.host)

        self.host.parasites.append(self.par1)  # for multiple axis
 
        self.host.set_ylabel("Depth dB(~m)")
        self.host.set_xlabel("Time( Sec)")

        self.host.tick_params(axis='both', which='major', labelsize=6)

        self.host.set_facecolor('black')
        self.host.set_title('Bongo trace file= '+self.LogFileName, size=10)
        self.host.xaxis.set_label_coords(0.3, 0.5)
              
        self.host.axis["right"].set_visible(False)
        self.par1.axis["right"].set_visible(True)
        self.par1.set_ylabel(u"Temperature(°C)")
        self.host.axis["left"].label.set_size(12) 
  
        self.par1.axis["right"].major_ticklabels.set_visible(True)
        self.par1.axis["right"].label.set_visible(True)
       
        self.host.axis["left"].major_ticklabels.set_size(8)
        self.host.axis["bottom"].major_ticklabels.set_size(8)
        self.par1.axis["right"].major_ticklabels.set_size(8) 

        self.fig.add_axes(self.host)
  
        self.plot_Pres = self.host.plot(
            self.data["Pres"],self.data["Et"], 
            linewidth=1,
            color=(1, 1, 0),
            )[0]

        self.plot_Temp = self.par1.plot(
            self.data["Temp"],self.data["Et"], 
            linewidth=1,
            color=(1, 0.5, 0),
            )[0]

# fixed reference line (RED) drawn 
        self.plot_Ref = self.host.plot(
            self.SlopeLineX,self.SlopeLineY,
            linewidth=1,
            color=(1, 0, 0),
            )[0]
        self.axes = self.host
#        start, end = ax.get_xlim()
#        ax.xaxis.set_ticks(np.arange(start, end, 600)) 
#        self.host.legend()
  
        self.host.axis["left"].label.set_color(self.plot_Pres.get_color())
        self.par1.axis["right"].label.set_color(self.plot_Temp.get_color())

#*************** Enf of Init_Plot ***************************

        
#############################################

    def draw_plot(self):
        """ Redraws the plot
        """
   
        # when xmin is on auto, it "follows" xmax to produce a 
        # sliding window effect. therefore, xmin is assigned after
        # xmax.
        #
        if self.xmax_control.is_auto():
            xmax = len(self.data["Pres"]) if len(self.data["Pres"]) > 1800 else 1800
        else:
            xmax = int(self.xmax_control.manual_value())
            
        xmin = 0.0

        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        # 
        # note that it's easy to change this scheme to the 
        # minimal/maximal value in the current display, and not
        # the whole data set.
        
        if self.ymin_control.is_auto():
            ymin = round(min(self.data["Pres"]), 0)
        else:
            ymin = int(self.ymin_control.manual_value())

        if ymin > 0 :    # we are working upside down
            ymin *=-1.0
        ymax = 0.0            

        
        if self.tmin_control.is_auto():
            tmin = round(min(self.data["Temp"]), 0) 
        else:
            tmin = int(self.tmin_control.manual_value())
        
        if self.tmax_control.is_auto():
            tmax = round(max(self.data["Temp"]), 0)
        else:
            tmax = int(self.tmax_control.manual_value())


        if self.DownSlope_control.is_auto():
            self.Dslope = 20.0  
        else:
            self.Dslope = int(self.DownSlope_control.manual_value())
      
        if self.UpSlope_control.is_auto():
            self.Uslope = 10.0
        else:
            self.Uslope = int(self.UpSlope_control.manual_value())

# 60 is acutally samples per minute from ctd, default is 1/sec but should be a var really
# neg 60 is to handle depth negative
        SlopeTime1 = (ymin/self.Dslope)*-60.0/DEFAULT_RATE
        SlopeTime2 = SlopeTime1+(ymin/self.Uslope)*-60.0/DEFAULT_RATE
#        print SlopeTime1, SlopeTime2
        self.SlopeLineX = np.array([0.0,SlopeTime1,SlopeTime2])
        self.SlopeLineY = np.array([0.0,ymin,0.0])

        self.host.set_xbound(lower=xmin, upper=xmax)
        self.host.set_ybound(lower=ymin-10.0, upper=ymax)

        self.par1.set_xbound (lower=xmin, upper=xmax)
        self.par1.set_ybound(lower=tmin, upper=tmax)        
        
        # anecdote: axes.grid assumes b=True if any other flag is
        # given even if b is set to False.
        # so just passing the flag into the first statement won't
        # work.
        #
        if self.cb_grid.IsChecked():
            self.axes.grid(True, color='gray')
        else:
            self.axes.grid(False)

# no need to redraw if we are idling the data input
        if (self.GraphRun) :        
#            self.plot_Pres.set_xdata(np.arange(len(self.data["Pres"])))
            self.plot_Pres.set_xdata(np.array(self.data["Et"]))
            self.plot_Pres.set_ydata(np.array(self.data["Pres"]))
#            self.plot_Temp.set_xdata(np.arange(len(self.data["Temp"])))
            self.plot_Temp.set_xdata(np.array(self.data["Et"]))
            self.plot_Temp.set_ydata(np.array(self.data["Temp"])) 

# if the ref line is changed
        self.plot_Ref.set_xdata(self.SlopeLineX)
        self.plot_Ref.set_ydata(self.SlopeLineY)
        
#any scalling changes ir change to the ref line will get updated on this call       
        self.canvas.draw()

#*** END of draw_plot ********************88

#*** ACTION METHODS ***************        
    def on_GraphRun_button(self, event):
        if  not self.DataSource == None :
            self.GraphRun = not self.GraphRun
            self.on_update_GraphRun_button(event)
            if self.GraphRun == True:
                self.MonitorRun = True
                self.on_update_monitor_button(event)

    def on_monitor_button(self, event):
        if  not self.DataSource == None :
          self.MonitorRun = not self.MonitorRun
          self.on_update_monitor_button(event)
          if self.MonitorRun == False:
            self.GraphRun = False
            self.on_update_GraphRun_button(event)
    
    def on_update_GraphRun_button(self, event):
        label = "Stop Graph/Logging" if self.GraphRun else "Start Graph/Logging"
        self.GraphRun_button.SetLabel(label)

    def on_update_monitor_button(self, event):
        label = "Stop CTD Monitor" if self.MonitorRun else "Start CTD Monitor"
        self.monitor_button.SetLabel(label)
    
    def on_cb_grid(self, event):
        self.draw_plot()
    
    def on_cb_xlab(self, event):
        self.draw_plot()
    
            
################### ON_REDRAW_TIMER ##########################################################
# This method is repeatably called by the re-draw timeer to get any new data and update plot
# to respond to scale modifications, grid change, etc.
# what it does depends on the STATE variables
##############################################################################################

    def on_redraw_timer(self, event):

# recorded_data = False means parse raw ctd format data, this flag is for testing
        self.Tstr = '0'
        ETstr ='0'
        pres = 0.0

# if no data source do nothing, but call for a re-draw in case any controls have been changed
        if self.DataSource == None :
            self.draw_plot()
            return()

        if  not self.MonitorRun :
          self.DataSource.flush()
        else :
          scan =self.DataSource.next()
          
          if scan["OK"]:
        
# no battery voltage in bongo95 outfile, channel 7 in raw data Vstr = line[7]
# need to add density calculation
# we will only save the  data when the graph is running
# this part is the data that is plotted on the graph.. NOTE at the moment there is a
# 1 sec(unit) per scan assumption here since there is no time variable , it is plotting against
# record number; really need to plot against computer or ctd clock if rate is not 1 scan per second
# ie make use of ETstr created below

              if self.GraphRun :             
                  temp = float(scan["Tstr"])

                  self.data["Pres"].append(-1.*float(scan["Pstr"]))
                  self.data["Temp"].append(float(scan["Tstr"]))
                  if self.RT_source:
                     if self.StartTime == 0:
                        self.StartTime = time.time()
                        
                     scan["Et"] = str(time.time() - self.StartTime)     

                  self.data["Et"].append(float(scan["Et"]))


                  
                  
#                  print time.strftime('%Y:%m:%dT%X') # ISO 8601 date time stamp                  
          else : # if scan not ok out of data so stop the graph and monitor, turning off the monitor turns off the graph as well
              self.on_monitor_button(wx.EVT_BUTTON)
              self.on_update_monitor_button(wx.EVT_UPDATE_UI)
              if self.RT_source :
                  self.on_stop_rt(1)
                  self.message_box("DATA SOURCE HAS STOPPED or MISSING\nIF THIS IS UNEXPECTED CHECK CABLING etc\n ...CLOSING CONNECTION...")
              else :
                   self.on_stop_arc(1)


# these are the data displayed on the monitor line
          if scan["OK"] and self.MonitorRun:

           Rstr = '{:>5.4}'.format(str(self.SRate.get_rate(scan["pres"])))
          
           self.p_text.Data_text.SetValue(scan["Pstr"])
           self.t_text.Data_text.SetValue(scan["Tstr"])
           self.c_text.Data_text.SetValue(scan["Cstr"])
           self.s_text.Data_text.SetValue(scan["Sstr"])
           self.d_text.Data_text.SetValue(scan["Dstr"])
           self.f1_text.Data_text.SetValue(scan["F1str"])
           self.f2_text.Data_text.SetValue(scan["F2str"])
           self.l_text.Data_text.SetValue(scan["Lstr"])
           self.v_text.Data_text.SetValue(scan["Vstr"])
           self.r_text.Data_text.SetValue(Rstr)
           self.et_text.Data_text.SetValue('{:>5.4}'.format(scan["Et"]))
#           self.ctd_clock_text.Data_text.SetValue(scan["ctdclock"])
        
           if self.GraphRun and self.runlogfile :
               self.ScanNum+=1
               xdatetime = '{:>8.8}'.format(str(datetime.datetime.now().time()))

               self.runlogfile.write(str(self.ScanNum)+" "+xdatetime+" "+'{:>5.4}'.format(scan["Et"])+" "+scan["Pstr"]+" "+scan["Tstr"]+" "+scan["Cstr"]+
                     " "+scan["Sstr"]+" "+scan["Dstr"]+ " "+scan["F1str"]+" "+scan["F2str"]+" "+scan["Lstr"]+" "+scan["Vstr"]+"\n")

#  end of if else MonitorRun
# call draw-plot iregardless of monitor status so that rescale works, else it
# wont update to new button settings until monitor is started
#  redraw the plot, and then return to wait for next timer call
        self.draw_plot()

######################## Menu things ########################
    def save_file_dialog(self):

        """Save contents of output window."""
        outfilename = None
        dlg = wx.FileDialog(None, "Save File As...", "", "", "BONGO Dat-File|*.dat|All Files|*",  wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() ==  wx.ID_OK:
            outfilename = dlg.GetPath()
        dlg.Destroy()
        return (outfilename)
    
    def get_file_dialog(self):
        filename = None
        dialog = wx.FileDialog(None, "Choose File.",os.getcwd(), "", "BONGO Dat-File|*.dat|All Files|*",wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            filename =  dialog.GetPath()  
        dialog.Destroy()
        return(filename)
    
# Save plot image
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
            
# Configure serial port, requires our serial instance, make sure port is closed before calling
    def on_ser_config(self,event):
        self.ser.close()
        dialog_serial_cfg = wxSerialConfigDialog.SerialConfigDialog(None, -1, "",
                show=wxSerialConfigDialog.SHOW_BAUDRATE|wxSerialConfigDialog.SHOW_FORMAT|wxSerialConfigDialog.SHOW_FLOW,
                serial=self.ser
            )
        result = dialog_serial_cfg.ShowModal()
        dialog_serial_cfg.Destroy()

# pop up the wxterminal for interaction with ctd - THIS IS NOT WORKING YET NEEDS WORK
    def on_term(self,event):

        self.ser.close()
#        wxTerminal.MyApp()
#        print "opening wx"
#        frame_terminal=wxTerminal.MyApp(0)
        frame_terminal=wxTerminal_NAFC.TerminalFrame(self, -1, "")
#        print "Show modal"
#        self.SetTopWindow(frame_terminal)
        frame_terminal.Show()
#        print "Destroying"
        frame_terminal.Destroy()

# Realtime -> start  opens serial port and log file for realtime data
        
    def on_start_rt (self, event):

        if self.Serial_In == None:
            self.Serial_In = self.SSource

        self.port_open = self.Serial_In.open_Port()
        if not self.port_open :
            self.message_box("Can Not Open Port- check settings"+self.ser.getPort())          
            return()
        
# if we have an open port proceed     
        self.RT_source = True
        
        self.LogFileName = self.save_file_dialog() # get filename of desired logfile

        if not self.LogFileName == None :
            self.flash_status_message("OPENING FILE FOR OUTPUT "+self.LogFileName)
            self.runlogfile = open(self.LogFileName,"w")
            self.WriteHeader(self.runlogfile)
        else:
            self.flash_status_message("NOT LOGGING TO FILE")
            self.LogFileName = "NOT LOGGING TO FILE"
            
        self.host.set_title('Bongo trace data file= '+self.LogFileName, size=8) # label plot

# now configure the STD and start the data coming
        self.Serial_In.send_Real()
        self.interval = DEFAULT_RATE  # until there is a menu item to change it :-)
        self.Serial_In.send_Set_DataRate(str(self.interval))
        self.Serial_In.send_Start_Data()

# Lock out some controls like archived data play back while RealTime is running
# set End to active Start to inactive on Realtime Memu
# need to add lock out on serial config as well !!!
        menubar = self.menubar

        enabled = menubar.IsEnabled(ID_START_RT)
        menubar.Enable(ID_START_RT,not enabled)
        enabled = menubar.IsEnabled(ID_STOP_RT)
        menubar.Enable(ID_STOP_RT,not enabled)
        menubar.Enable(ID_SER_CONF, False)
        menubar.EnableTop(2, False)  # lock out arc playback while rt running
        self.monitor_button.Enable(True)
        self.GraphRun_button.Enable(True)
        self.data["Pres"]=[0]
        self.data["Temp"]=[0]
        self.data["Et"]=[0]
        self.DataSource = self.Serial_In


# *****************************************************************

    def on_stop_rt (self, event):
        if self.MonitorRun:
             self.on_monitor_button(event)
        try:                  
              self.runlogfile.close()
        except: pass
        
        self.RT_source = False
        self.DataSource = None
        self.Serial_In.send_Stop_Data ()
        self.Serial_In.close_Port ()
        self.port_open = False
        menubar = self.GetMenuBar()
        enabled = menubar.IsEnabled(ID_START_RT)
        menubar.Enable(ID_START_RT,not enabled)
        enabled = menubar.IsEnabled(ID_STOP_RT)
        menubar.Enable(ID_STOP_RT,not enabled)
        menubar.Enable(ID_SER_CONF, True)

        menubar.EnableTop(2, True)  # re-enable archieved data option
        self.monitor_button.Enable(False)
        self.GraphRun_button.Enable(False)
        
#************************ archieve data ***************************
    def on_start_arc(self, event):
        FileName = self.get_file_dialog()  #get filename of logged file
        if FileName !="" :
            self.RT_source = False
            self.ARC_source = True
            self.host.set_title('Bongo trace data file= '+FileName, size=8) # label plot            
            menubar = self.GetMenuBar()
            enabled = menubar.IsEnabled(ID_START_ARC)
            menubar.Enable(ID_START_ARC,not enabled)
            enabled = menubar.IsEnabled(ID_STOP_ARC)
            menubar.Enable(ID_STOP_ARC,not enabled)
            menubar.EnableTop(1, False)  # lock out RT playback while Archieved running
            self.monitor_button.Enable(True)
            self.GraphRun_button.Enable(True)            
            self.datagen = DataGen2(FileName) #Create a data source instance
#            self.fig.clf()
            self.data["Pres"]=[0]
            self.data["Temp"]=[0]
            self.data["Et"]=[0]
            self.DataSource = self.datagen 

    def on_stop_arc (self, event):
        if self.MonitorRun:
             self.on_monitor_button(event)
        self.ARC_source = False
        self.DataSource = None
        self.datagen.close_infile()

        menubar = self.GetMenuBar()
        enabled = menubar.IsEnabled(ID_START_ARC)
        menubar.Enable(ID_START_ARC,not enabled)
        enabled = menubar.IsEnabled(ID_STOP_ARC)
        menubar.Enable(ID_STOP_ARC,not enabled)
        self.monitor_button.Enable(False)
        self.GraphRun_button.Enable(False)
        menubar.EnableTop(1, True)  # re-enable realtime data option

    def on_edit_head(self,event):
        if self.RT_source == True:
            self.on_stop_rt (1)
#        WINAQU_GUI_BONGO.main()

    def on_set_base_header(self,event):
        xx = ShipTrip_Dialog(self,self.hd1["SHIP"],self.hd1["TRIP"],self.hd1["STN"])
        print ("before "+self.hd1["SHIP"]+" "+ self.hship)

        xx.SetBase(self.hship,self.hd1["TRIP"],self.hd1["STN"])
        res=xx.ShowModal()
        if res == wx.ID_OK:

 
            self.hd1["SHIP"] = xx.GetShip()
            self.hship = xx.GetShip()
            self.hd1["TRIP"] = xx.GetTrip()
            self.hd1["STN"] = xx.GetStn()
            print ("AFTER="+self.hd1["SHIP"]+" "+ self.hship)
            self.hship="LL"

            xx.Destroy()


#******************* assorted  methods ****************************************************

    def WriteHeader (self,fp) :
#        print "In WRite "+self.hd1["SHIP"]

        xtime = '{:>5.5}'.format(str(datetime.datetime.now().time()))
        xdate = '{:>12.12}'.format(str(datetime.datetime.now().date()))
        hdr1_out= self.hd1["SHIP"].strip().zfill(2)+ self.hd1["TRIP"].strip().zfill(3)+ self.hd1["STN"].strip().zfill(3)
        fp.write("NAFC_Y2K_HEADER\n")
        fp.write (hdr1_out+"                    "+xdate+" "+xtime+"      STD12     O                1\n")
        fp.write (hdr1_out+" 000000 01.00 A 12 #ZEPTCSMWwLV--------              000 0000 0000 000 4\n")
        fp.write (hdr1_out+"                                                                       8\n")
        fp.write ("SCAN CtdClk   ET   DEPTH    TEMP  COND   SAL   SIGMAT   FLOW1   FLOW2  LIGHT   VOLTS\n")
        fp.write ("-- DATA --\n")


    
    def on_exit(self, event):
        if self.runlogfile != "": 
          self.runlogfile.close()
        self.redraw_timer.Stop()
        if self.port_open:
          self.Serial_In.close_Port()
        self.Destroy()
    
    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER, 
            self.on_flash_status_off, 
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)
    
    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')

    def message_box (self,message):
        result= wx.MessageBox (message,style=wx.CENTER|wx.OK)

    def ShowMessage2(self, event):
        dial = wx.MessageDialog(None, 'Error loading file', 'Error', 
        wx.OK | wx.ICON_ERROR)
        dial.ShowModal()  

    def OnAbout(self,event):
        """ Show About Dialog """
        info = wx.AboutDialogInfo()

        desc = ["\nWinBongo\n",
                "Platform Info: (%s,%s)",
                "License: None - see code"]
        desc = "\n".join(desc)

        # Platform info
        py_version = [sys.platform,", python ",sys.version.split()[0]]
        platform = list(wx.PlatformInfo[1:])
        platform[0] += (" " + wx.VERSION_STRING)
        wx_info = ", ".join(platform)

        info.SetName(TITLE)
        info.SetVersion(VERSION)
        info.SetDevelopers (["D. Senciall",
                             "\nBiological & Physical Oceanography Section",
                             "\n NWAFC, Nl region-DFO, Gov. of Canada"])
        info.SetCopyright ("Note: Some elements based on open community code:\nSee Source for credits")
#        info.SetDescription (desc % (py_version, wx_info))
        wx.AboutBox(info)
        
#******** END of GraphFrame ************************************************************

#        def __init__( self, parent ):
#                wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"WinAquire Header Editor", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )


class ShipTrip_Dialog(wx.Dialog) :
    def __init__(self,parent,ship,trip,stn):
        wx.Dialog.__init__ ( self, parent,title = u"ShipTrpStn" )
#        super(ShipTrip_Dialog,self).__init__(parent)
        
        self.panel = EntryPanel(self,ship,trip,stn )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel,1,wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()
    def SetBase(self,ship,trip,stn):
        self.panel.SetBase(ship,trip,stn)

    def GetShip(self):
            return (self.panel.GetShip())
    def GetTrip(self):
            return (self.panel.GetTrip())
    def GetStn(self):
            return (self.panel.GetStn())

class EntryPanel (wx.Panel):
      
    def __init__( self, parent,ship,trip,stn ):
            super(EntryPanel,self).__init__(parent)
#            wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, title = u"SET BASE HEADER", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

            self.ship = wx.TextCtrl(self)
#            self._ship = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ) )
            self.ship.SetMaxLength( 2 ) 
            self.ship.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
            self._trip = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 57,-1 ) )
            self._trip.SetMaxLength( 3 ) 
            self._trip.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
            self._stn = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 57,-1 ) )
            self._stn.SetMaxLength( 3 ) 
            self._stn.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                
               
#                SHPTRPSTN_GRID.Add( self.TRIP, 0, wx.ALL, 5 )


#            self._ship = wx.TextCtrl(self)
#            self._trip = wx.TextCtrl(self)
#            self._stn = wx.TextCtrl(self)

            sizer = wx.FlexGridSizer(3,2,8,8)
            sizer.Add(wx.StaticText (self,label="SHIP:"),0,wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self.ship,0,wx.EXPAND)
            sizer.Add(wx.StaticText (self,label="TRIP:"),0,wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self._trip,0,wx.EXPAND)
            sizer.Add(wx.StaticText (self,label="STN:"),0,wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self._stn,0,wx.EXPAND)

            msizer = wx.BoxSizer(wx.VERTICAL)
            msizer.Add(sizer,1,wx.EXPAND|wx.ALL,20)
            btnszr = wx.StdDialogButtonSizer()
            button = wx.Button(self,wx.ID_OK)
            button.SetDefault()
            btnszr.AddButton(button)
            msizer.Add(btnszr, 0, wx.ALIGN_CENTER|wx.ALL,12)
            btnszr.Realize()

            self.SetSizer(msizer)

            self.ship.SetValue(ship)
            self._trip.SetValue(trip)
            self._stn.SetValue(stn)
            
    def SetBase (self,ship,trip,stn):
            self.ship.SetValue(ship)
            self._trip.SetValue(trip)
            self._stn.SetValue(stn)    
        
    def GetBase(self):
            return self.ship.GetValue(),self._trip.GetValue(),self._stn.GetValue()


        
    def GetShip(self):
                print ("IN MODEL="+self.ship.GetValue())
                return self.ship.GetValue()
    def GetTrip(self):
                return self._trip.GetValue()
    def GetStn(self):
                return self._stn.GetValue()
    

#***************************************************************************************


class ConvertClass ():

    def __init__(self):
        self.a = (999.842594, 6.793952e-2, -9.095290e-3, 1.001685e-4, -1.120083e-6,6.536332e-9)
        self.b = (8.24493e-1, -4.0899e-3, 7.6438e-5, -8.2467e-7, 5.3875e-9)
        self.c = (-5.72466e-3, 1.0227e-4, -1.6546e-6)
        self.d = 4.8314e-4

        self.bastime = 0 

    def convert_STD12_raw(self,line):
        scan = dict()
        scan["ctdclock"] = line[0]
        xdatetime = datetime.datetime.strptime(scan["ctdclock"],'%H:%M:%S')
#       if basetime == 0 :
#                 basetime = xdatetime
                 
        scan["pres"] = -1.*(float(line[1])/10.0)
        scan["Pstr"] = str('{:.5}'.format(int(line[1])/10.0))
        scan["Tstr"] = str('{:.5}'.format(int(line[2])/1000.0))
        scan["Cstr"] = str('{:.5}'.format(int(line[3])/1000.0/42.921))
# for flow if < 56.5  value should be 0.. need to add
        scan["F1str"] = str('{:.5}'.format(int(line[4])/100.0))
        scan["F2str"] = str('{:.5}'.format(int(line[5])/100.0))
        scan["Lstr"] = str('{:.5}'.format(int(line[6])/100.0))
        scan["Vstr"] = str('{:.5}'.format(int(line[7])/100.0))
        scan["Sstr"] = str('{:.5}'.format(int(line[8])/1000.0))
        scan["Dstr"]= str('{:5}'.format(self.dens0((int(line[8])/1000.0),(int(line[2])/1000.0)-1000.0)))
        scan["OK"] = True
        scan["Et"] = 0.0
        return (scan)

    def convert_SBE19p_raw(self, line):
            scan = dict()
#            scan["ctdclock"] = line[0]
#            xdatetime = datetime.datetime.strptime(scan["ctdclock"], '%H:%M:%S')
            #       if basetime == 0 :
            #                 basetime = xdatetime

            scan["pres"] = -1. * (float(line[2]))
            scan["Pstr"] = str('{:7.5}'.format(float(line[2])))
            scan["Tstr"] = str('{:7.5}'.format(float(line[0])))
            scan["Cstr"] = str('{:7.5}'.format(float(line[1])))
            # for flow if < 56.5  value should be 0.. need to add
            scan["F1str"] = ""
            scan["F2str"] = ""
            scan["Lstr"] = ""
#            scan["Vstr"] = str('{:7.5}'.format(float(line[5])))
#
            scan["Sstr"] = str('{:7.5}'.format(float(line[3])))
#            scan["Dstr"] = str('{:7.5}'.format(float (line[4])))
            scan["Vstr"] = ""

            scan["Dstr"] = ""

            scan["OK"] = True
            scan["Et"] = 0.0
            return (scan)

    def convert_archived(self,line):
        scan = dict()

#        xdatetime = datetime.datetime.strptime(ctdclock,'%H:%M:%S')
#        if basetime = 0 :
#                 basetime = xdatetime
#        scan["ctdclock"] = line[0]
        scan["scannum"]=line[0]
        scan["ctdclock"] = line[1]
        scan["Et"] = line[2]
        scan["pres"] = -1.*float(line[3])
        scan["Pstr"] = str('{:.5}'.format(line[3]))
        scan["Tstr"] = str('{:.5}'.format(line[4]))
        scan["Cstr"] = str('{:.5}'.format(line[5]))
        scan["Sstr"] = str('{:.6}'.format(line[6]))
        scan["Dstr"] = str('{:.6}'.format(line[7]))
        scan["F1str"] = str('{:.5}'.format(line[8]))
        scan["F2str"] = str('{:.5}'.format(line[9]))
        scan["Lstr"] = str('{:.5}'.format(line[10]))
        scan["Vstr"] = str('{:.5}'.format(line[11]))
#        scan["Et"] = xdatetime - basetime

#        scan["Dstr"] = str('{:.5}'.format(self.dens0(np.float(line[6]),np.float(line[4]))-1000.0))
        scan["OK"] = True
        return (scan)

    def convert_simulation_b95(self,line):
        scan = dict()

#        xdatetime = datetime.datetime.strptime(ctdclock,'%H:%M:%S')
#        if basetime = 0 :
#                 basetime = xdatetime
#        scan["ctdclock"] = line[0]
        scan["ctdclock"] = "00:11:22"
        scan["pres"] = -1.*float(line[0])
        scan["Pstr"] = str('{:.5}'.format(line[0]))
        scan["Sstr"] = str('{:.6}'.format(line[2]))
        scan["Tstr"] = str('{:.5}'.format(line[3]))
        scan["Cstr"] = str('{:.5}'.format(line[1]))
        scan["F1str"] = str('{:.5}'.format(line[6]))
        scan["F2str"] = str('{:.5}'.format(line[7]))
        scan["Lstr"] = str('{:.5}'.format(line[5]))
        scan["Vstr"] = str('{:.5}'.format("12.5"))
#        scan["Et"] = xdatetime - basetime
        scan["Et"] = "0"
        scan["Dstr"] = str('{:.5}'.format(self.dens0(np.float(line[2]),np.float(line[3]))-1000.0))
        scan["OK"] = True
        return (scan)

    
# Code Borrowed from seawater-3.3.2-py.27.egg
    def dens0(self,s, t):

       """
    Density of Sea Water at atmospheric pressure.

    Parameters
    ----------
    s(p=0) : array_like
             salinity [psu (PSS-78)]
    t(p=0) : array_like
             temperature [℃ (ITS-90)]

    Returns
    -------
    dens0(s, t) : array_like
                  density  [kg m :sup:`3`] of salt water with properties
                  (s, t, p=0) 0 db gauge pressure

    References
    ----------
    .. [1] Fofonoff, P. and Millard, R.C. Jr UNESCO 1983. Algorithms for computation of fundamental properties of seawater. UNESCO Tech. Pap. in Mar. Sci., No. 44, 53 pp.  Eqn.(31) p.39. http://unesdoc.unesco.org/images/0005/000598/059832eb.pdf

    .. [2] Millero, F.J. and  Poisson, A. International one-atmosphere equation of state of seawater. Deep-Sea Res. 1981. Vol28A(6) pp625-629. doi:10.1016/0198-0149(81)90122-9

    Notes
    -----
    Modifications: 92-11-05. Phil Morgan.
                   03-12-12. Lindsay Pender, Converted to ITS-90.

    """

# UNESCO 1983 Eqn.(13) p17.     
       s, t = map(np.asanyarray, (s, t))

#    T68 = T68conv(t)
       T68 = t
# UNESCO 1983 Eqn.(13) p17.
#    b = (8.24493e-1, -4.0899e-3, 7.6438e-5, -8.2467e-7, 5.3875e-9)
#    c = (-5.72466e-3, 1.0227e-4, -1.6546e-6)
#    d = 4.8314e-4
       a=self.a
       b=self.b
       c=self.c
       d=self.d
       return (self.smow(t) + (b[0] + (b[1] + (b[2] + (b[3] + b[4] * T68) * T68) *
            T68) * T68) * s + (c[0] + (c[1] + c[2] * T68) * T68) * s *
            s ** 0.5 + d * s ** 2)

    def smow(self,t):
        """
    Density of Standard Mean Ocean Water (Pure Water) using EOS 1980.

    Parameters
    ----------
    t : array_like
        temperature [℃ (ITS-90)]

    Returns
    -------
    dens(t) : array_like
              density  [kg m :sup:`3`]

 
    References
    ----------
    .. [1] Fofonoff, P. and Millard, R.C. Jr UNESCO 1983. Algorithms for computation of fundamental properties of seawater. UNESCO Tech. Pap. in Mar. Sci., No. 44, 53 pp.  Eqn.(31) p.39. http://unesdoc.unesco.org/images/0005/000598/059832eb.pdf

    .. [2] Millero, F.J. and  Poisson, A. International one-atmosphere equation of state of seawater. Deep-Sea Res. 1981. Vol28A(6) pp625-629. doi:10.1016/0198-0149(81)90122-9

    Notes
    -----
    Modifications: 92-11-05. Phil Morgan.
                   99-06-25. Lindsay Pender, Fixed transpose of row vectors.
                   03-12-12. Lindsay Pender, Converted to ITS-90.

        """

        t = np.asanyarray(t)

#    a = (999.842594, 6.793952e-2, -9.095290e-3, 1.001685e-4, -1.120083e-6,6.536332e-9)
        a = self.a
#    T68 = T68conv(t)
        T68 = t
        return (a[0] + (a[1] + (a[2] + (a[3] + (a[4] + a[5] * T68) * T68) * T68) *
            T68) * T68)


##############################################################################################
#####################################  MAIN ENTRY POINT ################################        
if __name__ == '__main__':

    app = wx.App()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
###################################### END OF CODE #####################################
