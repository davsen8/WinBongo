####### ParseNAFCHdr.py ##########################################
# performs to functions   reads XBT (EDF)file and converts to nafc format file
# read nafc format file header for editing
#  unpdates:
# April 11-2015 : DRS adjusted file chooser write wild card issue under portable python
# April 17-2015 : DRS adjusted edf reader to ignore number of : in header lines
#   TO SUPPORT MK21 V7.0.0.12 EDF format


import os,sys
#import ntpath
#import csv
#import array
import wx

#####################################################################

def Read_EDF_File_Hdr(f,hdr):

        i=-1
        condition = True
        while condition:
            i+=1
            hdr.append(f.readline().strip().split(':'))
            if(hdr[i][0]=="// Data") :
                condition = False
#       end of loop
        return(True)

def Parse_EDF_Nafc_File_Hdr(hdr,HdrDict):
    hdr0 = HdrDict["hdr0"]
    hdr1 = HdrDict["hdr1"]
    hdr4 = HdrDict["hdr4"]
    hdr8 = HdrDict["hdr8"]

# due to : in file path
#    RawDataFile=hdr[2][0]+':'+hdr[2][1]+':'+hdr[2][2]
#  v7.0.0.12 doesn't hava a full path
    RawDataFile=hdr[2][-1]
    
    hdr0["RAWDATAFILE"]=RawDataFile
    hdr0["INFILE"]=""
   
    aprobe = hdr[6][1].split('-')
    probe ="XBT" + aprobe[1].zfill(2)
    Date = hdr[15][1].lstrip().split('/')

    SerialNumber = hdr[20][1].lstrip()
    if len(SerialNumber)<8 :
            SerialNumber ="00000000"
    outfile = SerialNumber+".d"+Date[2][2:4]
    hdr0["OUTFILE"]=outfile

    Lat = hdr[18][1].lstrip().split(' ')
    Lon = hdr[19][1].lstrip().split(' ')
    hdr1["LATD"]=Lat[0]
    LonD=(Lon[0][0:2])
    hdr1["LOND"]=LonD
# if the minutes are les than 10 everything is 1 space to the left,
# this is not elegant but works as a fix for now
#    print Lat[1], Lat[1][1:2],Lon[1] ,Lon[1][1:2]
    if Lat[1][1:2]=='.':
        hdr1["LATM"]=Lat[1][0:4]
    else:
        hdr1["LATM"]=Lat[1][0:5]
    if Lon[1][1:2]=='.':
        hdr1["LONM"]=Lon[1][0:4]
    else:
        hdr1["LONM"]=Lon[1][0:5]


# the current setup on some pcs has double : in the user defined fields.. this may be an issue.
# also if the user fields are missing things may go pair shaped
# So in case the user insert is missing,,, assume if DEPTH is missing they are all missing
# and check for the single blank between the 2 :
    if hdr[21][0][0:5] != "DEPTH":
        hdr1["DEPTH"]=""
        hdr1["FISHSET"]=""
        hdr1["COMMENT"]=""
    else:
#        if hdr[21][1]==" " :
#            x=2
#        else:
#            x=1
#        hdr1["DEPTH"]=hdr[21][x].lstrip()
#        hdr1["FISHSET"]=hdr[22][x].lstrip()
#        hdr1["COMMENT"]=hdr[23][x][0:16].lstrip()
# just take the right most list element -1 is that element
        hdr1["DEPTH"]=hdr[21][-1].lstrip()
        hdr1["FISHSET"]=hdr[22][-1].lstrip()
        hdr1["COMMENT"]=hdr[23][-1][0:16].lstrip()



    hdr1["SHIP"]=SerialNumber[0:2]
    hdr1["TRIP"]=SerialNumber[2:5]
    hdr1["STN"]=SerialNumber[5:8]


    hdr1["YEAR"]=Date[2]
    hdr1["MONTH"]=Date[0]
    hdr1["DAY"]=Date[1]
    hdr1["HOUR"]=hdr[16][1].lstrip()
    hdr1["MINUTE"]=hdr[16][2]

    hdr1["PROBE"]=probe
    hdr1["FORMAT"]="F"
    hdr1["CARD"]='1'
    hdr1["TERMINOUS"]=""

