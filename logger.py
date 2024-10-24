import os
#from main import DATAPATH
class Logger:
    DATAFILEPATH = "data/debug.logger"
    def __init__(self) -> None:
        self.log = True
        try:
            if (not os.path.isfile(Logger.DATAFILEPATH)):
                open(Logger.DATAFILEPATH, "x")
        
            savefile = open(Logger.DATAFILEPATH, "w")
            savefile.write(f"")
            savefile.close()
        except:
            self.log = False
    


    def Log(self, data):
        if not self.log: return
        savefile = open(Logger.DATAFILEPATH, "a")
        savefile.write(f"{data}\n")
        savefile.close()

logger = Logger()