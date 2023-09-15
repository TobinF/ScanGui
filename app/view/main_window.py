# coding: utf-8
import time

from PyQt5.QtCore import QSize, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication
from loguru import logger
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow, NavigationItemPosition, SplashScreen,NavigationAvatarWidget

from app.components.info_bar import CreateInfoBar

from ..common import resource
from ..common.config import  cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..components.agilent34970a import Agilent34970A
from ..components.create_thread import CreateThread

from .cmd_interface import CommandInterface
from .display_interface import DisplayInterface
from .gallery_interface import GalleryInterface
from .inst_config_interface import ConfInterface
from .scan_interface import ScanInterface
from .setting_interface import SettingInterface


class MainWindow(FluentWindow, Agilent34970A):

    def __init__(self):
        self.inst = Agilent34970A()
        # self.scanResult = {}
        self.scanResultData = {}
        super().__init__()
        self.initWindow()
        # create sub interface
        self.scanInterface = ScanInterface(self.inst,  self)
        self.confInterface = ConfInterface(self.inst, self)
        self.displayInterface = DisplayInterface(self.inst, self)
        self.cmdInterface = CommandInterface(self.inst, self)

        self.settingInterface = SettingInterface(self)

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
        # t = Translator()
        self.addSubInterface(self.confInterface, FIF.DEVELOPER_TOOLS, '配置仪器')
        # 添加分割线
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.scanInterface, FIF.SYNC, '扫描', pos)
        self.addSubInterface(self.displayInterface, FIF.SPEED_MEDIUM, '曲线', pos)
        self.addSubInterface(self.cmdInterface, FIF.COMMAND_PROMPT, '调试工具', pos)

        # 添加分割线
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)        
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)


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
        self.scanResultData = self.inst.channelListDict
        # self.displayInterface.initDisplay()
        # 扫描线程
        self.scanThread = CreateThread()
        self.scanThread.target = self.inst.parseResult
        self.scanThread.timeInterval = self.inst.scanInterval
        self.scanThread.scanSignal.connect(self.scanResult)
        # 更新表格线程
        self.tableThread = self.scanInterface.createTableThread
        # 时钟线程
        self.scanInterface.beginScanTime = time.time()
        self.syncTimeThread = self.scanInterface.createSyncTimeThread
        # 绘图线程
        self.displayInterface.initDisplay()   # 初始化绘图
        self.displayThread = self.displayInterface.createPlotThread
        # self.displayInterface
        # 启动线程
        CreateInfoBar.createInfoBar(self, '提示', '开始扫描')
        # self.inst.getBeginStartScanTime
        if self.scanThread:
            self.scanThread.start()
        if self.tableThread:
            self.tableThread.start()
        if self.syncTimeThread:
            self.syncTimeThread.start()
        if self.displayThread:
            self.displayThread.start()

    def stopScan(self, *args, **kwargs):
        '''
        结束扫描，关闭线程
        '''
        try:
            self.inst.breakScan
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self, '错误', str(e))
            return
        finally:
            if self.scanThread.isRunning:
                self.scanThread.stop()
            if self.tableThread.isRunning:
                self.tableThread.stop()
            if self.syncTimeThread.isRunning:
                self.syncTimeThread.stop()
            if self.displayThread.isRunning:
                self.displayThread.stop()
    
        ...
    def scanResult(self,resultData):
        # logger.info(f'字典: {self.scanResultData}')
        # j = 0
        # for i in range(len(self.inst.channelList)):
        #     logger.info(f'扫描结果: {resultData[j:j+7]}')
        #     self.scanResultData[self.scanResultData[i]]['data'].extend(resultData[j:j+7])
        #     self.scanResultData[self.scanResultData[i]]['time'].extend(resultData[j:j+7])
        #     self.scanResultData[self.scanResultData[i]]['maxValue'] = max(self.scanResultData[self.scanResultData[i]]['data'])
        #     self.scanResultData[self.scanResultData[i]]['minValue'] = min(self.scanResultData[self.scanResultData[i]]['data'])
        #     j+=7
        # logger.info(f'格式化数据: {self.scanResultData}')
        self.scanResultData = resultData
        # logger.info(f'扫描结果: {self.scanResultData}')
        ...
    def scanPlot(self):
        plotThread = CreateThread()
        plotThread.target = self.displayInterface.displayPlot(self.scanResult)
        plotThread.timeInterval = self.inst.scanInterval
        
        return plotThread
    
    def test(self):
        self.displayInterface.displayPlot(self.scanResult)
        ...

    def emptyScan(self, *args, **kwargs):
        '''
        清空当前数据
        '''
        self.scanResultData = {}
        # self.scanInterface.emptyTable()
        self.displayInterface.initDisplay()
        ...



        