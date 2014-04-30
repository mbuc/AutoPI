import AutoPi
import Media_Buttons_rc
from PyQt4 import QtCore, QtGui

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = AutoPi.Ui_AutoPi()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
