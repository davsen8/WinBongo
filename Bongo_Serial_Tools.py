

import time
import serial
import datetime
import numpy as np

import threading
import Queue

#DEFAULT_COM = "COM1"
#DEFAULT_BAUD = 1200
DEFAULT_RATE = 1   # scans per second

SIMULATOR = False

###########################################################################
# READS DATA FROM A FILE :PASS 1 LINE at a atime back via the next method

class DataGen2(object):
    def __init__(self, FileName ,init=50):
        self.data = self.init = init
        self.Convert =ConvertClass()
        #        self.temp = 0.0
        self.FileName = FileName
        self.f = open(self.FileName ,"r")
        self.scannum =0
        self.scan = dict()

        self.readheader()

    def next(self):
        text =self.f.readline()

        if text =="" :
            self.scan["OK"] = False
            return(self.scan)
        else :
            self.scannum+=1
            line = text.split()
            scan = self.Convert.convert_simulation_b95(line)
            #            scan = self.Convert.convert_archived(line)
            scan["Et" ] =str(self.scannum * DEFAULT_RATE)

            return (scan)

    def readheader(self):

        text =self.f.readline()
        text =self.f.readline()
        text =self.f.readline()
        text =self.f.readline()
        text =self.f.readline()
        text =self.f.readline()


    def flush(self):  # dummy
        return()

    def close_infile(self):
        self.f.close()

########################################################################################
#  SERIAL PORT STD READER CLASS
# non threaded version  reads data from port when asked via next method
# initialization
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
# ser.timeout = None          #blocking read when using radline
# ser.timeout = 0             #non-block read
########################################################################################
class SerialSource_STD12():

    def __init__(self ,parent ,serial):
        self.parent = parent                # needed to call the flash status bar method of Graphframe
        self.ser = serial
        self.StartTime = 0
        self.set_default()
        self.Convert =ConvertClass()
        self.scan = dict()

    def set_default (self):
#        self.ser.port = DEFAULT_COM
#        self.ser.baudrate = DEFAULT_BAUD
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
            #          print "error open serial port: "+self.ser.port+" " + str(e)
            return(False)
        self.parent.flash_status_message("PORT OPEN  " +self.ser.getPort())

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
                scan["Et" ]= str(time.time() - self.StartTime)
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

    def send_Set_DataRate(self ,rate):
        self.parent.flash_status_message("SETTING STD DATA RATE =  "+ rate +" SCANS PER SECOND")
        self.ser.write("SET S  " +rate +"\r")
        self.ser.readline()

    def close_Port(self):
        self.parent.flash_status_message("PORT CLOSSING")
        self.ser.close()

    def is_port_open(self):
        return (self.ser.isOpen())


# *** END OF SerialSource_STD12 Class ******************
# *******************************************  SBE19PLUS *********************************************
class SerialSource_SBE19p(threading.Thread):

    def __init__(self, serial, queue):

        self.queue = queue
        self.ser = serial
        self.StartTime = 0

        self.Convert = ConvertClass()
        self.scan = dict()

        self.pause = True    # wait waste gates the data
        self.StreamOn = False   # stops the run from getting any data; needed to com with instrument
        self.shutdown = False
        self.set_default()
        self.open_Port()

        threading.Thread.__init__(self)

    def set_default(self):
#        self.ser.port = DEFAULT_COM
#        self.ser.baudrate = DEFAULT_BAUD
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
            print ("error open serial port:  " +self.ser.port +" " + str(e))
            return (False)
        #        self.parent.flash_status_message("PORT OPEN " + self.ser.getPort())

        return (True)

    def flush(self):
        self.ser.flushInput()
        line = self.ser.readline()  # ensure a full line is in buffer by discarding any stub

    def unpause_data_feed(self):
        self.pause = False

    def pause_data_feed(self):
        self.pause = True

    def next(self):
        line = self.ser.readline()
        return (line)

    def run(self):
        if (self.ser.isOpen() == False):
            self.open_Port()
            self.ser.flushInput()

        retrys = 0
        while not self.shutdown:

            if self.StreamOn:   # data stream is available get a record
                line = self.next()

                if line != '' and not self.pause:  # if we are in a pause just waste the record, but keep reading
                    print(line)
                    line = line.split(',')
                    scan = self.Convert.convert_SBE19p_raw(line)
                    print (scan)
                    if "OK" in scan:
                        self.queue.put(scan)
                    retrys = 0
                else:
                    retrys = retrys + 1
            #                time.sleep (0.05)

                if retrys > 100:
                    line = "FINISHED"  # need a better code, but this is what archived file uses for now
                    self.queue.put(line)
                    retrys = 0  # we don't want to hang or stop trying, we want the main program to tell us what to do

        self.queue.put("FINISHED")
        if self.is_port_open():
            self.send_Stop_Data()
            self.close_Port()
        return



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
                MAX_TRYS = 20
                while (response.find("S>")==-1) and (trys <= MAX_TRYS):
                    #              self.ser.flushInput() #flush input buffer, discarding all its contents
                    self.ser.write("\r\r\r")
                    time.sleep(0.1)
                    while (self.ser.inWaiting() >= 2) and (sleeps < MAX_TRYS):
                        time.sleep(0.05)
                        sleeps += 1
                        print("sleeps=" + str(sleeps))
