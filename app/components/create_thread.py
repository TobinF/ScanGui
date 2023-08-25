# -*- coding: utf-8 -*-
import time
# from typing import Any
from PyQt5.QtCore import QThread, pyqtSignal


class CreateThread(QThread):

    finishSignel = pyqtSignal(str)
    scanSignal = pyqtSignal(dict)
    # scanTime = pyqtSignal(time.struct_time)

    def __init__(self, *args, **kwargs):
        self.target = None
        self.timeInterval = None
        self.display = None
        # self.isRunning = False
        super(CreateThread, self).__init__()
        

    def run(self):
        while True:
            if self.target:
                data = self.target()
                self.scanSignal.emit(data)
                # self.scanTime.emit(time.localtime())
                if self.display:
                    self.display()                
                if self.timeInterval:
                    time.sleep(self.timeInterval)

            else:
                break

    def stop(self):
        try:
            self.terminate()
            return 'stop'
        except Exception as e:
            return str(e)


