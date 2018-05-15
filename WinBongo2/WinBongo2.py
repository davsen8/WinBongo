# -*- coding: utf-8 -*-


"""

WinBongo2.py   D.Senciall  May 2018   python 3.65  wxpython 4.0.1 pheonix compatible

Elements BASED ON CODE SAMPLE FROM: matplotlib-with-wxpython-guis by E.Bendersky
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 31.07.2008
see   http://eli.thegreenplace.net/2008/08/01/matplotlib-with-wxpython-guis/

Also
 Code Borrowed from seawater-3.3.2-py.27.egg for the density calcuations

"""

import os
import sys
import wx
try:        #  2.7 vs 3.65 versions of queue class
    import queue
except:
    import Queue as queue

import json

import time
import serial
import datetime
# The recommended way to use wx graphics and matplotlib (mpl) is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
#from mpl_toolkits.axes_grid.parasite_axes import HostAxes, ParasiteAxes   DEPRECIATED
from mpl_toolkits.axes_grid1.parasite_axes import HostAxes, ParasiteAxes
import numpy as np

import wxSerialConfigDialog
#import wxTerminal_NAFC
#from WinAquireHdr import WINAQU_Thread
#from WinAquireHdr import WINAQU_GUI

import Bongo_Serial_Tools as BST
#import wxTerminal_NAFC

ID_START_RT = wx.NewId()
ID_STOP_RT = wx.NewId()
ID_START_ARC = wx.NewId()
ID_STOP_ARC = wx.NewId()
ID_SER_CONF = wx.NewId()
ID_INIT = wx.NewId()
ID_STATUS = wx.NewId()
ID_STOP = wx.NewId()
ID_WAKE = wx.NewId()
ID_RESET = wx.NewId()

VERSION = "V2.02 May 2018"
TITLE = "WinBongo2"

CTD="SBE"
SIMULATOR = False


    
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

        self.SetBackgroundColour('lightgray')   # affects the space arround buttons etc but not graph

        self.ser = serial.Serial()  # Create a serial com port access instance

        # get the last basename, and serial port parameters
        # if there is no pre-existing file Bongo.cfg a new one is name with default starting basename
        # for the mission and the serial configuration dialogue is displayed to get setup
        if not self.read_cfg(self.ser):
            self.set_default_com_cfg(self.ser)
            self.on_ser_config(-1)

        self.BQueue = queue.Queue()

        CTD = "SBE"

        self.SRate = BST.SmoothRate(5)  # Create a rate smoother instance

        self.port_open = False
        self.DataSource = None

# Some state variables
        self.GraphRun = False
        self.MonitorRun = False

        self.RT_source = False
        self.ARC_source = False
        self.runlogfile=None
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
#10 ms; if you call at slower rate say 100 ms things may not respnd as quick, but there
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(100)

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
#        m_term = menu_file.Append(-1, "Launch Terminal", "Terminal")
#        self.Bind(wx.EVT_MENU, self.on_term, m_term)
#        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        # responds to exit symbol x on frame title bar
        self.Bind(wx.EVT_CLOSE, self.on_exit)

        menu_realtime = wx.Menu()
        m_rtstart = menu_realtime.Append(ID_START_RT, "Start", "Start realtime data")
        self.Bind(wx.EVT_MENU, self.on_start_rt, m_rtstart)
        menu_realtime.AppendSeparator()
        m_rtstop = menu_realtime.Append(ID_STOP_RT, "End", "End realtime data")
        self.Bind(wx.EVT_MENU, self.on_stop_rt, m_rtstop)
        menu_realtime.AppendSeparator()
        self.m_initlogger = menu_realtime.Append(ID_INIT, "Initial Logger", "Clear ctd Memmory")
        self.Bind(wx.EVT_MENU, self.on_init_logger, self.m_initlogger)
        menu_realtime.AppendSeparator()
        self.m_getctdstatus = menu_realtime.Append(ID_STATUS, "Get CTD status", "CTD Status (DS)")
        self.Bind(wx.EVT_MENU, self.on_get_ctd_status, self.m_getctdstatus)
        menu_realtime.AppendSeparator()
        menu_realtime.AppendSeparator()
        self.m_sendwake = menu_realtime.Append(ID_WAKE, "Wake CTD", "Wake CTD")
        self.Bind(wx.EVT_MENU, self.on_sendwake, self.m_sendwake)
        menu_realtime.AppendSeparator()
        self.m_sendstop = menu_realtime.Append(ID_STOP, "Force a Stop on Data", "CTD STOP ")
        self.Bind(wx.EVT_MENU, self.on_sendstop, self.m_sendstop)


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
        self.cb_grid = menu_option.Append (-1,"Show Grid","Grid",kind=wx.ITEM_CHECK)
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
        self.m_initlogger.Enable(False)
        self.m_getctdstatus.Enable(False)

        self.m_sendstop.Enable(True)