#                    if (sleeps < MAX_TRYS):
                        ammount = self.ser.inWaiting()
                        response = response + self.ser.read(ammount)
                        print ("trys=" + str(ammount) + str(trys)+ ' ' + response)
                    sleeps = 0

                    trys += 1

                time.sleep(0.05)
                self.ser.flushInput()  # flush input buffer, discarding all its contents clear any Seacat

                if (trys > MAX_TRYS):
                    status = "FAIL: CAN NOT AWAKEN AFTER " + str(trys) + " TRYS : CHECK PORT,CABLES & SWITCHES"
                else:
                    status = "PASS: CTD AWAKE"

                print("awake " + status + response + " " + str(trys))

            except Exception as e1:
                print ("error communicating...: " + str(e1))
                status = "FAIL: Error COMMUNICATING ON WAKEUP: CHECK SERIAL PORT#/ADAPTER " + self.ser.port

        else:
            print ("cannot open serial port " + self.ser.port)
            status = "FAIL: PORT NOT OPEN: CHECK SERIAL PORT#/ADAPTER" + self.ser.port
        return status


    def Get_CTD_Status(self):
#        self.parent.flash_status_message("GETTING CTD STATUS ... sending DS")
        status = ""
        self.Send_Wake()
        if (self.Send_Command('DS')) :
            status = self.Get_Responce()

        return (status)

    # Sends the provided command and eats the echo back ; return true if seems to be ok
    def Send_Command(self,command):
        responce = ''
        try:
            print("port open")
            self.ser.flushInput()  # flush input buffer, discarding all its contents
            self.ser.flushOutput()  # flush output buffer, aborting current output

            # ensure command has a carriage return , add if needed
            if (command.find('\r'))== -1:
                command = command +'\r'

            command_size = len(command)
            print("sending command " + command + " " + str(command_size))
            self.ser.write(command)
            while (self.ser.inWaiting() < command_size):
                time.sleep(0.01)

            response = self.ser.read(command_size)

                # SBE19p returns ?cmd S>   if command is not recognized
            if (responce.find('?c')) != -1:
                self.ser.flushInput()
                return False


            print("read data: " + response)
        except Exception as e1:
            print("error communicating...: " + str(e1))
            return False

        return True


     # use after Send_Command if command returns a response, return that responce
    def Get_Responce(self):
        status = ''
        if self.ser.isOpen():
            try:
                numOfLines = 0
                status = ''
                response = ''
                while response != 'S>':
                    response = self.ser.readline()
                    if response != "":
                        status += response
                        numOfLines = numOfLines + 1
                    if (numOfLines >= 200):
                        break
                # having both CR and LF causes double spacing when displayed in window so string CR's out
                status = status.replace('\r', ' ', 20)
            except Exception as e1:
                print ("error communicating...: " + str(e1))

        else:
            print ("cannot open serial port ")
            status = 'ERROR'

        return status

    def send_Real(self):
#        self.parent.flash_status_message("SETTING CTD TO REAL TIME MODE")
#        self.parent.flash_status_message("SENDING IGNORESWITCH")
        self.ser.write("IGNORESWITCH=Y\r")
        print (self.ser.readline())  # echo plus Cr-Lf which requires the 2nd read
        #        self.ser.readline()
#        self.parent.flash_status_message("SENDING OUTPUTFORMAT=3")
        self.ser.write("OUTPUTFORMAT=3\r")
        print (self.ser.readline())  # echo plus Cr-Lf which requires the 2nd read
        #        self.ser.readline()
