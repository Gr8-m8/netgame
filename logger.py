import os
#from main import DATAPATH
DATAPATH = "data/"
class Logger:
    DATAFILE = "debug.logger"
    def __init__(self) -> None:
        self.log = True
        try:
            if (not os.path.isfile(f"{DATAPATH}{Logger.DATAFILE}")):
                open(Logger.DATAFILE, "x")
        
            savefile = open(f"{DATAPATH}{Logger.DATAFILE}", "w")
            savefile.write(f"")
            savefile.close()
        except:
            self.log = False
    


    def Log(self, data):
        if not self.log: return
        savefile = open(f"{DATAPATH}{Logger.DATAFILE}", "a")
        savefile.write(f"{data}\n")
        savefile.close()

logger = Logger()