import time
import typing
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl, QSize, QThread, pyqtSignal
from test000_Ui import Ui_Dialog

class Test000(QWidget, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.isRuning = False

        self.st1.clicked.connect(self.on_button1_clicked)
        self.sp1.clicked.connect(self.on_button2_clicked)
        self.thread = testThread()

    def on_button1_clicked(self):
        self.thread.setTraget(self.test)
        self.thread.start()

    def on_button2_clicked(self):
        print(self.thread.isRunning())
        self.thread.stop()
        print("Button 2 clicked")
    ...
    def test(self):
            print("hello")
            time.sleep(1)
        

class testThread(QThread):
    def __init__(self, traget=None) -> None:
        super().__init__()
        self.traget = None
    

    def setTraget(self, traget):
        self.traget = traget

    def run(self):
        while True:
            print("hello there")
            self.traget()
            time.sleep(1)

    def stop(self):
        # print
        print("stop")
        self.terminate()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Test000()
    w.show()
    sys.exit(app.exec_())