#        self.parent.flash_status_message("SENDING OUTPUTSAL")
        self.ser.write("OUTPUTSAL=Y\r")
        print (self.ser.readline())  # echo plus Cr-Lf which requires the 2nd read
        #        self.ser.readline()
        #        self.ser.write("OUTPUTUCSD=Y\r")
        #        self.ser.readline()  # echo plus Cr-Lf which requires the 2nd read
        #        self.ser.readline()

#        time.sleep(1.0)

    def send_StartNow_Data(self):
        self.Send_Wake()
        self.ser.write("STARTNOW\r")
#        print (self.ser.readline())
#        time.sleep(0.1)
        self.ser.flushInput()
#        self.ser.readline()
        self.StreamOn = True
#        self.parent.flash_status_message("CTD DATA STARTED")

    def send_Stop_Data(self):
#        self.parent.flash_status_message("STOPPING CTD DATA")
        self.StreamOn = False
        self.ser.write("STOP\r")
        print ("SENDING STOP")
#        time.sleep(0.01)
#        print (self.ser.readline())
        self.flush()


    def send_QS(self):  # put ctd to sleep
        self.ser.write("QS\r")

    def send_Clear_Data(self):
#        self.parent.flash_status_message("CLEARING CTD MEMORY")
        self.ser.write("INITLOGGING\r")
        print (self.ser.readline())
        time.sleep(0.1)
        self.ser.flushInput()


    def send_Set_DataRate(self, rate):
        avg = str(rate *4)
#        self.parent.flash_status_message("SETTING CTD DATA RATE = " + rate + " SCANS PER SECOND")
        self.ser.write("NAVG=" + '4' + "\r")
        self.ser.readline()

    def close_Port(self):
#        self.parent.flash_status_message("RESETTING CTD TO SELF CONTAINED")
        self.ser.write("IGNORESWITCH=N\r")
        self.ser.readline()  # echo plus Cr-Lf which requires the 2nd read
#        self.ser.readline()
        self.ser.write("OUTPUTFORMAT=0\r")
        self.ser.readline()  # echo plus Cr-Lf which requires the 2nd read
#        self.ser.readline()

#        self.parent.flash_status_message("PORT CLOSSING")
        self.ser.close()

    def is_port_open(self):
        return (self.ser.isOpen())

    def getPort(self):
        return ('-1')

    def shut_down(self):
        self.pause_data_feed()

        self.send_Stop_Data()
        self.send_QS()
        self.ser.flushInput()
#        time.sleep(0.05)   # avoid pulling the rug out to quick
        self.close_Port()
        self.shutdown = True


# *** END OF SerialSource_SBE19p Class ******************
## smoothed rate over Avg_interval scans

class SmoothRate(object):
    def __init__(self ,interval):
        self.Avg_interval = interval
        self.rolling_list =  l = [0.0] * self.Avg_interval
        self.n = 0
        self.OldPres = 0.0
        self.PSum =0.0

    def get_rate(self, pres):
        self.n = (self.n + 1) % self.Avg_interval
        deltaP = pres - self.OldPres
        self.PSum = self.PSum + deltaP - self.rolling_list[self.n]
        the_rate = (60. * self.PSum / self.Avg_interval)
        #           print self.n,pres,self.OldPres,deltaP, self.PSum,self.Avg_interval, Rstr
        self.rolling_list[self.n] = deltaP
        self.OldPres = pres
        return (the_rate)
# *** END of SmoothRate Class ******************************


