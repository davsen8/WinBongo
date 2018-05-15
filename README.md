# WinBongo2
WinBongo2.py
D.Senciall  May 2018 ;
Gov. of Canada , Dept. Fisheries and Oceans,
Science Branch NL region

python 3.65  wxpython 4.0.1 pheonix compatible

bongo net mounted CTD real-time flight tracker

Program intented for use with Seabird Inc. SBE-19+ ctd mounted on a Bongo Frame or other strcuture that is towed from side of ship.
Assumes CTD is connect via contducting cable to allow for realtme data transmission.
Program allows for read time data collection and view of package flight path.
An adjustable decent and asscent reference line provides a refeence to allow descent/accent to follow a prescibed angle/rate (user must of
course tell winch operator to adjust speed accordingly.)


credits:
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