#    print hdr1["SHIP"]
#    print hdr1["TRIP"]
#    print hdr1["STN"]
#    print hdr1["LATD"]
#    print hdr1["LATM"]
#    print hdr1["LOND"]
#    print hdr1["LONM"]
#    print hdr1["YEAR"]
#    print hdr1["MONTH"]
#    print hdr1["DAY"]
#    print hdr1["HOUR"]
#    print hdr1["MINUTE"]
#    print hdr1["DEPTH"]
#    print hdr1["PROBE"]
#    print hdr1["FISHSET"] 
#    print hdr1["FORMAT"]
#    print hdr1["COMMENT"]
#    print hdr1["CARD"]
#    print hdr1["TERMINOUS"]
    

    hdr4["SHIP"]=hdr1["SHIP"]
    hdr4["TRIP"]=hdr1["TRIP"]
    hdr4["STN"]=hdr1["STN"]
    hdr4["RECORDS"]="000000"
    hdr4["HERTZ"]="00.00"
    hdr4["DTYPE"]="A"
    hdr4["CHANCNT"]="03"
    hdr4["CHANNELS"]="#DT-----------------"
    hdr4["FREE"]="          "
    hdr4["MODE"]="D"
    hdr4["SUBSAMPLE"]=""
    hdr4["MIND"]=""
    hdr4["MAXD"]=""
    hdr4["STRATA"]=""
    hdr4["CARD"]="4"
    hdr4["TERMINOUS"]=""
    
    hdr8["SHIP"]=hdr1["SHIP"]
    hdr8["TRIP"]=hdr1["TRIP"]
    hdr8["STN"]=hdr1["STN"]
    hdr8["CLOUD"]=""
    hdr8["WINDDIR"]=""
    hdr8["WINDSPD"]=""
    hdr8["WWCODE"]=""
    hdr8["AIRPRES"]=""
    hdr8["DRYTEMP"]=""
    hdr8["WETTEMP"]=""
    hdr8["WAVEP"]="" 
    hdr8["WAVEH"]=""
    hdr8["SWELLD"]=""
    hdr8["SWELLP"]=""
    hdr8["SWELLH"]=""
    hdr8["ICECONC"]=""
    hdr8["ICESTAGE"]=""
    hdr8["NBERGS"]=" "
    hdr8["SandT"]=" " 
    hdr8["FREE"]="                "
    hdr8["CARD"]="8"
    hdr8["TERMINOUS"]=""

def Write_EDF_Nafc_File_Hdr(fout,hdr,HdrDict):
    Write_NAFC_File_Hdr(fout,"NAFC_Y2K_HEADER\n",HdrDict)
    fout.write(HdrDict["hdr0"]["RAWDATAFILE"])
    fout.write("\nSCAN   DEPTH  TEMP\n")
    fout.write ("-- DATA --\n")


def Copy_EDF_File_Data(f,fout):
        i=1
        for aline in  f :
                line =aline.strip().split('\t')
                record = str(i)+' '+line[2]+' '+line[3]+'\n'
                fout.write(record)
                i+=1
# end of loop
        return(True)

# stores elements of nafc-bpo card 1,4,8 header strings into dictionary elements (dict of strings)
def Parse_NAFC_Hdr1(cards,hdr1):
                hdr1["SHIP"]=cards["h1"][0:2]
                hdr1["TRIP"]=cards["h1"][2:5]
                hdr1["STN"]=cards["h1"][5:8]
                hdr1["LATD"]=cards["h1"][9:12]
                hdr1["LATM"]=cards["h1"][13:18]
                hdr1["LOND"]=cards["h1"][20:23]
                hdr1["LONM"]=cards["h1"][24:29]
                hdr1["YEAR"]=cards["h1"][30:34]
                hdr1["MONTH"]=cards["h1"][35:37]
                hdr1["DAY"]=cards["h1"][38:40]
                hdr1["HOUR"]=cards["h1"][41:43]
                hdr1["MINUTE"]=cards["h1"][44:46]
                hdr1["DEPTH"]=cards["h1"][47:51]
                hdr1["PROBE"]=cards["h1"][52:57]
                hdr1["FISHSET"]=cards["h1"][58:61] 
                hdr1["FORMAT"]=cards["h1"][62:63]
                hdr1["COMMENT"]=cards["h1"][64:78]
                hdr1["CARD"]=cards["h1"][79:80]
                hdr1["TERMINOUS"]=cards["h1"][81:]

