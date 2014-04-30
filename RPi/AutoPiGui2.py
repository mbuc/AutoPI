#!/usr/bin/env python

import time

from obd_capture import OBD_Capture
from PyQt4 import QtGui, QtCore
from AutoPi import Ui_AutoPi

class AutoPi(Ui_AutoPi):
    def __init__(self):
        Ui_AutoPi.__init__(self)
        #self.buttonCalc.clicked.connect(self.handleCalculate)
    #def handleCalculate(self):
    #    x = int(self.lineEditX.text())
    #    y = int(self.lineEditY.text())
    #    self.LineEditZ.setText(str(x + y))*/

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    AutoPi = QtGui.QMainWindow()
    ui = Ui_AutoPi()
    ui.setupUi(AutoPi)

    print "Displaying GUI"
#    AutoPi.showFullScreen()
    AutoPi.show()

    print "Attempting to start OBD_Capture()"
    obd = OBD_Capture()

    print "Done"

    if(obd is None):
        sys.exit(-1)
    print "Success!"
    obd.connect()
    time.sleep(3)
    if not obd.is_connected():
        print "Error: OBD Not Connected."
    else:
        print "Connected and ready."
        while 1:
#Get Coolant Temperature
            (name, value, unit) = obd.get_value(0x05)
#
#Get RPM
            (name, value, unit) = obd.get_value(0x0C)
            ui.lcdNumberRPM.value = value
#
#Get Intake Air Temperature
            (name, value, unit) = obd.get_value(0x0F)
            time.sleep(1)

    sys.exit(app.exec_())
