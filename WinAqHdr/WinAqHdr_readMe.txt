Nov 17 2015: DRS
This is the master stand-alone WinAquire Header form supporting MK21 EDF file import and conversion as well as NAFC D,P) file import-export. *EDF requires SEQUENCE # to hold ShipTripStn
Files are:
WinAqHdr_Main.py      : Main entry point program
WinAqHdr_GUI.py	      : Header data editing form
WinAqHdr_Validator.py : Contains validator code for the form
WinAqHdr_Parse_Nafc_EDF_Hdr.py :Routines to read (EDF or NAFC), parse and write (NAFC)format

WinAqHdr.bat	: batch file to launch application; if associating in win-XP associate with this file to launch from data file double click (edf)
WinAqHdr.cmd	: basically the same as .bat, but doesn't work for launch in XP

Note for bat and cmnd adjust python path the actual suit python install (*install requires wxpython)

May 15 2018 : DRS
Updated to run under python 3.65-32  and wxpython Pheonix 4.0.1