def Parse_NAFC_Hdr4(cards,hdr4):
                hdr4["SHIP"]=cards["h4"][0:2]
                hdr4["TRIP"]=cards["h4"][2:5]
                hdr4["STN"]=cards["h4"][5:8]
                hdr4["RECORDS"]=cards["h4"][9:15]
                hdr4["HERTZ"]=cards["h4"][16:21]
                hdr4["DTYPE"]=cards["h4"][22:23]
                hdr4["CHANCNT"]=cards["h4"][24:26]
                hdr4["CHANNELS"]=cards["h4"][27:47]
                hdr4["FREE"]=cards["h4"][48:58]  
                hdr4["MODE"]=cards["h4"][59:60]
                hdr4["SUBSAMPLE"]=cards["h4"][61:64]
                hdr4["MIND"]=cards["h4"][65:69]
                hdr4["MAXD"]=cards["h4"][70:74]
                hdr4["STRATA"]=cards["h4"][75:78]
                hdr4["CARD"]=cards["h4"][79:80]
                hdr4["TERMINOUS"]=cards["h4"][81:]
                
def Parse_NAFC_Hdr8(cards,hdr8): 
                hdr8["SHIP"]=cards["h8"][0:2]
                hdr8["TRIP"]=cards["h8"][2:5]
                hdr8["STN"]=cards["h8"][5:8]
                hdr8["CLOUD"]=cards["h8"][9:10]
                hdr8["WINDDIR"]=cards["h8"][11:13]
                hdr8["WINDSPD"]=cards["h8"][14:16]
                hdr8["WWCODE"]=cards["h8"][17:19]
                hdr8["AIRPRES"]=cards["h8"][20:26]
                hdr8["DRYTEMP"]=cards["h8"][27:32]
                hdr8["WETTEMP"]=cards["h8"][33:38]
                hdr8["WAVEP"]=cards["h8"][39:41] 
                hdr8["WAVEH"]=cards["h8"][42:44]
                hdr8["SWELLD"]=cards["h8"][45:47]
                hdr8["SWELLP"]=cards["h8"][48:50]
                hdr8["SWELLH"]=cards["h8"][51:53]
                hdr8["ICECONC"]=cards["h8"][54:55]
                hdr8["ICESTAGE"]=cards["h8"][56:57]
                hdr8["NBERGS"]=cards["h8"][58:59]
                hdr8["SandT"]=cards["h8"][60:61] 
                hdr8["FREE"]=cards["h8"][62:78]
                hdr8["CARD"]=cards["h8"][79:80]
                hdr8["TERMINOUS"]=cards["h8"][81:]
                                
def ReadnParse_MK21_EDF_Hdr(f,HdrDicts) :
                return True

#                        ' '+'{:>3}'.format(hdr1["LATD"].strip().zfill(2))+ ' '+ hdr1["LATM"].strip().zfill(5)+\
# builds card header string from dictionary elements
def Hdr1_Dict_to_String(hdr1):
    flatm = "     "
    flonm = "     "
    try:
      if hdr1["LATM"] != "" :
            flatm = "%0.2f" % (float (hdr1["LATM"]))
      if hdr1["LONM"] != "" :
            flonm = "%0.2f" % (float (hdr1["LONM"]))
    except:
            pass

    hdr1_out= hdr1["SHIP"].strip().zfill(2)+ hdr1["TRIP"].strip().zfill(3)+ hdr1["STN"].strip().zfill(3)+\
                        ' '+'{:>3}'.format(hdr1["LATD"].strip().zfill(2))+ ' '+ flatm.zfill(5) +\
                        ' -'+ hdr1["LOND"].strip().zfill(3)+' '+ flonm.zfill(5)+\
                        ' '+ hdr1["YEAR"].strip().zfill(4)+'-'+ hdr1["MONTH"].strip().zfill(2)+\
                        '-'+hdr1["DAY"].strip().zfill(2)+' '+ hdr1["HOUR"].strip().zfill(2)+':'+ hdr1["MINUTE"].strip().zfill(2)+\
                        ' '+ hdr1["DEPTH"].strip().zfill(4)+' '+ hdr1["PROBE"]+\
                        ' '+hdr1["FISHSET"].strip().zfill(3)+' '+ hdr1["FORMAT"].strip().zfill(1)+' '+ hdr1["COMMENT"][0:14].ljust(14)+\
                        ' '+ hdr1["CARD"].strip().zfill(1)+hdr1["TERMINOUS"]

    return (hdr1_out)
    
