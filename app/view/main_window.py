# coding: utf-8
import threading as td
import time
from unittest import result
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from more_itertools import peekable

from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from app.components.info_bar import CreateInfoBar

from .gallery_interface import GalleryInterface
from .scan_interface import ScanInterface
from .inst_config_interface import ConfInterface
from .display_interface import DisplayInterface
from ..common.config import SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common import resource
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..components.agilent34970a import Agilent34970A
from ..components.create_thread import CreateThread


class MainWindow(FluentWindow, Agilent34970A):

    def __init__(self):
        self.inst = Agilent34970A()
        self.scanResult = {}
        super().__init__()
        self.initWindow()
        # create sub interface
        self.scanInterface = ScanInterface(self.inst,  self)
        self.confInterface = ConfInterface(self.inst, self)
        self.displayInterface = DisplayInterface(self.inst, self)
        # self.scanThread = CreateThread()
        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        # signalBus.showMessageBox.connect(self.onShowMessageBox)
        # signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.confInterface, FIF.DEVELOPER_TOOLS, '配置仪器')
        # 添加分割线
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.scanInterface, FIF.SYNC, '扫描', pos)
        self.addSubInterface(self.displayInterface, FIF.SPEED_MEDIUM, '曲线', pos)


    def initWindow(self):
        self.resize(1200, 800)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon('app/resource/images/Inst.svg'))
        self.setWindowTitle('Agilent34970A 数据采集系统')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()


    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)


    def startScan(self, *args, **kwargs):
        '''
        创建新线程，启动扫描
        '''
        # 扫描线程
        scanThread:CreateThread = kwargs.get('scanThread')
        # self.scanThread = CreateThread()
        # self.scanThread.scanSignal.connect(slot)
        # self.scanThread.target = self.inst.test     # TODO:修改为scanAll函数
        # self.scanThread.timeInterval = self.inst.scanInterval
        # self.scanThread.timeInterval = 1
        # 时钟线程
        syncTimeThread:CreateThread = kwargs.get('syncTimeThread')
        # self.beginScanTime = time.time()
        # self.syncTimeThread = CreateThread()
        # self.syncTimeThread.target = self.syncTime
        # self.syncTimeThread.timeInterval = 1

        # 启动线程
        CreateInfoBar.createInfoBar(self, '提示', '开始扫描')
        self.inst.getBeginStartScanTime
        scanThread.start()
        syncTimeThread.start()
        # beginScanTime = time.localtime()
        # self.syncTime(beginScanTime)
        # self.scanThread.start()
        # self.syncTimeThread.start()

        ...
    def scanResultData(self,resultData):
        self.scanResult = resultData
        # return self.r
        ...




        