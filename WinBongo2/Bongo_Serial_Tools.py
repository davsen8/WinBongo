
import time
import serial
import datetime
import numpy as np

import threading
try:
    import queue
except:
    import Queue as queue

#DEFAULT_COM = "COM1"
#DEFAULT_BAUD = 1200
DEFAULT_RATE = 1   # scans per second

SIMULATOR = False

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
        line = self.ser.readline().decode()
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
#                    print(line)
                    line = line.split(',')
                    scan = self.Convert.convert_SBE19p_raw(line)
#                    print (scan)
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

                CR = "\r"
                CR3 = "\r\r\r"
                self.ser.write(CR.encode('utf-8'))
#                print("write data: CR CR CR")
                response = ""
                status = ""
                trys = 0
                sleeps = 0
                MAX_TRYS = 20
                prompt = "S>"

                while (response.find(prompt)==-1) and (trys <= MAX_TRYS):
                    #              self.ser.flushInput() #flush input buffer, discarding all its contents
                    self.ser.write(CR3.encode())
                    time.sleep(0.1)
#                    print('in waiting= ',self.ser.inWaiting())
                    while (self.ser.inWaiting() >= 2) and (sleeps < MAX_TRYS):
                        time.sleep(0.05)
                        sleeps += 1
#                        print('in waiting2 = ',self.ser.inWaiting(),'response= ',response)

                        ammount = self.ser.inWaiting()
#                        print ("ammonut= ",ammount)
                        response =  self.ser.read(ammount).decode()
#                        print ('resp= ',response)
#                        print ("trys=" + str(ammount) + str(trys)+ ' ' + response)
                    sleeps = 0

                    trys += 1

                time.sleep(0.05)
                self.ser.flushInput()  # flush input buffer, discarding all its contents clear any Seacat
#                print ('trys= ',trys)
                if (trys > MAX_TRYS):
                    status = False
                else:
                    status = True

#                print("awake " + status + response + " " + str(trys))

            except Exception as e1:
                print ("wake-ctd error communicating...: " + str(e1))
                status = False

        else:
#            print ("cannot open serial port " + self.ser.port)
            status = False
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
                                    # when ctd fals asleep it write  'time out'  so need to
            self.ser.flushInput()  # flush input buffer, discarding all its contents
            self.ser.flushOutput()  # flush output buffer, aborting current output

            if self.Send_Wake():

            # ensure command has a carriage return , add if needed
                if (command.find('\r'))== -1:
                    command = command +'\r'

                command_size = len(command)
#            print("sending command " + command + " " + str(command_size))
                self.ser.write(command.encode())  # in python 3 chars are unicode, and need recoding for serial
                while (self.ser.inWaiting() < command_size):
                    time.sleep(0.005)

                response = self.ser.read(command_size).decode()

                # SBE19p returns ?cmd S>   if command is not recognized
                ERROR_CODE = '?c'
                if responce.find(ERROR_CODE) != -1:
                    self.ser.flushInput()
                    return False
            else:
                return False   # didnt wake


#            print("read data: " + response)
        except Exception as e1:
            print("send-command error communicating...: " + str(e1))
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
                    response = self.ser.readline().decode()
                    if response != "":
                        status += response
                        numOfLines = numOfLines + 1
                    if (numOfLines >= 200):
                        break
                # having both CR and LF causes double spacing when displayed in window so string CR's out
                status = status.replace('\r', ' ', 20)
            except Exception as e1:
                print ("get-response error communicating...: " + str(e1))
        else:
#            print ("cannot open serial port ")
            status = 'ERROR'

        return status

    def send_Real(self):  # place ctd inr ealtime mode under computer control, eng unit data with salinity
        self.Send_Command("IGNORESWITCH=Y\r")
        self.Send_Command("OUTPUTFORMAT=3\r")
        self.Send_Command("OUTPUTSAL=Y\r")


    def send_Reset_factory(self):  # return ctd to swithc control and hex data
        self.Send_Command("IGNORESWITCH=N\r")
        self.Send_Command("OUTPUTFORMAT=0\r")


    def send_StartNow_Data(self):
        self.Send_Command("STARTNOW\r")

        self.StreamOn = True


    def send_Stop_Data(self):
        self.pause_data_feed()
        self.StreamOn = False   # should stop thread proccesing further data
        command = "STOP\r"
        self.ser.write(command.encode())   # stop doesnt echo or require a wakeup so dont use Send_Command
        self.flush()  #clear the S> prompt and any data lines left in buffer

    def send_InitLogging(self):  # put ctd to sleep
        self.Send_Command('INITLOGGING')
        self.ser.flushInput()
        return (True)

    def send_QS(self):  # put ctd to sleep Qs doesnt echo so dont use Send_Command
        if self.Send_Wake():   # we dont know if it is awake or in QS so wake anyway and then put to QS
            command = "QS\r"
            self.ser.write(command.encode())


    def send_Set_DataRate(self, rate):
        avg = str(rate *4)
        self.Send_Command("NAVG=" + '4' + "\r") #  avg 4 scans to get 1 per sencond


    def close_Port(self):
#        self.parent.flash_status_message("RESETTING CTD TO SELF CONTAINED")
        self.send_Stop_Data()
        self.Send_Command("IGNORESWITCH=N")
        self.Send_Command("OUTPUTFORMAT=0")
        self.send_QS()

        self.ser.close()

    def is_port_open(self):
        return (self.ser.isOpen())

    def getPort(self):
        return ('-1')

    def shut_down(self):
        self.pause_data_feed()
        self.send_Stop_Data()
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