#        m_edithead(False)
#        m_term.Enable (False)  # leave off for now
        m_basehead.Enable(False)

        self.menubar.EnableTop(2, False)  # lock out arc playback while rt running

# ***********************************************************************************
    def create_main_panel(self):
        
        self.panel = wx.Panel(self)  # Create a Panel instance

# The Plot-  init_pot sets up the MatPlotLib graph
        self.init_plot()
        
# Create a Canvas  make plot area background light gray
        self.fig.patch.set_facecolor("lightgray")
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
 
        self.host.tick_params(axis='both', which='major', labelsize=6)

# set the color of the graph area
        self.host.set_facecolor('black')
#        self.host.set_edgecolor('gray')
        self.host.set_title('Bongo trace file= '+self.LogFileName, size=10)
        self.host.xaxis.set_label_coords(0.3, 0.5)
#        self.host.set_facecolor("lightslategray")
              
        self.host.axis["right"].set_visible(False)
        self.par1.axis["right"].set_visible(True)
        self.par1.axis["left"].set_visible(False)
        self.par1.set_ylabel(u"Temperature(°C)",fontweight='bold', fontsize=14)
#        self.host.axis["left"].label.set_size(12)
  
        self.par1.axis["right"].major_ticklabels.set_visible(True)
        self.par1.axis["right"].label.set_visible(True)
       
        self.host.axis["left"].major_ticklabels.set_size(8)
        self.host.axis["bottom"].major_ticklabels.set_size(8)
        self.par1.axis["right"].major_ticklabels.set_size(8)

        self.host.xaxis.set_label_coords(0.5, -0.06)
        self.host.set_ylabel("Depth dB(~m)",fontweight='bold', fontsize=14)
        self.host.set_xlabel("Time( Sec)",fontweight='bold', fontsize=10)

        self.fig.add_axes(self.host)

# ctd pressure yellow
        self.plot_Pres = self.host.plot(
            self.data["Pres"],self.data["Et"], 
            linewidth=1,
            color=(1, 1, 0),
            )[0]
# temperature trace orange
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
        DEFAULT_RATE = 1.0
        SlopeTime1 = (ymin/self.Dslope)*-60.0/DEFAULT_RATE
        SlopeTime2 = SlopeTime1+(ymin/self.Uslope)*-60.0/DEFAULT_RATE

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
        
#any scalling changes or change to the ref line will get updated on this call
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

          if self.MonitorRun:
              self.DataSource.unpause_data_feed()
              self.flash_status_message("SENDING STARTNOW FOR DATA")
              self.DataSource.send_StartNow_Data()
          else:
              self.DataSource.pause_data_feed()
              self.flash_status_message("STOPPING DATA FEED")
              self.DataSource.send_Stop_Data()

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
        block = dict()

# if no data source do nothing, but call for a re-draw in case any controls have been changed
        if self.DataSource == None :
            self.draw_plot()
            return()

        if  not self.MonitorRun :
            self.draw_plot()
            return()
        else:
            if not self.BQueue.empty():
                tries = 0
                block = self.BQueue.get()
            else:   # Empty Queue
                self.draw_plot()
                return()

        if block["OK"]:
        
