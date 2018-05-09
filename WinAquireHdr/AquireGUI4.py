# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
#from WinAquireHdr.AquireGUI_Validate import IntRangeValidator
from WinAquireHdr.AquireGUI_Validate import IntRangeValidator
###########################################################################
## Class HDR_DIALOG
###########################################################################

class HDR_DIALOG ( wx.Dialog ):
        
        def __init__( self, parent ):
                wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"WinAquire Header Editor", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
                
                self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
                self.SetBackgroundColour( wx.Colour( 208, 208, 208 ) )
                
                FULL_PAGE = wx.FlexGridSizer( 3, 1, 0, 0 )
                FULL_PAGE.SetFlexibleDirection( wx.BOTH )
                FULL_PAGE.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                fgSizer151 = wx.FlexGridSizer( 3, 1, 0, 0 )
                fgSizer151.SetFlexibleDirection( wx.BOTH )
                fgSizer151.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                fgSizer16 = wx.FlexGridSizer( 3, 1, 0, 0 )
                fgSizer16.SetFlexibleDirection( wx.BOTH )
                fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                SHPTRPSTN_GRID = wx.FlexGridSizer( 1, 7, 0, 0 )
                SHPTRPSTN_GRID.SetFlexibleDirection( wx.BOTH )
                SHPTRPSTN_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.CARD1_LABEL = wx.StaticText( self, wx.ID_ANY, u"NAFC_BPO_CARD 1 HEADER:", wx.DefaultPosition, wx.Size( 230,-1 ), wx.ALIGN_RIGHT )
                self.CARD1_LABEL.Wrap( -1 )
                self.CARD1_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.CARD1_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.SHIP_LABEL1 = wx.StaticText( self, wx.ID_ANY, u"SHIP_ID :", wx.DefaultPosition, wx.Size( 180,-1 ), wx.ALIGN_RIGHT )
                self.SHIP_LABEL1.Wrap( -1 )
                self.SHIP_LABEL1.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.SHIP_LABEL1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.SHIP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), wx.TE_READONLY )
                self.SHIP.SetMaxLength( 2 ) 
                self.SHIP.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.SHIP, 0, wx.ALL, 5 )
                
                self.TRIP_LABEL = wx.StaticText( self, wx.ID_ANY, u"TRIP :", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_RIGHT )
                self.TRIP_LABEL.Wrap( -1 )
                self.TRIP_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.TRIP_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.TRIP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), wx.TE_READONLY )
                self.TRIP.SetMaxLength( 3 ) 
                self.TRIP.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.TRIP, 0, wx.ALL, 5 )
                
                self.STATION_LABEL = wx.StaticText( self, wx.ID_ANY, u"STATION :", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
                self.STATION_LABEL.Wrap( -1 )
                self.STATION_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.STATION_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.STN = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), wx.TE_READONLY )
                self.STN.SetMaxLength( 3 ) 
                self.STN.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                SHPTRPSTN_GRID.Add( self.STN, 0, wx.ALL, 5 )
                
                
                fgSizer16.Add( SHPTRPSTN_GRID, 1, wx.EXPAND, 5 )
                
                MAIN_ENTER_GRID = wx.FlexGridSizer( 1, 2, 0, 0 )
                MAIN_ENTER_GRID.SetFlexibleDirection( wx.BOTH )
                MAIN_ENTER_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                LEFT_COL_GRID = wx.FlexGridSizer( 6, 1, 0, 0 )
                LEFT_COL_GRID.SetFlexibleDirection( wx.BOTH )
                LEFT_COL_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.LEF_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
                LEFT_COL_GRID.Add( self.LEF_staticline, 0, wx.EXPAND |wx.ALL, 5 )
                
                self.STATION_META_DATA = wx.StaticText( self, wx.ID_ANY, u"STATION META-DATA", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
                self.STATION_META_DATA.Wrap( -1 )
                self.STATION_META_DATA.SetFont( wx.Font( 12, 74, 93, 92, True, "Arial" ) )
                self.STATION_META_DATA.SetMinSize( wx.Size( 340,-1 ) )
                
                LEFT_COL_GRID.Add( self.STATION_META_DATA, 0, wx.ALL, 5 )
                
                LAT_LON_GRID = wx.FlexGridSizer( 2, 5, 0, 0 )
                LAT_LON_GRID.SetFlexibleDirection( wx.BOTH )
                LAT_LON_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.LAT_LABEL = wx.StaticText( self, wx.ID_ANY, u"LATITUDE :     +", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.LAT_LABEL.Wrap( -1 )
                self.LAT_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.LAT_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.LATD = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), 0,validator = IntRangeValidator("0","90") )
                self.LATD.SetMaxLength( 2 ) 
                self.LATD.SetExtraStyle( wx.WS_EX_VALIDATE_RECURSIVELY )
                self.LATD.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.LATD, 0, wx.ALL, 5 )
                
                self.DEG_LAT_LABEL = wx.StaticText( self, wx.ID_ANY, u"°", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.DEG_LAT_LABEL.Wrap( -1 )
                self.DEG_LAT_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.DEG_LAT_LABEL, 0, wx.ALL, 5 )
                
                self.LATM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0,validator = IntRangeValidator("0","60") )
                self.LATM.SetMaxLength( 5 ) 
                self.LATM.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.LATM, 0, wx.ALL, 5 )
                
                self.MINUTES_LAT_LABEL = wx.StaticText( self, wx.ID_ANY, u"'", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.MINUTES_LAT_LABEL.Wrap( -1 )
                self.MINUTES_LAT_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.MINUTES_LAT_LABEL, 0, wx.ALL, 5 )
                
                self.LONGITUDE_LABEL = wx.StaticText( self, wx.ID_ANY, u"LONGITUDE : -0", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.LONGITUDE_LABEL.Wrap( -1 )
                self.LONGITUDE_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.LONGITUDE_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.LOND = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.LOND.SetMaxLength( 2 ) 
                self.LOND.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.LOND, 0, wx.ALL, 5 )
                
                self.DEGLONG_LABEL = wx.StaticText( self, wx.ID_ANY, u"°", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.DEGLONG_LABEL.Wrap( -1 )
                self.DEGLONG_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.DEGLONG_LABEL, 0, wx.ALL, 5 )
                
                self.LONM = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0,validator = IntRangeValidator("0","60") )
                self.LONM.SetMaxLength( 5 ) 
                self.LONM.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.LONM, 0, wx.ALL, 5 )
                
                self.MIN_LONG_LABEL = wx.StaticText( self, wx.ID_ANY, u"'", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.MIN_LONG_LABEL.Wrap( -1 )
                self.MIN_LONG_LABEL.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                LAT_LON_GRID.Add( self.MIN_LONG_LABEL, 0, wx.ALL, 5 )
                
                
                LEFT_COL_GRID.Add( LAT_LON_GRID, 1, wx.EXPAND, 5 )
                
                TIME_GRID = wx.FlexGridSizer( 2, 6, 0, 0 )
                TIME_GRID.SetFlexibleDirection( wx.BOTH )
                TIME_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.YEAR_LABEL = wx.StaticText( self, wx.ID_ANY, u"YEAR :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.YEAR_LABEL.Wrap( -1 )
                self.YEAR_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.YEAR_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.YEAR = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0,validator = IntRangeValidator("0","2030") )
                self.YEAR.SetMaxLength( 4 ) 
                self.YEAR.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.YEAR, 0, wx.ALL, 5 )
                
                self.HYPH1 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.HYPH1.Wrap( -1 )
                self.HYPH1.SetFont( wx.Font( 14, 70, 90, 92, False, "Arial" ) )
                
                TIME_GRID.Add( self.HYPH1, 0, wx.ALL, 5 )
                
                self.MONTH = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0,validator = IntRangeValidator("0","12") )
                self.MONTH.SetMaxLength( 2 ) 
                self.MONTH.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.MONTH, 0, wx.ALL, 5 )
                
                self.HYPH2 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.HYPH2.Wrap( -1 )
                self.HYPH2.SetFont( wx.Font( 14, 70, 90, 92, False, "Arial" ) )
                
                TIME_GRID.Add( self.HYPH2, 0, wx.ALL, 5 )
                
                self.DAY = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 38,-1 ), 0,validator = IntRangeValidator("0","31") )
                self.DAY.SetMaxLength( 2 ) 
                self.DAY.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.DAY, 0, wx.ALL, 5 )
                
                self.HOUR_LABEL = wx.StaticText( self, wx.ID_ANY, u"HOUR :", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
                self.HOUR_LABEL.Wrap( -1 )
                self.HOUR_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.HOUR_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.HOUR = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.Size( 35,-1 ), 0,validator = IntRangeValidator("0","23") )
                self.HOUR.SetMaxLength( 2 ) 
                self.HOUR.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )

                
                TIME_GRID.Add( self.HOUR, 0, wx.ALL, 5 )
                
                self.MINS_T_LABEL = wx.StaticText( self, wx.ID_ANY, u":", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
                self.MINS_T_LABEL.Wrap( -1 )
                self.MINS_T_LABEL.SetFont( wx.Font( 14, 70, 90, 92, False, "Arial" ) )
                
                TIME_GRID.Add( self.MINS_T_LABEL, 0, wx.ALL, 5 )
                
                self.MINUTES = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0,validator = IntRangeValidator("0","59") )
                self.MINUTES.SetMaxLength( 2 ) 
                self.MINUTES.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.MINUTES, 0, wx.ALL, 5 )
                
                self.DUMMY = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
                self.DUMMY.Wrap( -1 )
                TIME_GRID.Add( self.DUMMY, 0, wx.ALL, 5 )
                
                self.GMT = wx.StaticText( self, wx.ID_ANY, u"GMT", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT|wx.ALIGN_RIGHT )
                self.GMT.Wrap( -1 )
                self.GMT.SetFont( wx.Font( 12, 74, 93, 90, False, "Arial" ) )
                
                TIME_GRID.Add( self.GMT, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                
                LEFT_COL_GRID.Add( TIME_GRID, 1, wx.EXPAND, 5 )
                
                OTHER_DATA_GRID = wx.FlexGridSizer( 5, 2, 0, 0 )
                OTHER_DATA_GRID.SetFlexibleDirection( wx.BOTH )
                OTHER_DATA_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.BOTTOM_LABEL = wx.StaticText( self, wx.ID_ANY, u"BOTTOM DEPTH (M) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.BOTTOM_LABEL.Wrap( -1 )
                self.BOTTOM_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.BOTTOM_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.DEPTH = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0,validator = IntRangeValidator("0","6000") )
                self.DEPTH.SetMaxLength( 4 ) 
                self.DEPTH.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.DEPTH, 0, wx.ALL, 5 )
                
                self.PROBE_TYPE_LABEL = wx.StaticText( self, wx.ID_ANY, u"PROBE TYPE :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.PROBE_TYPE_LABEL.Wrap( -1 )
                self.PROBE_TYPE_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.PROBE_TYPE_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.PROBE = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 68,-1 ), wx.TE_READONLY )
                self.PROBE.SetMaxLength( 5 ) 
                self.PROBE.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.PROBE, 0, wx.ALL, 5 )
                
                self.FISHSET_LABEL = wx.StaticText( self, wx.ID_ANY, u"FISH SET # :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.FISHSET_LABEL.Wrap( -1 )
                self.FISHSET_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.FISHSET_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.FISHSET = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0,validator = IntRangeValidator("0","999") )
                self.FISHSET.SetMaxLength( 3 ) 
                self.FISHSET.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.FISHSET, 0, wx.ALL, 5 )
                
                self.FORMAT_LABEL = wx.StaticText( self, wx.ID_ANY, u"PROFILE FORMAT :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.FORMAT_LABEL.Wrap( -1 )
                self.FORMAT_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.FORMAT_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.FORMAT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
                self.FORMAT.SetMaxLength( 1 ) 
                self.FORMAT.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.FORMAT, 0, wx.ALL, 5 )
                
                self.COMM_LABEL = wx.StaticText( self, wx.ID_ANY, u"COMMENT (14CHR) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.COMM_LABEL.Wrap( -1 )
                self.COMM_LABEL.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.COMM_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.COMMENT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
                self.COMMENT.SetMaxLength( 14 ) 
                self.COMMENT.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                OTHER_DATA_GRID.Add( self.COMMENT, 0, wx.ALL, 5 )
                
                
                LEFT_COL_GRID.Add( OTHER_DATA_GRID, 1, wx.EXPAND, 5 )
                
                fgSizer18 = wx.FlexGridSizer( 1, 2, 0, 0 )
                fgSizer18.SetFlexibleDirection( wx.BOTH )
                fgSizer18.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.FileName_Label = wx.StaticText( self, wx.ID_ANY, u"FILE=", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.FileName_Label.Wrap( -1 )
                self.FileName_Label.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
                
                fgSizer18.Add( self.FileName_Label, 0, wx.ALL, 5 )
                
                self.FileName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_READONLY )
                self.FileName.SetFont( wx.Font( 8, 74, 90, 90, False, "Arial" ) )
                self.FileName.SetMinSize( wx.Size( 286,-1 ) )
 		
                fgSizer18.Add( self.FileName, 0, wx.ALL, 5 )
                
                
                LEFT_COL_GRID.Add( fgSizer18, 1, wx.EXPAND, 5 )
                
                
                MAIN_ENTER_GRID.Add( LEFT_COL_GRID, 1, wx.EXPAND, 5 )
                
                RIGHT_COL_GRID = wx.FlexGridSizer( 2, 2, 0, 0 )
                RIGHT_COL_GRID.SetFlexibleDirection( wx.BOTH )
                RIGHT_COL_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.RIGHT_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
                RIGHT_COL_GRID.Add( self.RIGHT_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
                
                self.RIGHT_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
                RIGHT_COL_GRID.Add( self.RIGHT_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
                
                METEROLOGY1 = wx.FlexGridSizer( 3, 1, 0, 0 )
                METEROLOGY1.SetFlexibleDirection( wx.BOTH )
                METEROLOGY1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.METEOROLOGY_LABEL = wx.StaticText( self, wx.ID_ANY, u"METEOROLOGY DATA", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
                self.METEOROLOGY_LABEL.Wrap( -1 )
                self.METEOROLOGY_LABEL.SetFont( wx.Font( 12, 74, 93, 92, True, "Arial" ) )
                self.METEOROLOGY_LABEL.SetMinSize( wx.Size( 340,-1 ) )
                
                METEROLOGY1.Add( self.METEOROLOGY_LABEL, 0, wx.ALL, 5 )
                
                fgSizer24 = wx.FlexGridSizer( 3, 1, 0, 0 )
                fgSizer24.SetFlexibleDirection( wx.BOTH )
                fgSizer24.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                fgSizer27 = wx.FlexGridSizer( 1, 2, 0, 0 )
                fgSizer27.SetFlexibleDirection( wx.BOTH )
                fgSizer27.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.AIR_LABEL = wx.StaticText( self, wx.ID_ANY, u"AIR", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
                self.AIR_LABEL.Wrap( -1 )
                self.AIR_LABEL.SetFont( wx.Font( 12, 74, 90, 92, True, "Arial" ) )
                self.AIR_LABEL.SetMinSize( wx.Size( 180,-1 ) )
                
                fgSizer27.Add( self.AIR_LABEL, 0, wx.ALL, 5 )
                
                self.WATER_LABEL = wx.StaticText( self, wx.ID_ANY, u"WATER", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
                self.WATER_LABEL.Wrap( -1 )
                self.WATER_LABEL.SetFont( wx.Font( 12, 74, 90, 92, True, "Arial" ) )
                self.WATER_LABEL.SetMinSize( wx.Size( 175,-1 ) )
                
                fgSizer27.Add( self.WATER_LABEL, 0, wx.ALL, 5 )
                
                
                fgSizer24.Add( fgSizer27, 1, wx.EXPAND, 5 )
                
                fgSizer15 = wx.FlexGridSizer( 1, 2, 0, 0 )
                fgSizer15.SetFlexibleDirection( wx.BOTH )
                fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                AIR_GRID = wx.FlexGridSizer( 9, 2, 0, 0 )
                AIR_GRID.SetFlexibleDirection( wx.BOTH )
                AIR_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.CLOUD_LABEL = wx.StaticText( self, wx.ID_ANY, u"CLOUD (1-9-/) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.CLOUD_LABEL.Wrap( -1 )
                self.CLOUD_LABEL.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.CLOUD_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.CLOUD = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","9") )
                self.CLOUD.SetMaxLength( 1 ) 
                self.CLOUD.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.CLOUD, 0, wx.ALL, 5 )
                
                self.WINDDIR_LABEL = wx.StaticText( self, wx.ID_ANY, u"WIND DIR (°/10) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.WINDDIR_LABEL.Wrap( -1 )
                self.WINDDIR_LABEL.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.WINDDIR_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.WINDDIR = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0,validator = IntRangeValidator("0","36") )
                self.WINDDIR.SetMaxLength( 2 ) 
                self.WINDDIR.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.WINDDIR, 0, wx.ALL, 5 )
                
                self.WINDSPD_LABEL = wx.StaticText( self, wx.ID_ANY, u"WIND SPEED (Knts) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.WINDSPD_LABEL.Wrap( -1 )
                self.WINDSPD_LABEL.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.WINDSPD_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.WINDSPD = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.WINDSPD.SetMaxLength( 2 ) 
                self.WINDSPD.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.WINDSPD, 0, wx.ALL, 5 )
                
                self.WW_CODE_LABEL = wx.StaticText( self, wx.ID_ANY, u"WW CODE :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.WW_CODE_LABEL.Wrap( -1 )
                AIR_GRID.Add( self.WW_CODE_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.WWCODE = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.WWCODE.SetMaxLength( 2 ) 
                self.WWCODE.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.WWCODE, 0, wx.ALL, 5 )
                
                self.AIRPRES_LABEL = wx.StaticText( self, wx.ID_ANY, u"AIR PRES. (mb) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.AIRPRES_LABEL.Wrap( -1 )
                AIR_GRID.Add( self.AIRPRES_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.AIRPRES = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,-1 ), 0,validator = IntRangeValidator("0","1400") )
                self.AIRPRES.SetMaxLength( 6 ) 
                self.AIRPRES.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.AIRPRES, 0, wx.ALL, 5 )
                
                self.AIRTEMPDRY_LABEL = wx.StaticText( self, wx.ID_ANY, u"AIR TEMP DRY (°C) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.AIRTEMPDRY_LABEL.Wrap( -1 )
                AIR_GRID.Add( self.AIRTEMPDRY_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.DRYTEMP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0,validator = IntRangeValidator("-45","45") )
                self.DRYTEMP.SetMaxLength( 5 ) 
                self.DRYTEMP.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.DRYTEMP, 0, wx.ALL, 5 )
                
                self.AIRTEMPWET_LABEL = wx.StaticText( self, wx.ID_ANY, u"AIR TEMP WET (°C) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.AIRTEMPWET_LABEL.Wrap( -1 )
                AIR_GRID.Add( self.AIRTEMPWET_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.WETTEMP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 ,validator = IntRangeValidator("-45","45"))
                self.WETTEMP.SetMaxLength( 5 ) 
                self.WETTEMP.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                AIR_GRID.Add( self.WETTEMP, 0, wx.ALL, 5 )
                
                
                fgSizer15.Add( AIR_GRID, 1, wx.EXPAND, 5 )
                
                WATER_GRID = wx.FlexGridSizer( 9, 2, 0, 0 )
                WATER_GRID.SetFlexibleDirection( wx.BOTH )
                WATER_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.WAVEPERIOD_LABEL = wx.StaticText( self, wx.ID_ANY, u"WAVE PERIOD (SEC) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.WAVEPERIOD_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.WAVEPERIOD_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.WAVEP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.WAVEP.SetMaxLength( 2 ) 
                self.WAVEP.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.WAVEP, 0, wx.ALL, 5 )
                
                self.WAVE_H_LABEL = wx.StaticText( self, wx.ID_ANY, u"WAVE HEIGHT (x½m)  :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.WAVE_H_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.WAVE_H_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.WAVEH = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.WAVEH.SetMaxLength( 2 ) 
                self.WAVEH.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.WAVEH, 0, wx.ALL, 5 )
                
                self.SWELLDIR_LABEL = wx.StaticText( self, wx.ID_ANY, u"SWELL DIR (°/10) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.SWELLDIR_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.SWELLDIR_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.SWELLD = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","36") )
                self.SWELLD.SetMaxLength( 2 ) 
                self.SWELLD.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.SWELLD, 0, wx.ALL, 5 )
                
                self.SWELLPERIOD_LABEL = wx.StaticText( self, wx.ID_ANY, u"SWELL PERIOD (s) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.SWELLPERIOD_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.SWELLPERIOD_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.SWELLP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.SWELLP.SetMaxLength( 2 ) 
                self.SWELLP.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.SWELLP, 0, wx.ALL, 5 )
                
                self.SWELL_H_LABEL = wx.StaticText( self, wx.ID_ANY, u"SWELL HEIGHT (x½m) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.SWELL_H_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.SWELL_H_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.SWELLH = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","99") )
                self.SWELLH.SetMaxLength( 2 ) 
                self.SWELLH.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.SWELLH, 0, wx.ALL, 5 )
                
                self.ICE_CONC_LABEL = wx.StaticText( self, wx.ID_ANY, u"ICE CONC. (1/10s) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.ICE_CONC_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.ICE_CONC_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.ICECONC = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","9") )
                self.ICECONC.SetMaxLength( 1 ) 
                self.ICECONC.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.ICECONC, 0, wx.ALL, 5 )
                
                self.ICESTAGE_LABEL = wx.StaticText( self, wx.ID_ANY, u"ICE STAGE (0-9/) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.ICESTAGE_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.ICESTAGE_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.ICESTAGE = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","9") )
                self.ICESTAGE.SetMaxLength( 1 ) 
                self.ICESTAGE.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.ICESTAGE, 0, wx.ALL, 5 )
                
                self.BERGS_LABEL = wx.StaticText( self, wx.ID_ANY, u"BERGS (#) (0-9/) :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.BERGS_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.BERGS_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.NBERGS = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","9") )
                self.NBERGS.SetMaxLength( 1 ) 
                self.NBERGS.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.NBERGS, 0, wx.ALL, 5 )
                
                self.SITnTREND_LABEL = wx.StaticText( self, wx.ID_ANY, u"SIT and TREND :", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.SITnTREND_LABEL.Wrap( -1 )
                WATER_GRID.Add( self.SITnTREND_LABEL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
                
                self.SandT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0,validator = IntRangeValidator("0","9") )
                self.SandT.SetMaxLength( 1 ) 
                self.SandT.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                WATER_GRID.Add( self.SandT, 0, wx.ALL, 5 )
                
                
                fgSizer15.Add( WATER_GRID, 1, wx.EXPAND, 5 )
                
                
                fgSizer24.Add( fgSizer15, 1, wx.EXPAND, 5 )
                
                BUTTONS_GRID = wx.FlexGridSizer( 0, 3, 0, 0 )
                BUTTONS_GRID.SetFlexibleDirection( wx.BOTH )
                BUTTONS_GRID.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                self.ClearButton = wx.Button( self, wx.ID_CANCEL, u"Clear All", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.ClearButton.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                BUTTONS_GRID.Add( self.ClearButton, 0, wx.ALL, 5 )
                
                self.Save_n_Exit_Button = wx.Button( self, wx.ID_ANY, u"Save and Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.Save_n_Exit_Button.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                BUTTONS_GRID.Add( self.Save_n_Exit_Button, 0, wx.ALL, 5 )
                
                self.QuitButton = wx.Button( self, wx.ID_ANY, u"Quit", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.QuitButton.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
                
                BUTTONS_GRID.Add( self.QuitButton, 0, wx.ALL, 5 )
                
                
                fgSizer24.Add( BUTTONS_GRID, 1, wx.EXPAND, 5 )
                
                
                METEROLOGY1.Add( fgSizer24, 1, wx.EXPAND, 5 )
                
                
                RIGHT_COL_GRID.Add( METEROLOGY1, 1, wx.EXPAND, 5 )
                
                
                MAIN_ENTER_GRID.Add( RIGHT_COL_GRID, 1, wx.EXPAND, 5 )
                
                
                fgSizer16.Add( MAIN_ENTER_GRID, 1, wx.EXPAND, 5 )
                
                
                fgSizer151.Add( fgSizer16, 1, wx.EXPAND, 5 )
                
                
                FULL_PAGE.Add( fgSizer151, 1, wx.EXPAND, 5 )
                
                
                self.SetSizer( FULL_PAGE )
                self.Layout()
                FULL_PAGE.Fit( self )
                
                self.Centre( wx.BOTH )
                
                # Connect Events
                self.Bind( wx.EVT_CLOSE, self.OnClose )
                self.ClearButton.Bind( wx.EVT_BUTTON, self.clearFunc )
                self.Save_n_Exit_Button.Bind( wx.EVT_BUTTON, self.SaveNExit )
                self.QuitButton.Bind( wx.EVT_BUTTON, self.OnClose )

################ ALLOW ENTER KEY TO FUNCTION THE SAME AS TAB KEY
                return_id = wx.NewId()
                acc_table = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_RETURN, return_id)])
                self.SetAcceleratorTable(acc_table)
#                wx.EVT_MENU(self, return_id, self.on_return)
                self.Bind(wx.EVT_MENU, self.on_return, id=return_id)
                self.Centre( wx.BOTH )
        def on_return(self, event):
                ctl = wx.Window.FindFocus()
                ctl.Navigate()
# self.SetAcceleratorTable(wx.NullAcceleratorTable)
############
        
        def __del__( self ):
                pass
        
        
        # Virtual event handlers, overide them in your derived class
        def OnClose( self, event ):
                event.Skip()
        
        def clearFunc( self, event ):
                event.Skip()
        
        def SaveNExit( self, event ):
                event.Skip()
        
        

