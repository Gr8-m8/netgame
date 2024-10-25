import select
import sys
class Getch:
    def readkey(self):
        return b''
    
getch = Getch()

try:
    import msvcrt
    class GetchWindows(Getch):
        def readkey(self):
            if msvcrt.kbhit(): 
                return msvcrt.getch()
            return b''
    
    getch = GetchWindows()
except: pass
try:
    import termios
    import tty

    oset = termios.tcgetattr(sys.stdin)

    class GetchUnix(Getch):
        def iskey():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        
        def readkey(self):
            tty.setcbreak(sys.stdin.fileno())
            if self.iskey():
                return sys.stdin.read(1).encode()
            return b''

    getch = GetchUnix()
except: pass

try:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oset)
except: pass