# no battery voltage in bongo95 outfile, channel 7 in raw data Vstr = line[7]
# need to add density calculation
# we will only save the  data when the graph is running
# this part is the data that is plotted on the graph.. NOTE at the moment there is a
# 1 sec(unit) per scan assumption here since there is no time variable , it is plotting against
# record number; really need to plot against computer or ctd clock if rate is not 1 scan per second
# ie make use of ETstr created below

              if self.GraphRun :             
                  temp = float(block["Tstr"])

                  self.data["Pres"].append(-1.*float(block["Pstr"]))
                  self.data["Temp"].append(float(block["Tstr"]))
                  if self.RT_source:
                     if self.StartTime == 0:
                        self.StartTime = time.time()
                        
                     block["Et"] = str(time.time() - self.StartTime)

                  self.data["Et"].append(float(block["Et"]))


                  
                  
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
        if block["OK"] and self.MonitorRun:

           Rstr = '{:>5.4}'.format(str(self.SRate.get_rate(block["pres"])))
          
           self.p_text.Data_text.SetValue(block["Pstr"])
           self.t_text.Data_text.SetValue(block["Tstr"])
           self.c_text.Data_text.SetValue(block["Cstr"])
           self.s_text.Data_text.SetValue(block["Sstr"])
           self.d_text.Data_text.SetValue(block["Dstr"])
           self.f1_text.Data_text.SetValue(block["F1str"])
           self.f2_text.Data_text.SetValue(block["F2str"])
           self.l_text.Data_text.SetValue(block["Lstr"])
           self.v_text.Data_text.SetValue(block["Vstr"])
           self.r_text.Data_text.SetValue(Rstr)
           self.et_text.Data_text.SetValue('{:>5.4}'.format(block["Et"]))
#           self.ctd_clock_text.Data_text.SetValue(scan["ctdclock"])
        
           if self.GraphRun and self.runlogfile :
               self.ScanNum+=1
               xdatetime = '{:>8.8}'.format(str(datetime.datetime.now().time()))

               self.runlogfile.write(str(self.ScanNum)+" "+xdatetime+" "+'{:>5.4}'.format(block["Et"])+" "+block["Pstr"]+" "+block["Tstr"]+" "+block["Cstr"]+
                     " "+block["Sstr"]+" "+block["Dstr"]+ " "+block["F1str"]+" "+block["F2str"]+" "+block["Lstr"]+" "+block["Vstr"]+"\n")

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
            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
            
#

# pop up the wxterminal for interaction with ctd - THIS IS NOT WORKING YET NEEDS WORK
#    def on_term(self,event):

        self.ser.close()
#        wxTerminal.MyApp()
#        print "opening wx"
#        frame_terminal=wxTerminal.MyApp(0)
#        frame_terminal=wxTerminal_NAFC.TerminalFrame(self, -1, "")
#        print "Show modal"
#        self.SetTopWindow(frame_terminal)
#        frame_terminal.Show()
#        print "Destroying"
#        frame_terminal.Destroy()

# Realtime -> start  opens serial port and log file for realtime data

    def on_sendwake(self,event):
        if self.DataSource == None:

            if (CTD == "SBE"):
                self.DataSource = BST.SerialSource_SBE19p(self.ser, self.BQueue)
                self.DataSource.start()
            self.flash_status_message("Waking CTD")
            status = self.DataSource.Send_Wake()
            if status:
                self.flash_status_message("CTD AWAKE")
                self.m_initlogger.Enable(True)
                self.m_getctdstatus.Enable(True)
            else:
                self.flash_status_message("CTD **NOT** WAKING")


    def on_start_rt (self, event):

        self.LogFileName = self.save_file_dialog()  # get filename of desired logfile

        if self.LogFileName != None :
            self.flash_status_message("OPENING FILE FOR OUTPUT "+self.LogFileName)
            self.runlogfile = open(self.LogFileName,"w")
            self.WriteHeader(self.runlogfile)
        else:
            self.flash_status_message("NOT LOGGING TO FILE")
            self.LogFileName = "NOT LOGGING TO FILE"


        if self.DataSource == None:

            if (CTD == "SBE"):
                self.DataSource = BST.SerialSource_SBE19p(self.ser,self.BQueue)
                self.DataSource.start()

        if not self.DataSource.is_port_open() :
            self.message_box("Can Not Open Port- check settings")
            self.DataSource.shutdown()
            return()
        
