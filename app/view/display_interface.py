# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (qApp, QListWidgetItem, QFrame, QTreeWidgetItem, QHBoxLayout,QVBoxLayout,
                             QTreeWidgetItemIterator, QTableWidgetItem,QAbstractItemView)
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView
# from .main_window import MainWindow
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from pyqtgraph import PlotWidget


class DisplayInterface(GalleryInterface):
    """ Display interface """

    def __init__(self, inst, parent=None):
        self.inst = inst
        super().__init__(
            title='扫描绘图',
            subtitle="实时绘制扫描结果",
            parent=parent
        )
        self.setObjectName('displayInterface')

        temperatureDisplay = self.addExampleCard(
            title=self.tr('温度曲线'),
            widget=DisplayFrame(parent=self, 
                                title='温度曲线', 
                                subtitle='通道列表:101,102,103 ...\nPt100', 
                                ylabel='温度', yunits='℃', 
                                xlabel='时间', xunits='s'),
        )
        temperatureDisplay.widget.plotGraphic(x=0, y=0, pen='r', name='Red curve')
        flowDisplay = self.addExampleCard(
            title=self.tr('流量曲线'),
            widget=DisplayFrame(parent=self, 
                                title='流量曲线', 
                                subtitle='通道: 121', 
                                ylabel='流量', yunits='m3/s', 
                                xlabel='时间', xunits='s'),
        )
        pressureDisplay = self.addExampleCard(
            title=self.tr('压力变送器'),
            widget=DisplayFrame(parent=self, 
                                title='压力曲线', 
                                subtitle='通道: 122', 
                                ylabel='压力', yunits='kPa', 
                                xlabel='时间', xunits='s'),
        )
        transmitterDisplay = self.addExampleCard(
            title=self.tr('温度变送器'),
            widget=DisplayFrame(parent=self, 
                                title='温度曲线', 
                                subtitle='通道: 221', 
                                ylabel='温度', yunits='℃', 
                                xlabel='时间', xunits='s'),
        )


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.SCAN_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class DisplayFrame(Frame):

    def __init__(self, parent, title, subtitle,ylabel,yunits,xlabel,xunits):
        super().__init__(parent)
        self.__initPlot(title, subtitle,ylabel,yunits,xlabel,xunits)
    
    def __initPlot(self,title, subtitle,ylabel,yunits,xlabel,xunits):
        self.tempPlot = PlotWidget()
        self.tempPlot.setTitle(title=title, subtitle=subtitle)
        self.tempPlot.setLabel('left', ylabel, units=yunits)
        self.tempPlot.setLabel('bottom', xlabel, units=xunits)
        self.tempPlot.showGrid(x=True, y=True)
        self.tempPlot.addLegend()
        self.tempPlot.setWindowTitle('pyqtgraph example: PlotWidget')

        self.tempPlot.setBackground('white')
        self.tempPlot.setFixedHeight(250)
        self.addWidget(self.tempPlot)

    def plotGraphic(self, x, y, pen, name):
        # self.tempPlot.plot([1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8],
        #                     pen='r', name='Red curve')
        # self.tempPlot.plot([1, 2, 3, 4, 5, 6, 7, 8], [1, 4, 9, 16, 25, 36, 49, 64],
        #                     pen='b', name='Blue curve')
        # self.tempPlot.plot([1, 2, 3, 4, 5, 6, 7, 8], [1, 8, 27, 64, 125, 216, 343, 512],
        #                     pen='g', name='Green curve')
        x = [0.0, 3.0, 5.0, 8.0, 11.0, 13.0, 16.0, 19.0]
        y = [29.911, 29.949, 29.939, 29.866, 29.816, 29.753, 34.734, 35.156]
        self.tempPlot.plot(x, y, pen=pen, name=name)
