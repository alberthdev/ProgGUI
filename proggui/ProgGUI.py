from PyQt4 import QtGui, QtCore
from proggui.progwin import ProgressWindow

import sys
import multiprocessing

# Python 3 uses queue, Python 2 uses Queue
try:
    import queue
except ImportError:
    import Queue as queue

import time

class ProgressProcess(multiprocessing.Process):
    def __init__(self, comm_queue, **kwargs):
        multiprocessing.Process.__init__(self)
        self.comm_queue = comm_queue
        self.kwargs = kwargs
        
        self.closed_cleanly = None
    
    def run(self):
        self.app = QtGui.QApplication(sys.argv)
        
        self.window = ProgressWindow(comm_queue = self.comm_queue, **self.kwargs)
        self.window.open()
        
        return(self.app.exec_())

class ProgressBar:
    def __init__(self, cancel_callback = None, **kwargs):
        self.kwargs = kwargs
        
        # If we are using Python >= 3.4, we can use this little trick
        # to make multiprocessing work with PyQt!
        if (sys.version_info >= (3, 4)):
            multiprocessing.set_start_method('spawn')
        
        self.process_queue = multiprocessing.Queue()
        self.process = ProgressProcess(self.process_queue, **kwargs)
        self.cancel_callback = cancel_callback
        
        self.closed_cleanly = None
        
    def show(self):
        multiprocessing.freeze_support()
        self.process.start()
    
    def close(self):
        self.closeWindow()
    
    # Internal/external function
    # Check if the process is still alive. If it is, return True.
    # Otherwise, return False.
    def checkProcessState(self):
        if not self.process.is_alive():
            if (self.closed_cleanly == None):
                # Search the queue for our exit message!
                while True:
                    try:
                        req = self.process_queue.get(timeout = 1)
                    except queue.Empty:
                        break
                    
                    if len(req) > 0:
                        if req[0] == "closed" and (len(req) == 2):
                            self.closed_cleanly = req[1]
                            
                if not self.closed_cleanly:
                    if self.cancel_callback:
                        self.cancel_callback()
            
            return False
        else:
            return True
    
    def isOpen(self):
        return self.checkProcessState()
    
    def isClosed(self):
        return not self.checkProcessState()
    
    # Internal function - raises if already exited
    def checkExited(self):
        if not self.checkProcessState():
            raise Exception("GUI already exited!")
    
    def setStatus(self, status):
        self.checkExited()
        self.process_queue.put(["setStatus", status])
    
    def setProgress(self, progress):
        self.checkExited()
        self.process_queue.put(["setProgress", progress])
    
    def setCancelLbl(self, cancel_label):
        self.checkExited()
        self.process_queue.put(["setCancelLbl", cancel_label])
    
    def setCancelEnabled(self, en):
        self.checkExited()
        self.process_queue.put(["setCancelEnabled", en])
    
    def enableCancel(self):
        self.checkExited()
        self.process_queue.put(["enableCancel"])
    
    def disableCancel(self):
        self.checkExited()
        self.process_queue.put(["disableCancel"])
    
    def setPulseEnabled(self, en):
        self.checkExited()
        self.process_queue.put(["setPulseEnabled", en])
    
    def enablePulse(self):
        self.checkExited()
        self.process_queue.put(["enablePulse"])
    
    def disablePulse(self):
        self.checkExited()
        self.process_queue.put(["disablePulse"])
    
    def closeWindow(self):
        self.checkExited()
        self.process_queue.put(["closeWindow"])
    
    def finish(self):
        self.closeWindow()
        self.process.join()
    
    def __del__(self):
        self.process.join()