# if we have an open port proceed     
        self.RT_source = True
            
        self.host.set_title('Bongo trace data file= '+self.LogFileName, size=8) # label plot

# now configure the CTD and start the data coming
        self.flash_status_message("Waking CTD")
        self.DataSource.Send_Wake()


#        self.on_get_ctd_status(-1)

        self.flash_status_message("SETTING CTD TO REAL TIME MODE")
        self.DataSource.send_Real()
#        self.interval = DEFAULT_RATE  # until there is a menu item to change it :-)
#        self.DataSource.send_Set_DataRate(str(self.interval))

        # starts ctd sending data ,but processing is paused until start_data_feed sent
#        self.flash_status_message("SENDING STARTNOW FOR DATA")
        self.DataSource.pause_data_feed()
#        self.DataSource.send_StartNow_Data()

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
        self.m_initlogger.Enable(True)
        self.m_getctdstatus.Enable(True)

        self.monitor_button.Enable(True)
        self.GraphRun_button.Enable(True)
        self.data["Pres"]=[0]
        self.data["Temp"]=[0]
        self.data["Et"]=[0]


# *****************************************************************

    def on_stop_rt (self, event):
        if self.MonitorRun:
             self.on_monitor_button(event)
        try:                  
              self.runlogfile.close()
        except: pass
        
        self.RT_source = False

        self.flash_status_message("STOPPING CTD DATA")
        self.DataSource.pause_data_feed()
#        self.DataSource.send_Stop_Data ()

#        self.DataSource.close_Port () shutdown will close the port
        if self.DataSource != None:
            self.DataSource.shut_down()
            self.DataSource = None


        self.port_open = False
        menubar = self.GetMenuBar()
        enabled = menubar.IsEnabled(ID_START_RT)
        menubar.Enable(ID_START_RT,not enabled)
        enabled = menubar.IsEnabled(ID_STOP_RT)
        menubar.Enable(ID_STOP_RT,not enabled)
        menubar.Enable(ID_SER_CONF, True)

        self.m_initlogger.Enable(False)
        self.m_getctdstatus.Enable(False)

#        menubar.EnableTop(2, True)  # re-enable archieved data option
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
#            self.datagen = DataGen2(FileName) #Create a data source instance
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
#        if self.RT_source == True:
#            self.on_stop_rt (1)
#        hdr_edit = WINAQU_Thread.winaqu_thread()
#        hdr_edit.start()
        WINAQU_GUI.main()



    def on_set_base_header(self,event):
        xx = ShipTrip_Dialog(self,self.hd1["SHIP"],self.hd1["TRIP"],self.hd1["STN"])


        xx.SetBase(self.hship,self.hd1["TRIP"],self.hd1["STN"])
        res=xx.ShowModal()
        if res == wx.ID_OK:

 
            self.hd1["SHIP"] = xx.GetShip()
            self.hship = xx.GetShip()
            self.hd1["TRIP"] = xx.GetTrip()
            self.hd1["STN"] = xx.GetStn()

            self.hship="LL"

            xx.Destroy()


#******************* assorted  methods ****************************************************

    def read_cfg(self, ser):
        try:
            with open('Bongo.CFG', 'r') as fp:
#                self.basename = fp.readline().rstrip()
#                self.make_SYTS(self.basename)
                self.comPort = fp.readline().rstrip()
                ser.port = self.comPort
                commsettings = json.load(fp)
            try:
                ser.apply_settings(commsettings)
            except:
                ser.applySettingsDict(commsettings)  # pyserial pre v 3.0

            fp.close()
        except:
            return (False)

        return (True)
        #            self.set_default_com_cfg()

    def save_cfg(self, ser):
        try:
            comsettings = ser.get_settings()
        except:
            comsettings = ser.getSettingsDict()  # pyserial pre v 30.0

        with open('Bongo.CFG', 'w') as fp:
