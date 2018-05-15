# WinBongo2
WinBongo2.py
D.Senciall  May 2018 ;
Gov. of Canada , Dept. Fisheries and Oceans,
Science Branch NL region

python 3.65  wxpython 4.0.1 pheonix compatible

bongo net mounted CTD real-time flight tracker

Program intented for use with Seabird Inc. SBE-19+ ctd mounted on a Bongo Frame or other structure that is towed from side of ship.
Assumes CTD is connected via conducting cable to allow for realtme data transmission.
Program allows for read time data collection and view of package flight path.
An adjustable decent and asscent reference line provides a refeence to allow descent/accent to follow a prescibed angle/rate (user must of
course tell winch operator to adjust cable speed accordingly.)

Assumptions:
  tested under MS-Windows 7 and 10 ; not tested or configured for linux (serial port ids would need adjustment)
  assumes SBE-19+ ctd with ROM version 1.1a or similar command set 
  assumes CTD sampling rate is 1 scan/second (this can be adjusted if needed but currently hardcoded in current version)
  
 Note:
  Ctd is configured apon connection (tow start) and deconfigured on exit; unplanned disocnnection of ctd from computer may leave
  ctd in undetermined state, requiring reconnection with software and a clean exit to reset; specific ctd recovery command in plan for
  come updates.
  
Credits:
  Elements of progenitor screen layout BASED ON CODE SAMPLE FROM:
  matplotlib-with-wxpython-guis by E.Bendersky
  Eli Bendersky (eliben@gmail.com)
  License: this code is in the public domain
  Last modified: 31.07.2008
  see   http://eli.thegreenplace.net/2008/08/01/matplotlib-with-wxpython-guis/

Also
 Code Borrowed from seawater-3.3.2-py.27.egg for the density calcuations

Requirement:
Python 3.65 ; Matplotlib ; datetime ; Queue ; numpy ; pyserial ; wxpython (4..)

History:
WinBongo (V1)  used older model Applied-MicroSystems STD-12 CTD, (depreciated) , python 2.7 , wxpython 3
