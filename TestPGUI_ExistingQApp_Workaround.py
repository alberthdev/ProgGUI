import sys
import time

from PyQt4 import QtGui, QtCore

from proggui import ProgressBar

global pb

# Python 2 compatibility fun (from Python 3)
if (sys.version_info < (3, 0)):
    range = xrange

class TestDlg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TestDlg, self).__init__(parent)
        self.helloWorldLbl = QtGui.QLabel("Hello, world!")
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.helloWorldLbl)
        self.setLayout(self.layout)
        
        self.setWindowTitle("Hello, world!")
        
        progressTest()
        
def stopCallback():
    print("Callback triggered - GUI closed!")

def progressTest():
    global pb
    #pb = ProgressBar(title="Testing...", status="Testing 1, 2, 3...", pulsing = True, cancel_callback = stopCallback)
    pb.show()

    time.sleep(1)
    pb.disablePulse()

    for i in range(1, 101):
        if pb.isClosed():
            break
        else:
            pb.setProgress(i)
            
            if i > 80:
                pb.setStatus("Almost done...")
            elif i > 60:
                pb.setStatus("Halfway there (and some)...")
                pb.enableCancel()
            elif i > 40:
                pb.setStatus("Working on it...")
                pb.disableCancel()
            elif i > 20:
                pb.setStatus("Running the gears...")
            
        time.sleep(0.1)

    if pb.isOpen():
        pb.close()

def main():
    global pb
    pb = ProgressBar(title="Testing...", status="Testing 1, 2, 3...", pulsing = True, cancel_callback = stopCallback)
    pb.show()
    pb.hide()
    
    time.sleep(3)
    # Create the application and the main window
    app = QtGui.QApplication(sys.argv)
    window = TestDlg()
    
    # Run
    window.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
