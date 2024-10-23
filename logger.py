import os
#from main import DATAPATH
DATAPATH = "data/"
class Logger:
    DATAFILE = "debug.logger"
    def __init__(self) -> None:
        if (not os.path.isfile(f"{DATAPATH}{Logger.DATAFILE}")):
            open(Logger.DATAFILE, "x")


    def Log(self, data):
        savefile = open(f"{DATAPATH}{Logger.DATAFILE}", "a")
        savefile.write(data)
        savefile.close()

logger = Logger()