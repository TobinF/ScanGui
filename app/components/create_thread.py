# -*- coding: utf-8 -*-
import time
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

class CreateThread(QThread):
    '''
    创建新的线程
    '''

    finishSignel = pyqtSignal(str)
    # scanSignal = pyqtSignal(np.ndarray)
    scanSignal = pyqtSignal(dict)
    flushpDisplay = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        self.target = None
        self.timeInterval = None
        self.display = None
        super(CreateThread, self).__init__()
        

    def run(self):
        while True:
            if self.target:
                data = self.target()
                self.scanSignal.emit(data)
            if self.display:
                self.flushpDisplay.emit(True)               
            if self.timeInterval:
                time.sleep(self.timeInterval)

    def stop(self):
        try:
            self.terminate()
            return 'stop'
        except Exception as e:
            return str(e)


