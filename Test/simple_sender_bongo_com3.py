# from : http://eli.thegreenplace.net/2009/07/30/setting-up-python-to-work-with-the-serial-port/
# simple sender use with http://com0com.sourceforge.net/
# http://www.magsys.co.uk/comcap/onlinehelp/null_modem_emulator_com0com.htm

#############################################################################
# NOTE  IF YOU HAVE ISSUES NOT GETTING DATA LOWER THE SIZE OF THE FIFO BUFFERS 
# IN THE WINDOWS HARDWARE SETUP FOR THE SERIAL PORTS UNDER ADVANCED SETTINGS
#############################################################################

import serial
import time
import msvcrt # built-in module

class DataGen2(object):
    def __init__(self, FileName,init=50):
        self.data = self.init = init

        self.FileName = FileName
        self.f = open(self.FileName,"r")

    def next(self):
        line=self.f.readline()
        return line

    def close_infile(self):
        print "closing file"
        self.f.close()

def on_send_timer(datagen,ser) :
    line = datagen.next()
    if line !=[] :
        x = ser.write(line)
        return line
    else:
        return ([])


def kbfunc():

    return msvcrt.getch() if msvcrt.kbhit() else '0'

def main() :
    FileName = "V035_517.DAT"
#    FileName = "BONGO_OUTPUT_LONG.TXT"
# virtual port for testing - requires com0com application pairs with "\\\\.\\CNCA0"
#    port = "\\\\.\\CNCB0"
    port = "com3"
    Nseconds = 1.0
    
    datagen = DataGen2(FileName)

    try: 
        ser = serial.Serial(port, 1200)
    except serial.serialutil.SerialException,e:
          print "error opening serial port: "+port+" " + str(e)
          return(False)
    print "port open in SerialSource"



    akey =""
    x = "x"
    while x !="" :
#        time.sleep(Nseconds)
        x = on_send_timer(datagen,ser)
        print x
        
    datagen.close_infile()

    ser.close()
    print 'bye - port closed'

if __name__ == '__main__':
        main()
