from loguru import logger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLCDNumber, QFrame, QHBoxLayout, QTableWidgetItem, QAbstractItemView, QApplication
from qfluentwidgets import PushButton, TableWidget, BodyLabel

from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from ..components.info_bar import CreateInfoBar
from ..components.create_thread import CreateThread
from ..components.agilent34970a import Agilent34970A

# 新开一个线程进行数据扫描
import time

class ScanInterface(GalleryInterface):
    """ Scan interface scanThread,"""

    def __init__(self,inst, parent=None):
        self.inst:Agilent34970A = inst
        self.mainWindow = parent
        self.beginScanTime = 0
        super().__init__(
            title='扫描页面',
            subtitle="查看扫描结果和保存扫描数据",
            parent=parent
        )
        self.resultData = parent.scanResult   
        self.setObjectName('scanInterface')
        self.__initButtonBoxLayout()

        # table view
        self.slot1 = self.addExampleCard(
            title=self.tr('插槽1'),
            widget=TableFrame(self,
                              ['101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122'],
                              ['测量类型','单位', '当前值', '最大值', '最小值'],
                              0),
        )
        self.slot2 = self.addExampleCard(
            title=self.tr('插槽2'),
            widget=TableFrame(self,
                              ['201','202','203','204','205','206','207','208','209','210','211','212','213','214','215','216','217','218','219','220','221','222'],
                              ['测量类型','单位', '当前值', '最大值', '最小值'],
                              0),
        )
        self.slot3 = self.addExampleCard(
            title=self.tr('插槽3'),
            widget=TableFrame(self,
                              ['301','302','303','304','305','306','307','308','309','310','311','312','313','314','315','316','317','318','319','320','321','322'],
                              ['测量类型','单位', '当前值', '最大值', '最小值'],
                              0),
        )

    def __initButtonBoxLayout(self):
        buttonBoxLayout = QHBoxLayout()
        # leftBottonLayout = QHBoxLayout()
        # rightBottonLayout = QHBoxLayout()
        # 添加控件
        saveDateButton = PushButton()
        saveDateButton.setText('导出数据')
        saveDateButton.clicked.connect(self.testStartButtonOnClicked)
        saveDateButton.setFixedSize(120, 32)        
        startScanButton = PushButton()
        startScanButton.setText('开始扫描')
        startScanButton.clicked.connect(self.startScanButtonOnClicked)
        startScanButton.setFixedSize(120, 32)
        stopScanButton = PushButton()
        stopScanButton.setText('结束扫描')
        stopScanButton.clicked.connect(self.stopScanButtonOnClicked)
        stopScanButton.setFixedSize(120, 32)
        # 设置LCD显示时间
        timeLcdLabel = BodyLabel()
        timeLcdLabel.setText('扫描时间')
        self.timeLcd = QLCDNumber()
        self.timeLcd.setDigitCount(8)
        self.timeLcd.setSegmentStyle(QLCDNumber.Flat)
        self.timeLcd.setFixedSize(120, 32)
        scanTime = time.strftime("%H:%M:%S", (1,0,0,0,0,0,0,0,0))
        self.timeLcd.display(scanTime)

        # 添加控件到布局
        buttonBoxLayout.addWidget(startScanButton)
        buttonBoxLayout.addWidget(stopScanButton)
        buttonBoxLayout.addWidget(saveDateButton)
        buttonBoxLayout.addWidget(timeLcdLabel)
        buttonBoxLayout.addWidget(self.timeLcd)
        # 布局设置
        buttonBoxLayout.setSpacing(20)
        buttonBoxLayout.setAlignment(Qt.AlignCenter)
        # 添加布局到主布局
        self.vBoxLayout.addLayout(buttonBoxLayout)

    def __initTableLayout(self):
        slotList = [1,2,3] 
        ...

    @property
    def createTableThread(self)->CreateThread:
        tableThread = CreateThread()   
        tableThread.display = True
        tableThread.flushpDisplay.connect(self.syncTableData)
        tableThread.timeInterval = 1
        return tableThread
    @property
    def createSyncTimeThread(self)->CreateThread:
        syncTimeThread = CreateThread()
        syncTimeThread.display = True
        syncTimeThread.flushpDisplay.connect(self.syncTime)
        syncTimeThread.timeInterval = 1
        return syncTimeThread


    def startScanButtonOnClicked(self):
        '''
        创建新线程，启动扫描
        '''
        self.mainWindow.startScan()
        ...
    def stopScanButtonOnClicked(self):
        '''
        关闭线程
        '''
        self.mainWindow.stopScan()
        ...
    def testStartButtonOnClicked(self):
        self.exportData()

    def syncTableData(self, isFlush:bool):
        if not isFlush:
            return
        resultData = self.mainWindow.scanResultData
        for k, v in resultData.items():
            channel = k
            data = v['data'][-1]
            physicalType = v['type']
            unit = v['unit']
            maxValue = v['maxValue']
            minValue = v['minValue']
            slot = int(str(k)[0])
            getattr(self, f'slot{slot}').widget.syncData(channel, data, physicalType, unit, maxValue, minValue)        # ...

    def syncTime(self):
        # 更新LCD显示时间
        if self.beginScanTime:
            # 计算时间差
            sec = time.time() - self.beginScanTime
            # 输出时间差，格式为：时:分:秒
            scanTime = time.strftime("%H:%M:%S", time.gmtime(sec))
            self.timeLcd.display(scanTime)

    def exportData(self):
        resultData = self.mainWindow.scanResultData
        fileNmae = f'扫描数据-{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.json'
        with open(fileNmae, 'w', encoding='utf-8') as f:
            import json
            jsonData = json.dumps(resultData)
            f.write(jsonData)
        CreateInfoBar.createInfoBar(self.mainWindow, '提示', f'数据已导出到{fileNmae}')
        ...

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.SCAN_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)

