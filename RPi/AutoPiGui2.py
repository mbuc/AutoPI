#!/usr/bin/env python

import time
import pygame
#import RPi.GPIO as GPIO

from obd_capture import OBD_Capture
from PyQt4 import QtGui, QtCore
from AutoPi import Ui_AutoPi

#GPIO.setmode(GPIO.BOARD)
red = 12
green = 16
freq = 100 #Hz

playing = 0
paused  = 0

#GPIO.setup(red, GPIO.OUT)
#GPIO.setup(green, GPIO.OUT)


class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
 
    def run(self):
#        for i in range(6):
#            time.sleep(0.3) # artificial time delay
#            self.emit( QtCore.SIGNAL('update(QString)'), "from work thread " + str(i) )
        
#Get RPM
        while 1:
            (name, value, unit) = obd.get_value(0x0C)
            ui.lcdNumberRPM.display(value)
            vol = value/2000
            if vol > 1:
                vol = 1

            if playing:
                pygame.mixer.music.set_volume(vol)
                time.sleep(1)

            (name, value, unit) = obd.get_value(0x0D)
            ui.lcdNumberMPH.display(value)
#            vol = int(value/60)
#            pygame.mixer.music.set_volume(vol)
            time.sleep(0.5)
        return

class AutoPi(Ui_AutoPi):
    def __init__(self):
        Ui_AutoPi.__init__(self)
        #self.buttonCalc.clicked.connect(self.handleCalculate)
    #def handleCalculate(self):
    #    x = int(self.lineEditX.text())
    #    y = int(self.lineEditY.text())
    #    self.LineEditZ.setText(str(x + y))*/
        self.pushButton_Play.clicked.connect(self.handlePlay)
    def handlePlay(self):
        if playing:
            pygame.mixer.music.pause
            playing = 0
            paused = 1
        elif paused:
            pygame.mixer.music.unpause
            playing = 1
            paused = 0
        else:
            pygame.mixer.music.play()
            playing = 1
        return
    def handlePause(self):
        pygame.music.pause()
        return

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    AutoPi = QtGui.QMainWindow()
    ui = Ui_AutoPi()
    ui.setupUi(AutoPi)

    print "Displaying GUI"
#    AutoPi.showFullScreen()
    AutoPi.show()

#init pygame
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/mysong.mp3")

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
        while 0:
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

    print "starting worker thread"
    ui.lcdNumberRPM.display(10)
    workthread = WorkThread()
    workthread.start()
    print "done"
    sys.exit(app.exec_())