def Hdr4_Dict_to_String(hdr4):
    hdr4_out= hdr1["SHIP"].strip().zfill(2)+ hdr1["TRIP"].strip().zfill(3)+ hdr1["STN"].strip().zfill(3)+' '+ hdr4["RECORDS"].strip().zfill(6)+\
                        ' '+ hdr4["HERTZ"].strip().zfill(5)+' '+ hdr4["DTYPE"]+' '+ hdr4["CHANCNT"].strip().zfill(2)+' '+ hdr4["CHANNELS"].ljust(2)+\
                        ' '+ hdr4["FREE"]+' '+hdr4["MODE"].strip().zfill(1)+' '+ hdr4["SUBSAMPLE"].strip().zfill(3)+' '+ hdr4["MIND"].strip().zfill(4)+\
                        ' '+ hdr4["MAXD"].strip().zfill(4)+' '+ hdr4["STRATA"].strip().zfill(3)+' '+ hdr4["CARD"].strip().zfill(1)+hdr4["TERMINOUS"]
    return (hdr4_out)
    
def Hdr8_Dict_to_String(hdr8):
    fairp = "      "
    fairTW = "     "
    fairTD = "     "
    try:
        if hdr8["AIRPRES"] != "" :
            fairp = "%0.1f" % (float (hdr8["AIRPRES"]))
        if hdr8["WETTEMP"] != "" :
            fairTW = "%0.1f" % (float (hdr8["WETTEMP"]))
        if hdr8["DRYTEMP"] != "" :    
            fairTD = "%0.1f" % (float (hdr8["DRYTEMP"]))
    except:
            pass

    hdr8_out= hdr1["SHIP"].strip().zfill(2)+ hdr1["TRIP"].strip().zfill(3)+ hdr1["STN"].strip().zfill(3)+' '+ '{:<1}'.format(hdr8["CLOUD"])+\
                        ' '+ '{:>2}'.format(hdr8["WINDDIR"])+' '+ '{:>2}'.format(hdr8["WINDSPD"])+' '+ '{:>2}'.format(hdr8["WWCODE"])+\
                        ' '+ fairp.zfill(6)+' '+ fairTD.zfill(5)+ ' '+fairTW.zfill(5) +\
                        ' '+ '{:>2}'.format(hdr8["WAVEP"])+' '+ '{:>2}'.format(hdr8["WAVEH"])+' '+ '{:>2}'.format(hdr8["SWELLD"])+\
                        ' '+ '{:>2}'.format(hdr8["SWELLP"])+' '+'{:>2}'.format(hdr8["SWELLH"])+' '+ '{:<1}'.format(hdr8["ICECONC"])+\
                        ' '+ '{:<1}'.format(hdr8["ICESTAGE"])+' '+ '{:<1}'.format(hdr8["NBERGS"])+' '+ '{:<1}'.format(hdr8["SandT"])+\
                        ' '+ hdr8["FREE"]+' '+hdr8["CARD"]
#    +hdr8["TERMINOUS"]
    return (hdr8_out)


# fudge: -strings are in a dictionary element because strings are value based and imutable whne passed to functions,
# so need a mutable wrapper (sucha sa a dict or list) to carry the changed values back to the calling level
def Read_NAFC_File_Hdr(f,cards):
        cards["h0"]=f.readline()
        cards["h1"]=f.readline()
        cards["h4"]=f.readline()
        cards["h8"]=f.readline()
        return(True)
        
        Read_MK21_EDF_Hdr(f,hdr1dict)
        return(True)

# write header card strings to target file
def Write_NAFC_File_Hdr(f,z,HdrDicts):
        hdr1_out=Hdr1_Dict_to_String(HdrDicts["hdr1"])
        hdr4_out=Hdr4_Dict_to_String(HdrDicts["hdr4"])
        hdr8_out=Hdr8_Dict_to_String(HdrDicts["hdr8"])

        f.write("NAFC_Y2K_HEADER\n")
        f.write(hdr1_out)
        f.write('\n')
        f.write(hdr4_out)

        f.write('\n')
        f.write(hdr8_out)
        f.write('\n')
        return True
def save_file_dialog(filename):

        """Save contents of output window."""