class TableFrame(Frame):

    def __init__(self, parent, horizontalHeaderLabels, verticalHeaderLabels, channelInfos):
        super().__init__(parent)
        self.table = TableWidget(self)
        self.addWidget(self.table)
        self.table.setWordWrap(False)
        self.table.setRowCount(5)
        self.table.setColumnCount(22)
        self.table.setSelectRightClickedRow(True)
        self.table.setHorizontalHeaderLabels(horizontalHeaderLabels)
        self.table.setVerticalHeaderLabels(verticalHeaderLabels)
        # 设置最小行宽
        self.table.horizontalHeader().setMinimumSectionSize(90)

        self.setFixedHeight(250)
        self.table.resizeColumnsToContents()
        # # 禁止编辑
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def syncData(self, channel, data, physicalType, unit, maxValue, minValue):
        row = int(str(channel)[1:]) - 1
        self.table.setItem(0, row, QTableWidgetItem(str(physicalType)))     # 测量类型
        self.table.setItem(1, row, QTableWidgetItem(str(unit)))             # 单位
        self.table.setItem(2, row, QTableWidgetItem(str(data)))             # 当前值
        self.table.setItem(3, row, QTableWidgetItem(str(maxValue)))         # 最大值
        self.table.setItem(4, row, QTableWidgetItem(str(minValue)))         # 最小值
        ...

    # def keyPressEvent(self, event):
    #     """ Ctrl + C复制表格内容 """
    #     if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
    #         # 获取表格的选中行
    #         selected_ranges = self.table.selectedRanges()[0]  # 只取第一个数据块,其他的如果需要要做遍历,简单功能就不写得那么复杂了
    #         text_str = ""  # 最后总的内容
    #         # 行（选中的行信息读取）
    #         for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
    #             row_str = ""
    #             # 列（选中的列信息读取）
    #             for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
    #                 item = self.table.item(row, col)
    #                 row_str += item.text() + '\t'  # 制表符间隔数据
    #             text_str += row_str + '\n' # 换行
    #         clipboard = qApp.clipboard()  # 获取剪贴板
    #         clipboard.setText(text_str)  # 内容写入剪贴板