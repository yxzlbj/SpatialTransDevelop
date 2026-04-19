import sys
from PyQt5 import QtWidgets, QtCore
import VTKWindow
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = VTKWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())