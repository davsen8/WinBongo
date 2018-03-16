
import wx
import os,sys
 
#import the created GUI file and Parser
import AquireGUI4
import ParseNafcHdr

 
#inherit from the MainFrame created in wxFowmBuilder and create CalcFrame
class EditHdr(AquireGUI4.HDR_DIALOG):
    #constructor
    def __init__(self,parent,filename,Hdr1dict,Hdr8dict):
        #initialize parent class        
        AquireGUI4.HDR_DIALOG.__init__(self,parent)
        
        self.afileNpath=filename 
        self.Hdr1=Hdr1dict
        self.Hdr8=Hdr8dict
        self.LoadHdrFunc(self.afileNpath)


        
# file the form with contents from file
    def LoadHdrFunc(self,afileNpath):
        self.FileName.SetValue(afileNpath)
        self.SHIP.SetValue(self.Hdr1['SHIP'])
        self.TRIP.SetValue(self.Hdr1['TRIP'])
        self.STN.SetValue(self.Hdr1['STN'])
        self.LATD.SetValue(self.Hdr1['LATD'].replace(" ",""))
        self.LATM.SetValue(self.Hdr1['LATM'].replace(" ",""))
        self.LOND.SetValue(self.Hdr1['LOND'].replace(" ",""))
        self.LONM.SetValue(self.Hdr1['LONM'].replace(" ",""))
        self.YEAR.SetValue(self.Hdr1['YEAR'].replace(" ",""))
        self.MONTH.SetValue(self.Hdr1['MONTH'].replace(" ",""))
        self.DAY.SetValue(self.Hdr1['DAY'].replace(" ",""))
        self.HOUR.SetValue(self.Hdr1['HOUR'].replace(" ",""))
        self.MINUTES.SetValue(self.Hdr1['MINUTE'].replace(" ",""))
        self.DEPTH.SetValue(self.Hdr1['DEPTH'].replace(" ",""))
        self.PROBE.SetValue(self.Hdr1['PROBE'])
        self.FISHSET.SetValue(self.Hdr1['FISHSET'].replace(" ",""))
        self.FORMAT.SetValue(self.Hdr1['FORMAT'].replace(" ",""))
        self.COMMENT.SetValue(self.Hdr1['COMMENT'])
        
        self.CLOUD.SetValue(self.Hdr8['CLOUD'].replace(" ",""))
        self.WINDDIR.SetValue(self.Hdr8['WINDDIR'].replace(" ",""))
        self.WINDSPD.SetValue(self.Hdr8['WINDSPD'].replace(" ",""))
        self.WWCODE.SetValue(self.Hdr8['WWCODE'].replace(" ",""))
        self.AIRPRES.SetValue(self.Hdr8['AIRPRES'].replace(" ",""))
        self.DRYTEMP.SetValue(self.Hdr8['DRYTEMP'].replace(" ",""))
        self.WETTEMP.SetValue(self.Hdr8['WETTEMP'].replace(" ",""))
        self.WAVEP.SetValue(self.Hdr8['WAVEP'].replace(" ",""))
        self.WAVEH.SetValue(self.Hdr8['WAVEH'].replace(" ",""))
        self.SWELLD.SetValue(self.Hdr8['SWELLD'].replace(" ",""))
        self.SWELLP.SetValue(self.Hdr8['SWELLP'].replace(" ",""))
        self.SWELLH.SetValue(self.Hdr8['SWELLH'].replace(" ",""))
        self.ICECONC.SetValue(self.Hdr8['ICECONC'].replace(" ",""))
        self.ICESTAGE.SetValue(self.Hdr8['ICESTAGE'].replace(" ",""))
        self.NBERGS.SetValue(self.Hdr8['NBERGS'].replace(" ",""))
        self.SandT.SetValue(self.Hdr8['SandT'].replace(" ",""))

################################################## N/A