class ConvertClass():

    def __init__(self):
        self.a = (999.842594, 6.793952e-2, -9.095290e-3, 1.001685e-4, -1.120083e-6, 6.536332e-9)
        self.b = (8.24493e-1, -4.0899e-3, 7.6438e-5, -8.2467e-7, 5.3875e-9)
        self.c = (-5.72466e-3, 1.0227e-4, -1.6546e-6)
        self.d = 4.8314e-4

        self.bastime = 0

    def convert_STD12_raw(self, line):
        scan = dict()
        scan["ctdclock"] = line[0]
        xdatetime = datetime.datetime.strptime(scan["ctdclock"], '%H:%M:%S')
        #       if basetime == 0 :
        #                 basetime = xdatetime

        scan["pres"] = -1. * (float(line[1]) / 10.0)
        scan["Pstr"] = str('{:.5}'.format(int(line[1]) / 10.0))
        scan["Tstr"] = str('{:.5}'.format(int(line[2]) / 1000.0))
        scan["Cstr"] = str('{:.5}'.format(int(line[3]) / 1000.0 / 42.921))
        # for flow if < 56.5  value should be 0.. need to add
        scan["F1str"] = str('{:.5}'.format(int(line[4]) / 100.0))
        scan["F2str"] = str('{:.5}'.format(int(line[5]) / 100.0))
        scan["Lstr"] = str('{:.5}'.format(int(line[6]) / 100.0))
        scan["Vstr"] = str('{:.5}'.format(int(line[7]) / 100.0))
        scan["Sstr"] = str('{:.5}'.format(int(line[8]) / 1000.0))
        scan["Dstr"] = str('{:5}'.format(self.dens0((int(line[8]) / 1000.0), (int(line[2]) / 1000.0) - 1000.0)))
        scan["OK"] = True
        scan["Et"] = 0.0
        return (scan)

    def convert_SBE19p_raw(self, line):
        scan = dict()
        #            scan["ctdclock"] = line[0]
        #            xdatetime = datetime.datetime.strptime(scan["ctdclock"], '%H:%M:%S')
        #       if basetime == 0 :
        #                 basetime = xdatetime
        try:
            scan["pres"] = -1. * (float(line[2]))
            scan["Pstr"] = str('{:7.4}'.format(float(line[2])))
            scan["Tstr"] = str('{:7.4}'.format(float(line[0])))
            scan["Cstr"] = str('{:7.4}'.format(float(line[1])))
        # for flow if < 56.5  value should be 0.. need to add
            scan["F1str"] = ""
            scan["F2str"] = ""
            scan["Lstr"] = ""
        #            scan["Vstr"] = str('{:7.5}'.format(float(line[5])))
        #
            scan["Sstr"] = str('{:7.4}'.format(float(line[3])))
        #            scan["Dstr"] = str('{:7.5}'.format(float (line[4])))
            scan["Vstr"] = ""

            scan["Dstr"]  = str('{:.4}'.format(self.dens0(np.float(line[3]), np.float(line[0])) - 1000.0))

            scan["OK"] = True
            scan["Et"] = 0.0
        except: pass

        return (scan)

    def convert_archived(self, line):
        scan = dict()

        #        xdatetime = datetime.datetime.strptime(ctdclock,'%H:%M:%S')
        #        if basetime = 0 :
        #                 basetime = xdatetime
        #        scan["ctdclock"] = line[0]
        scan["scannum"] = line[0]
        scan["ctdclock"] = line[1]
        scan["Et"] = line[2]
        scan["pres"] = -1. * float(line[3])
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

    def convert_simulation_b95(self, line):
        scan = dict()

        #        xdatetime = datetime.datetime.strptime(ctdclock,'%H:%M:%S')
        #        if basetime = 0 :
        #                 basetime = xdatetime
        #        scan["ctdclock"] = line[0]
        scan["ctdclock"] = "00:11:22"
        scan["pres"] = -1. * float(line[0])
        scan["Pstr"] = str('{:.4}'.format(line[0]))
        scan["Sstr"] = str('{:.4}'.format(line[2]))
        scan["Tstr"] = str('{:.4}'.format(line[3]))
        scan["Cstr"] = str('{:.4}'.format(line[1]))
        scan["F1str"] = str('{:.4}'.format(line[6]))
        scan["F2str"] = str('{:.4}'.format(line[7]))
        scan["Lstr"] = str('{:.4}'.format(line[5]))
        scan["Vstr"] = str('{:.4}'.format("12.5"))
        #        scan["Et"] = xdatetime - basetime
        scan["Et"] = "0"
        scan["Dstr"] = str('{:.4}'.format(self.dens0(np.float(line[2]), np.float(line[3])) - 1000.0))
        scan["OK"] = True
        return (scan)

    # Code Borrowed from seawater-3.3.2-py.27.egg
    def dens0(self, s, t):
        """
     Density of Sea Water at atmospheric pressure.

     Parameters
     ----------
     s(p=0) : array_like
              salinity [psu (PSS-78)]
     t(p=0) : array_like
              temperature [ (ITS-90)]

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
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        return (self.smow(t) + (b[0] + (b[1] + (b[2] + (b[3] + b[4] * T68) * T68) *
                                        T68) * T68) * s + (c[0] + (c[1] + c[2] * T68) * T68) * s *
                s ** 0.5 + d * s ** 2)

    def smow(self, t):
        """
    Density of Standard Mean Ocean Water (Pure Water) using EOS 1980.

    Parameters
    ----------
    t : array_like
        temperature [ (ITS-90)]

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