#        filename = "frog.txt"
        outfilename = None
        dlg = wx.FileDialog(None, "Save File As...", "", filename, "NAFC D-File|*.d*|All Files|*",  wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() ==  wx.ID_OK:
            outfilename = dlg.GetPath()
        dlg.Destroy()
        

        return(outfilename)

def EDF_to_NAFC(filename,HdrDict):
    hdr =list()
    oK=False
    temp=dict()
    Updateshiptripstn =False
    afiletype= FileTypeIs(filename)

    if afiletype =="MK21_EDF" :
     f=open(filename,"r")
     Read_EDF_File_Hdr(f,hdr)

     Parse_EDF_Nafc_File_Hdr(hdr,HdrDict)
     fileout = HdrDict["hdr0"]["OUTFILE"]
     if fileout[0:8]=="00000000":
        Updateshiptripstn =True

     msg="ENTER OUTPUT FILE TO CREATE"

     condition = True
     while condition:
             FileOK = True

             fileout = save_file_dialog(fileout)
             if fileout!=None :
               try:
                  fout=open(fileout,"w")         
               except IOError:
                print "bad filename or path.. by"
                msg="Bad name or path "+fileout+" edit or Cancel"
                FileOK=False

             if(fileout ==None) or FileOK :
                condition = False
#       end of loop
     if fileout ==None:
        wx.Exit()
        exit()

# when the input XBT file had no serial number
     if Updateshiptripstn ==True:
        hdr1=HdrDict["hdr1"]
        hdr4=HdrDict["hdr4"]
        hdr8=HdrDict["hdr8"]
        hdr1["SHIP"]=os.path.basename(fileout)[0:2]
        hdr1["TRIP"]=os.path.basename(fileout)[2:5]
        hdr1["STN"]=os.path.basename(fileout)[5:8]
        hdr4["SHIP"]=hdr1["SHIP"]
        hdr4["TRIP"]=hdr1["TRIP"]
        hdr4["STN"]=hdr1["STN"]
        hdr8["SHIP"]=hdr1["SHIP"]
        hdr8["TRIP"]=hdr1["TRIP"]
        hdr8["STN"]=hdr1["STN"]
                      
     Write_EDF_Nafc_File_Hdr(fout,hdr,HdrDict)
     Copy_EDF_File_Data(f,fout)
     f.close()
     fout.close()

     return(fileout)
     

def FileTypeIs(filename):

    f=open(filename,"r")
    firstline = f.readline().strip()
#    print firstline
    f.close()
#    if firstline == "// MK21 EXPORT DATA FILE  (EDF)":
    if firstline[0:7] == "// MK21":
        return ("MK21_EDF")
    if firstline[0:4] == "NAFC":
        return ("NAFC_Y2K_HEADER");
    else:
        return ("UNKNOWN");    

######################################
#  This code needs to go into the main of the program startup module
#######################################
def main():

# to hold the file header card strings , there are read from or written tot the file
    cards=dict(h0="",h1="",h4="",h8="")
                
# to hold the parsed header card elements, this are assigned to from the form
    hdr0dict=dict()
    hdr1dict=dict()
    hdr4dict=dict()
    hdr8dict=dict()
    HdrDicts=dict(hdr0=hdr0dict,hdr1=hdr1dict,hdr4=hdr4dict,hdr8=hdr8dict)

    filename = os.path.normpath("C:\sources\Win7Aquire\TestData\T5_00037.EDF".replace(r"\\",r"/"))
#    filename = os.path.normpath("TestData\\20114037.d14".replace(r"\\",r"/"))
    if filename == "" :
     if len(sys.argv)>1 :
        filename=sys.arg[1]
     else:
       exit()
#    print "reading ",filename
#   for afile in hdr_list:
#       cat_file = os.path.splitext(afile)[0]+".SBE"


    oK=False

    afiletype = FileTypeIs(filename)
 
    if afiletype =="NAFC_Y2K_HEADER" :
         f=open(filename,"r+")
         if Read_NAFC_File_Hdr(f,cards):
            Parse_NAFC_Hdr1(cards,HdrDicts["hdr1"])
            Parse_NAFC_Hdr4(cards,HdrDicts["hdr4"])
            Parse_NAFC_Hdr8(cards,HdrDicts["hdr8"])
            f.seek(0)
            oK= Write_NAFC_File_Hdr(f,cards["h0"],HdrDicts)
         f.close()
    elif afiletype == "MK21_EDF" :
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
        app = wx.App(False)

        EDF_to_NAFC(filename,HdrDicts)

    else:
#        print filename," is not an NAFC_Y2K_HEADER format file..aborting"

        exit()



###################### SAMPLE HEADER #################################################
# h0="NAFC_Y2K_HEADER"
# h1="20114037  46 28.84 -043 36.57 2014-11-20 20:05 3048 XBT05 003 F fc35-sgb19-022 1"
# h4="20586148 000665  8.00 A 10 #PTCSMO%FL----------            D 000 0000 0170 000 4"
# h8="20586148 7 20 04 02 1016.5 -01.0 -01.5 00 00 18 04 01 1 2 3 4                  8"
######################################################################################

if __name__ == '__main__':
        main()
        
#################################################################################
#  the essential workaround to the problem of Python not having pass-by-reference
#def Change(self, var):
#    var[0] = 'Changed'

#variable = ['Original']
#self.Change(variable)      
#print variable[0]
#################################################################################