#put a blank string in text when 'Clear' button is clicked
    def clearFunc(self,event):
#        self.SHIP.SetValue(str(''))
#        self.TRIP.SetValue(str(''))
#        self.STN.SetValue(str(''))
        self.LATD.SetValue(str(''))
        self.LATM.SetValue(str(''))
        self.LOND.SetValue(str(''))
        self.LONM.SetValue(str(''))
        self.YEAR.SetValue(str(''))
        self.MONTH.SetValue(str(''))
        self.DAY.SetValue(str(''))
        self.HOUR.SetValue(str(''))
        self.MINUTES.SetValue(str(''))
        self.DEPTH.SetValue(str(''))
#        self.PROBE.SetValue(str(''))
        self.FISHSET.SetValue(str(''))
        self.FORMAT.SetValue(str(''))
        self.COMMENT.SetValue(str(''))
        self.CLOUD.SetValue(str(''))
        self.WINDDIR.SetValue(str(''))
        self.WINDSPD.SetValue(str(''))
        self.WWCODE.SetValue(str(''))
        self.AIRPRES.SetValue(str(''))
        self.DRYTEMP.SetValue(str(''))
        self.WETTEMP.SetValue(str(''))
        self.WAVEP.SetValue(str(''))
        self.WAVEH.SetValue(str(''))
        self.SWELLD.SetValue(str(''))
        self.SWELLP.SetValue(str(''))
        self.SWELLH.SetValue(str(''))
        self.ICECONC.SetValue(str(''))
        self.ICESTAGE.SetValue(str(''))
        self.NBERGS.SetValue(str(''))
        self.SandT.SetValue(str(''))

# palce form data back into transfer dict structures, called from SavenExit
    def WriteBackHdr(self):

        self.Hdr1['SHIP']=self.SHIP.GetValue()
        self.Hdr1['TRIP']=self.TRIP.GetValue()
        self.Hdr1['STN']=self.STN.GetValue()
        self.Hdr1['LATD']=self.LATD.GetValue()
        self.Hdr1['LATM']=self.LATM.GetValue()
        self.Hdr1['LOND']=self.LOND.GetValue()
        self.Hdr1['LONM']=self.LONM.GetValue()
        self.Hdr1['YEAR']=self.YEAR.GetValue()
        self.Hdr1['MONTH']=self.MONTH.GetValue()
        self.Hdr1['DAY']=self.DAY.GetValue()
        self.Hdr1['HOUR']=self.HOUR.GetValue()
        self.Hdr1['MINUTES']=self.MINUTES.GetValue()
        self.Hdr1['DEPTH']=self.DEPTH.GetValue()
        self.Hdr1['PROBE']=self.PROBE.GetValue()
        self.Hdr1['FISHSET']=self.FISHSET.GetValue()
        self.Hdr1['FORMAT']=self.FORMAT.GetValue()
        self.Hdr1['COMMENT']=self.COMMENT.GetValue()
        
        self.Hdr8['CLOUD']=self.CLOUD.GetValue()
        self.Hdr8['WINDDIR']=self.WINDDIR.GetValue()
        self.Hdr8['WINDSPD']=self.WINDSPD.GetValue()
        self.Hdr8['WWCODE']=self.WWCODE.GetValue()
        self.Hdr8['AIRPRES']=self.AIRPRES.GetValue()
        self.Hdr8['DRYTEMP']=self.DRYTEMP.GetValue()
        self.Hdr8['WETTEMP']=self.WETTEMP.GetValue()
        self.Hdr8['WAVEP']=self.WAVEP.GetValue()
        self.Hdr8['WAVEH']=self.WAVEH.GetValue()
        self.Hdr8['SWELLD']=self.SWELLD.GetValue()
        self.Hdr8['SWELLP']=self.SWELLP.GetValue()
        self.Hdr8['SWELLH']=self.SWELLH.GetValue()
        self.Hdr8['ICECONC']=self.ICECONC.GetValue()
        self.Hdr8['ICESTAGE']=self.ICESTAGE.GetValue()
        self.Hdr8['NBERGS']=self.NBERGS.GetValue()
        self.Hdr8['SandT']=self.SandT.GetValue()

        
