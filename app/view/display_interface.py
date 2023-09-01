# coding:utf-8
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout,QVBoxLayout
from loguru import logger
import numpy as np

from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from ..components.create_thread import CreateThread
from ..components.agilent34970a import Agilent34970A
from pyqtgraph import PlotWidget

colorList = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
# colorList = (color for color in colorList)

class DisplayInterface(GalleryInterface):
    """ Display interface """

    def __init__(self, inst, parent=None):
        self.inst:Agilent34970A = inst
        self.mainWindow = parent
        super().__init__(
            title='扫描绘图',
            subtitle="实时绘制扫描结果",
            parent=parent
        )
        self.setObjectName('displayInterface')
        self.displayDict = {
            '温度': 'temperatureDisplay',
            '电流': 'currDisplay',
            '电压': 'voltDisplay',
            '流量': 'flowDisplay',
            '压力': 'pressureDisplay',
            '温度变送器': 'transmitterDisplay',
            '其他': 'otherDisplay',
        }

    def initDisplay(self):
        parseData = self.parsePlotData(self.mainWindow.scanResultData)
        logger.info(f'解析数据: {parseData}')
        displayList = parseData.keys()
        channelList = []
        for v in parseData.values():
            for i in range(len(v)):
                channelList.append(v[i]['channel'])

        logger.info(f'显示列表: {displayList}')
        for displayCard in displayList:
            card = self.addExampleCard(
                    title=self.tr(f'{displayCard}曲线'),
                    widget=DisplayFrame(parent=self,
                                        title=f'{displayCard}曲线',
                                        subtitle=f'扫描通道: {channelList}',
                                        xlabel='时间',
                                        xunits='s'),
                )
            setattr(self, self.displayDict[displayCard],card) 


    @property
    def createPlotThread(self)->CreateThread:
        plotThread = CreateThread()
        plotThread.display = True
        plotThread.flushpDisplay.connect(self.displayPlot)
        plotThread.timeInterval = self.inst.scanInterval
        return plotThread
    
    def displayPlot(self, isFlush:bool = True):
        if not isFlush:
            return

        for physicalType, data in self.parsePlotData(self.mainWindow.scanResultData).items():
            if physicalType == '温度':
                self.temperatureDisplay.widget.plotGraphic(
                    # pen = next(colorList),
                    plotData = data,
                    )
            elif physicalType == '电流':
                self.currDisplay.widget.plotGraphic(
                    # pen = next(colorList),
                    plotData = data,
                    )
            elif physicalType == '电压':
                self.voltDisplay.widget.plotGraphic(
                    # pen = next(colorList),
                    plotData = data,
                    )
            elif physicalType == '流量':
                self.flowDisplay.widget.plotGraphic(
                    # pen = next(colorList),
                    plotData = data,
                    )
            elif physicalType == '压力':
                self.pressureDisplay.widget.plotGraphic(
                    # pen = next(colorList),
                    plotData = data,
                    )
            elif physicalType == '温度变送器':
                self.transmitterDisplay.widget.plotGraphic(
                    # pen = next(colorList),
                    plotData = data,
                    )
            else:
                ...
    def parsePlotData(self, dic):
        # 定义一个空字典，用来存储按照type分组后的结果
        result = {}

        # 遍历字典中的每一项
        for key, value in dic.items():
            # 获取当前项的类型，数据，单位和时间
            type = value["type"]
            data = value["data"]
            unit = value["unit"]
            time = value["time"]
            
            # 如果当前类型已经在结果字典中，说明已经分组过，将当前项添加到对应的列表中
            if type in result:
                result[type].append({"channel": key, "unit": unit, "data": data, "time": time})
            
            # 否则，将当前类型作为一个新的键，创建一个空列表作为值，并将当前项添加到列表中
            else:
                result[type] = [{"channel": key, "unit": unit, "data": data, "time": time}]
        return result

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.DEFAULT_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class DisplayFrame(Frame):

    def __init__(self, parent, title=None, subtitle=None,ylabel=None,yunits=None,xlabel=None,xunits=None):
        super().__init__(parent)
        self.__initPlot(title, subtitle,ylabel,yunits,xlabel,xunits)
    
    def __initPlot(self,title, subtitle,ylabel=None,yunits=None,xlabel=None,xunits=None, *args, **kwargs):
        self.scanPlot = PlotWidget()
        self.scanPlot.setTitle(title=title, subtitle=subtitle)
        if ylabel and yunits:
            self.scanPlot.setLabel('left', ylabel, units=yunits)
        if xlabel and xunits:
            self.scanPlot.setLabel('bottom', xlabel, units=xunits)
        if kwargs.get('showGrid',True):
            self.scanPlot.showGrid(x=True, y=True)
        self.scanPlot.addLegend()

        self.scanPlot.setBackground('white')
        self.scanPlot.setFixedHeight(250)
        self.addWidget(self.scanPlot)

    def plotGraphic(self, **kwargs):

        plotData = kwargs.get('plotData')
        # 清除上一步的绘图结果
        self.scanPlot.clear()
        self.scanPlot.setLabel('left',  units=plotData[0]['unit'])
        for i in range(len(plotData)):
            plotTime = np.array(plotData[i]['time']) - plotData[i]['time'][0]
            self.scanPlot.plot(plotTime, plotData[i]['data'], pen=colorList[i], name=plotData[i]['channel'])
        ...
