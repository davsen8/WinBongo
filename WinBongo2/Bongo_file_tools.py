

import threading
try:
    import queue
except:
    import Queue as queue


class read_from_file(threading.Thread):

    def __init__(self, afile, queue):

        self.queue = queue
        self.afile = afile

        self.StartTime = 0

        self.pause = True    # wait waste gates the data
        self.StreamOn = False   # stops the run from getting any data; needed to com with instrument
        self.shutdown = False
        self.set_default()
        self.open_File()

        threading.Thread.__init__(self)

    def set_default(self):
        pass


    def open_File(self):
        try:
            self.fp = open( self.afile,"r")
        except Exception as e:
            print ("error opening data file:  " +self.afile+" " + str(e))
            return (False)
        #        self.parent.flash_status_message("PORT OPEN " + self.ser.getPort())
        self.find_data_start()

        return (True)


    def find_data_start(self):
        line = self.fp.readline()
        while "-- DATA --" not in line:
            line = self.fp.readline()

    def flush(self):
        pass

    def unpause_data_feed(self):
        self.pause = False

    def pause_data_feed(self):
        self.pause = True

    def next(self):
        line = self.fp.readline()
        print (line)
        return (line)

    def run(self):

        scan = dict()
        retrys = 0
        while not self.shutdown:

            if self.StreamOn:   # data stream is available get a record
                line = self.next()

                if line != '' and not self.pause:  # if we are in a pause just waste the record, but keep reading
                    print(line)
                    line = line.split()
                    scan = self.convert_datafile(line)
#                    print (scan)
                    if scan["OK"]:
                        self.queue.put(scan)
                    retrys = 0
                else:
                    retrys = retrys + 1
            #                time.sleep (0.05)

                if retrys > 100:
                    scan["OK"] = False # need a better code, but this is what archived file uses for now
                    self.queue.put(scan)
                    self.shut_down()


        scan["OK"] = False # need a better code, but this is what archived file uses for now
        self.queue.put(scan)
        self.fp.close()
        return


    def send_StartNow_Data(self):
        self.StreamOn = True


    def send_Stop_Data(self):
        self.pause_data_feed()
        self.StreamOn = False   # should stop thread proccesing further data

    def shut_down(self):
        self.pause_data_feed()
        self.shutdown = True
        self.fp.close()



    def convert_datafile(self,line):
        scan = dict()

        try:
            scan["pres"] = float(line[3])
            scan["Pstr"] = (line[3])
            scan["Tstr"] = (line[4])
            scan["Cstr"] = (line[5])
            # for flow if < 56.5  value should be 0.. need to add
            scan["F1str"] = ""
            scan["F2str"] = ""
            scan["Lstr"] = ""
            #            scan["Vstr"] = str('{:7.5}'.format(float(line[5])))
            #
            scan["Sstr"] = (line[6])
            #            scan["Dstr"] = str('{:7.5}'.format(float (line[4])))
            scan["Vstr"] = ""

            scan["Dstr"] = (line[7])

            scan["OK"] = True
            scan["Et"] = float(line[2])

            for i in scan:
                print(i, scan[i])
        except:
            scan["OK"] = False

        return (scan)