# if saving call WritenackHdrs  and assigns to variable in the global space ie back
#to the parent to say YES data changed
    def SaveNExit(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to Save and Close this application?",
            "Confirm Save changes and Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()

        dlg.Destroy()
        if result == wx.ID_OK:
            self.WriteBackHdr()
            globals()["DataChanged"] = True
            self.Destroy()
 
# this actually quits, no changes and assigns to variable in the global space ie back
#to the parent to say NO data changed
    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application and discard changes?",
            "Confirm Quit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            globals()["DataChanged"] = False
            self.Destroy()
######################### END OF CLASS EDIT #########################
#####################################################################

def get_file_dialog():
        filename = None

        wildcard = "NAFC Dfile (*.d*)|*.d*|" "NAFC Pfile (*.p*)|*.p*|" \
        "MK21 Xbt File (*.edf)|*.edf|" "All files (*.*)|*.*"

        dialog = wx.FileDialog(None, message="Choose a file", defaultDir=os.getcwd(), wildcard=wildcard,style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            filename =  dialog.GetPath()
    
        dialog.Destroy()
        return(filename)
#####################################################################
def main ():

# Borrowed from ParseNafcHdr main , to get things going, need to review this further
# to hold the file header card strings , that are read from or written to the file
  cards=dict(h0="",h1="",h4="",h8="")
                
# to hold the parsed header card elements, this are assigned to from the form
  hdr0dict=dict()
  hdr1dict=dict()
  hdr4dict=dict()
  hdr8dict=dict()
  HdrDicts=dict(hdr0=hdr0dict,hdr1=hdr1dict,hdr4=hdr4dict,hdr8=hdr8dict)
  afiletype=""
  global DataChanged

  DataChanges = False
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
  app = wx.App(False)

#  args = sys.argv

# check for a command line filename, for now assume it is a NAFC file
  if len(sys.argv)>1 :
        infilename=sys.argv[1]
  else:
        infilename = get_file_dialog()
#  wx.Exit()
  
  if infilename==None:
       print ("No file name provided or selected.. aborting" )
       exit()
  afiletype = ParseNafcHdr.FileTypeIs(infilename)

   
  if  afiletype == "NAFC_Y2K_HEADER":
      f=open(infilename,"r+")
      if ParseNafcHdr.Read_NAFC_File_Hdr(f,cards):
         ParseNafcHdr.Parse_NAFC_Hdr1(cards,HdrDicts["hdr1"])
         ParseNafcHdr.Parse_NAFC_Hdr4(cards,HdrDicts["hdr4"])
         ParseNafcHdr.Parse_NAFC_Hdr8(cards,HdrDicts["hdr8"])
         f.close()
         outfilename=infilename
  elif afiletype == "MK21_EDF" :
        outfilename = ParseNafcHdr.EDF_to_NAFC(infilename,HdrDicts)
        if outfilename==".":
            print ("Outfile abort =",outfilename)
#            wx.Exit()
            exit()       
  else:
        print (infilename," is not an NAFC_Y2K MK21_EDF format file..aborting")
#        wx.Exit()
        exit()


#create an sub-class of AquireGUI4 of the Edit Header Dialog to run the show
  frame = EditHdr(None,outfilename,hdr1dict,hdr8dict)
#show the frame
  frame.Show(True)
#start the applications
  app.MainLoop()

#after edit is done  
  if DataChanged:
        f=open(outfilename,"r+")
        oK= ParseNafcHdr.Write_NAFC_File_Hdr(f,cards["h0"],HdrDicts)
        f.close()
###################### Program entry point ###############################
if __name__ == '__main__':
    main()

