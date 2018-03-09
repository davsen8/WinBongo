import serial, time
from serial.tools import list_ports


################################### DOSERIAL CLASS #####################################################

class DoSerial():

    def __init__(self):

        # initialization and open the port
        # possible timeout values:
        #    1. None: wait forever, block call
        #    2. 0: non-blocking mode, return immediately
        #    3. x, x is bigger than 0, float allowed, timeout block call

        self.ser = serial.Serial()
        self.ser.port = "com1"

        # ser.port = "/dev/ttyS2"

        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits

        # ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read

        self.ser.timeout = 5  # timeout block read
        self.ser.xonxoff = True  # disable software flow control
        self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2  # timeout for write

        try:
            self.ser.open()
        except Exception, e:
            print
            "error open serial port: " + str(e)
            exit()
        print
        "port on in DoSerial"

    #################
    def wake_ctd(self):

        if self.ser.isOpen():
            try:
                print
                "port open"
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
                MAX_TRYS = 5
                while (response != "S>\r\n") and (trys <= MAX_TRYS):
                    #              self.ser.flushInput() #flush input buffer, discarding all its contents
                    self.ser.write("\r")
                    time.sleep(0.1)
                    while (self.ser.inWaiting() < 4) and (sleeps < MAX_TRYS):
                        time.sleep(0.5)
                        sleeps += 1
                        print
                        "sleeps=" + str(sleeps)
                    if (sleeps < MAX_TRYS):
                        response = self.ser.readline()
                    sleeps = 0
                    print
                    "trys=" + str(trys) + '\n ' + response
                    trys += 1;

                self.ser.flushInput()  # flush input buffer, discarding all its contents

                if (trys > MAX_TRYS):
                    status = "FAIL: CAN NOT AWAKEN AFTER " + str(trys) + " TRYS : CHECK PORT,CABLES & SWITCHES"
                else:
                    status = "PASS: CTD AWAKE"

                print("awake " + status + response + " " + str(trys))

            except Exception, e1:
                print
                "error communicating...: " + str(e1)
                status = "FAIL: Error COMMUNICATING ON WAKEUP: CHECK SERIAL PORT#/ADAPTER " + self.ser.port

        else:
            print
            "cannot open serial port " + self.ser.port
            status = "FAIL: PORT NOT OPEN: CHECK SERIAL PORT#/ADAPTER" + self.ser.port
        return status

    ##################################
    def run_command(self, command):
        if self.ser.isOpen():
            try:
                print
                "port open"
                self.ser.flushInput()  # flush input buffer, discarding all its contents
                self.ser.flushOutput()  # flush output buffer, aborting current output

                command_size = len(command)
                print("sending command " + command + " " + str(command_size))
                self.ser.write(command)
                while (self.ser.inWaiting() < command_size):
                    time.sleep(0.1)

                response = self.ser.read(command_size)
                print("read data: " + response)

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


            except Exception, e1:
                print
                "error communicating...: " + str(e1)

        else:
            print
            "cannot open serial port "

        # having both CR and LF causes double spacing when displayed in window so string CR's out
        status = status.replace('\r', ' ', 20)
        #        status=status.replace('\n',' ',20)
        #        for c in status:
        #       	print (c+" ",ord(c))
        return status