#            fp.write(self.basename)
#            fp.write('\n')
            fp.write(ser.port)
            fp.write('\n')
            fp.write(json.dumps(comsettings))
        fp.close()

        # Configure serial port, requires our serial instance, make sure port is closed before calling

    def on_ser_config(self, event):
        dialog_serial_cfg = wxSerialConfigDialog.SerialConfigDialog(None, -1, "",
                                                                    show=wxSerialConfigDialog.SHOW_BAUDRATE | wxSerialConfigDialog.SHOW_FORMAT | wxSerialConfigDialog.SHOW_FLOW,
                                                                    serial=self.ser
                                                                    )
        result = dialog_serial_cfg.ShowModal()
        dialog_serial_cfg.Destroy()
        self.save_cfg(self.ser)


    def set_default_com_cfg(self,ser):  # Defaults as specified
        DEFAULT_COM = "COM1"
        DEFAULT_BAUD = 1200

        ser.port = DEFAULT_COM
        ser.baudrate = DEFAULT_BAUD
        ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        ser.parity = serial.PARITY_NONE  # set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        ser.timeout = 5  # timeout block read
        ser.xonxoff = True  # disable software flow control
        ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        ser.writeTimeout = 2  # timeout for write

    def WriteHeader (self,fp) :

        xtime = '{:>5.5}'.format(str(datetime.datetime.now().time()))
        xdate = '{:>12.12}'.format(str(datetime.datetime.now().date()))
        CTDID='S4018'
        hdr1_out= self.hd1["SHIP"].strip().zfill(2)+ self.hd1["TRIP"].strip().zfill(3)+ self.hd1["STN"].strip().zfill(3)
        fp.write("NAFC_Y2K_HEADER\n")
        fp.write (hdr1_out+"                    "+xdate+" "+xtime+"      "+CTDID+"     O                1\n")
        fp.write (hdr1_out+" 000000 01.00 A 12 #ZEPTCSM------------              000 0000 0000 000 4\n")
        fp.write (hdr1_out+"                                                                       8\n")
        fp.write ("SCAN CtdClk   ET   PRES    TEMP  COND   SAL   SIGMAT \n")
        fp.write ("-- DATA --\n")

    def on_init_logger(self,event):
        self.flash_status_message("Initiizing CTD - Deleting internal Stored casts")
        if self.ser.isOpen():
            if self.DataSource != None:
                self.DataSource.send_InitLogging()
                status = "OK"
            else:
                status = "Data Source not present"
        else :
            status = " DATASOURCE NOT OPEN"
        self.message_box(status)

    def on_get_ctd_status(self,event):
        self.flash_status_message("Getting CTD Status message (May take 20 seconds....)")
        if self.ser.isOpen():
            if self.DataSource != None:
                status = self.DataSource.Get_CTD_Status()
            else:
                status = "Data Source not present"
        else :
            status = " DATASOURCE NOT OPEN"
        self.message_box(status)

    def on_sendstop(self,event):
        self.flash_status_message("Sending a Blind STOP to CTD")
        if self.ser.isOpen():
            if self.DataSource != None:
                self.DataSource.send_Stop_Data()
                status = "OK - try a Get CTD Status to check"
            else:
                status = "Data Source not present"
        else :
            status = " DATASOURCE NOT OPEN"
        self.message_box(status)


    def on_exit(self, event):
        if self.runlogfile != None:
          self.runlogfile.close()
        self.redraw_timer.Stop()
        if self.ser.isOpen():
            if self.DataSource != None:
                  self.DataSource.shut_down()
            self.ser.close()
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

#    def Confirm_dialogue(self, event):
#        dlg = wx.MessageDialog(self, "Real-time data not Running.\nOpening feed from Scanmar",
#                               "When data seen on screen please retry IN WATER button", wx.OK | wx.ICON_QUESTION)
#        if dlg.ShowModal() == wx.ID_OK:
#            return (True)
#        else:
#            return (False)



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
                return self.ship.GetValue()
    def GetTrip(self):
                return self._trip.GetValue()
    def GetStn(self):
                return self._stn.GetValue()
    

#***************************************************************************************

#####################################  MAIN ENTRY POINT ################################        
if __name__ == '__main__':

    app = wx.App()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
###################################### END OF CODE #####################################
