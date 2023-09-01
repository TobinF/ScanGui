# coding:utf-8
import time
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QWidget, QFrame,  QHBoxLayout, QVBoxLayout)
from qfluentwidgets import EditableComboBox, PlainTextEdit, CheckBox, LineEdit,ComboBox,CardWidget, PushButton, FlowLayout
from qfluentwidgets import FluentIcon as FIF
from loguru import logger

from .gallery_interface import GalleryInterface,ToolBar
from ..config.InstConfig import ConfigImport
from ..common.style_sheet import StyleSheet
from ..components.info_bar import CreateInfoBar
from ..components.utils import channelInputCheck
from ..components.agilent34970a import Agilent34970A


class ConfInterface(GalleryInterface):
    """ Config interface """

    def __init__(self, inst:Agilent34970A, parent=None):
        super().__init__(
            title='仪器配置',
            subtitle="仪器初始化和通道配置",            
            parent=parent
        )
        self.setObjectName('confInterface')

        # set cards
        self.addExampleCard(
            title=self.tr('仪器初始化'),
            widget=InitInstFrame(inst,self),
        )
        self.addExampleCard(
            title=self.tr('温度通道配置'),
            widget=InitTempChannelFrame(inst,self),
        )
        self.addExampleCard(
            title=self.tr('电流通道配置'),
            widget=InitCurrChannelFrame(inst,self),
        )
        self.addExampleCard(
            title=self.tr('计算通道配置'),
            widget=InitCalculatedFrame(inst,self),
        )


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.CONF_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)

class InitInstFrame(Frame, QWidget):
    def __init__(self,inst, parent=None):
        self.inst:Agilent34970A = inst
        super().__init__(parent)
        self.mainWindow = parent
        self.card = CardWidget(self)
        self.toolBar = ToolBar(parent=None)
        self.widgetLayout = QVBoxLayout()
        self.__initInstView()
        self.addWidget(self.card)

    def __initInstView(self):
        
        comboBoxLayout = QHBoxLayout()
        CheckBoxLayout = QHBoxLayout()
        buttonBoxLayout = QHBoxLayout()

        self.setCom = ComboBox()
        self.baudRate = ComboBox()
        self.timeOut = ComboBox()
        self.scanInterval = LineEdit()
        self.resetInst = CheckBox()
        self.clsInst = CheckBox()
        self.resetInst.setText('重设仪器')
        self.clsInst.setText('清除寄存器')
        self.initInstButton = PushButton()
        self.initInstButton.setText('提交配置')
        self.initInstButton.setIcon(FIF.ACCEPT)
        self.testInstButton = PushButton()
        self.testInstButton.setText('测试仪器')
        self.testInstButton.setIcon(FIF.SETTING)
        self.importConfButton = PushButton()
        self.importConfButton.setText('导入配置')
        self.importConfButton.setIcon(FIF.LINK)

        # 设置控件大小
        self.setCom.setFixedSize(120, 32)
        self.baudRate.setFixedSize(120, 32)
        self.timeOut.setFixedSize(120, 32)
        self.scanInterval.setFixedSize(120, 32)
        self.resetInst.setFixedSize(120, 32)
        self.clsInst.setFixedSize(120, 32)
        self.initInstButton.setFixedSize(120, 32)
        self.testInstButton.setFixedSize(120, 32)
        
        comboBoxLayout.addWidget(self.setCom)
        comboBoxLayout.addWidget(self.baudRate)
        comboBoxLayout.addWidget(self.timeOut)
        comboBoxLayout.addWidget(self.scanInterval)
        CheckBoxLayout.addWidget(self.resetInst)
        CheckBoxLayout.addWidget(self.clsInst)
        buttonBoxLayout.addWidget(self.testInstButton)
        buttonBoxLayout.addWidget(self.initInstButton)
        buttonBoxLayout.addWidget(self.importConfButton)
        # 设置布局间隔
        comboBoxLayout.setSpacing(20)
        CheckBoxLayout.setSpacing(20)
        buttonBoxLayout.setSpacing(20)
        # 设置布局对齐方式
        comboBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        CheckBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        buttonBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignRight)

        self.widgetLayout.addLayout(comboBoxLayout)
        self.widgetLayout.addLayout(CheckBoxLayout)
        self.widgetLayout.addLayout(buttonBoxLayout)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.widgetLayout.setSpacing(20)
        self.widgetLayout.setContentsMargins(20, 20, 20, 20)

        # 仪器配置
        comlist = self.inst.getComList
        self.setCom.addItems(['选择端口']+list(comlist)+['刷新'])    # 选择端口
        def flush_com():
            if self.setCom.currentIndex() == self.setCom.count()-1:
                self.setCom.clear()
                comlist = self.inst.getComList
                self.setCom.addItems(['选择端口']+list(comlist)+['刷新'])    # 选择端口
                self.setCom.setCurrentIndex(0)
                CreateInfoBar.createSuccessInfoBar(self.mainWindow,'成功', '已刷新端口列表')
        self.setCom.currentIndexChanged.connect(flush_com)
        self.baudRate.addItems(
            ['波特率', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        self.timeOut.addItems(['超时时间(s)', '0', '5', '10', '20', '30', '60'])
        self.scanInterval.setPlaceholderText('扫描间隔(s)')
        self.card.setLayout(self.widgetLayout)
        self.setFixedHeight(200)        
        
        # 设置按钮点击事件
        self.initInstButton.clicked.connect(self.initInstButtonOnClicked)
        self.testInstButton.clicked.connect(self.testInstButtOnClicked)
        self.importConfButton.clicked.connect(self.importConfButtonOnClicked)


    def initInstButtonOnClicked(self):
        '''
        连接和初始化仪器
        '''
        # 设置默认值
        com = None
        baude_rate = 9600
        timeout = 10*1000
        reset = False
        cls = False
        scanInterval = 10
        # 判断输入是否正确
        if self.setCom.currentIndex() == 0:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '请选择端口')
            return
        else:
            com = self.setCom.currentText()
        if self.baudRate.currentIndex() == 0:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'警告', '未选择波特率，设置为默认值9600')
        else:
            baude_rate = int(self.baudRate.currentText())
        if self.timeOut.currentIndex() == 0:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'警告', '未选择超时时间，设置为默认值10s')
        else:
            timeout = int(self.timeOut.currentText())*1000
        if self.scanInterval.text() == '':
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'警告', '未输入扫描间隔，设置为默认值10s')
        else:
            scanInterval = float(self.scanInterval.text())
            
        if self.resetInst.isChecked():
            reset = True
        if self.clsInst.isChecked():
            cls = True
        # 初始化仪器
        id = self.inst.connectInstrument(
            com, baude_rate, timeout, reset=reset, cls=cls, scanInterval=scanInterval)
        if type(id) == str:
            CreateInfoBar.createSuccessInfoBar(self.mainWindow,'成功', '已初始化仪器'+str(id))
        else:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '初始化失败: '+str(id)+'请重试')
            return
        return id
    
    def testInstButtOnClicked(self, **kargs):
        '''
        执行仪器自检
        '''
        if not self.inst.connectState:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器未连接，请先初始化仪器')
            return
        flag = self.inst.testInst()
        if flag == 'passed':
            CreateInfoBar.createSuccessInfoBar(self.mainWindow,'成功', '仪器检查通过')
            return
        elif flag == 'failed':
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器自检未通过，请检查仪器!')
            return
        else:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器自检操作失败: '+str(flag)+'建议增加超时时间')
            return

    def importConfButtonOnClicked(self, **kargs):
        fileName = r'instConfig.ini'
        if not self.inst.connectState:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器未连接，请先初始化仪器')
            return
        config = ConfigImport(fileName,self.mainWindow)
        # 温度通道配置
        self.inst.inst.write('CONF:TEMP %s,%s,%s,%s'%(config.TemperatureConf.probe_type,
                                                      config.TemperatureConf.sensor_type,
                                                      config.TemperatureConf.channel_list))
        self.inst.inst.write('UNIT:TEMP %s,%s'%(config.TemperatureConf.temperature_Unit,
                                                config.TemperatureConf.channel_list))
        # 电流通道配置
        self.inst.inst.write('CONF:CURR %s,%s,%s'%(config.CurrentConf.curr_type,
                                                    config.CurrentConf.curr_range,
                                                    config.CurrentConf.channel_list))
        # 计算通道配置
        # self.inst.inst.write('CONF:CALC %s,%s,%s,%s,%s,%s,%s,%s'%(config.CalculatedConf.curr_type,
        #                                                         config.CalculatedConf.curr_range,
        #                                                         config.CalculatedConf.channel_list,
        #                                                         config.CalculatedConf.measure_type,
        #                                                         config.CalculatedConf.measure_unit,
        #                                                         config.CalculatedConf.curr_range_min,
        #                                                         config.CalculatedConf.curr_range_max,
        #                                                         config.CalculatedConf.measure_range_min,
        #                                                         config.CalculatedConf.measure_range_max))
        ...
        CreateInfoBar.createSuccessInfoBar(self.mainWindow,'成功', '已导入配置')


class InitTempChannelFrame(Frame, QWidget):
    def __init__(self,inst, parent=None):
        self.inst:Agilent34970A = inst
        super().__init__(parent)
        self.mainWindow = parent
        self.toolBar = ToolBar(parent=None)
        self.card = CardWidget(self)
        self.widgetLayout = QVBoxLayout()
        self.__initTempChannelView()
        self.addWidget(self.card)

    def __initTempChannelView(self):
        
        comboBoxLayout = QHBoxLayout()
        textBoxLayout = QHBoxLayout()
        buttonBoxLayout = QHBoxLayout()

        self.probeType = ComboBox()
        self.sensorType = ComboBox()
        self.temperatureUnit = ComboBox()
        self.tempChannelList = PlainTextEdit()
        self.tempConfButton= PushButton()
        self.probeType.setText('探头类型')
        self.sensorType.setText('传感器类型')
        self.temperatureUnit.setText('温度单位')
        self.tempConfButton.setText('提交配置')
        self.tempConfButton.setIcon(FIF.ACCEPT)
        self.tempChannelList.setPlaceholderText(
            '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。例如:\n101,102,109\n104:111')

        # 设置控件大小
        self.probeType.setFixedSize(120, 32)
        self.sensorType.setFixedSize(120, 32)
        self.temperatureUnit.setFixedSize(120, 32)
        self.tempChannelList.setMaximumHeight(100)
        self.tempChannelList.setMaximumWidth(800)
        self.tempConfButton.setFixedSize(120, 32)
        
        # 添加控件到布局
        comboBoxLayout.addWidget(self.probeType)
        comboBoxLayout.addWidget(self.sensorType)
        comboBoxLayout.addWidget(self.temperatureUnit)
        textBoxLayout.addWidget(self.tempChannelList)
        buttonBoxLayout.addWidget(self.tempConfButton)
        # 设置布局间隔
        comboBoxLayout.setSpacing(20)
        textBoxLayout.setSpacing(20)
        buttonBoxLayout.setSpacing(20)
        # 设置布局对齐方式
        comboBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout.setContentsMargins(0, 0, 0, 0)
        buttonBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignRight)
        buttonBoxLayout.setContentsMargins(0, 0, 0, 20)
        # 添加布局到主布局
        self.widgetLayout.addLayout(comboBoxLayout)
        self.widgetLayout.addLayout(textBoxLayout)
        self.widgetLayout.addLayout(buttonBoxLayout)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.widgetLayout.setSpacing(20)
        self.widgetLayout.setContentsMargins(20, 20, 20, 0)
        # 添加布局到卡片控件
        self.card.setLayout(self.widgetLayout)
        self.setFixedHeight(300)
        # 添加控件内容
        self.probeType.addItems(['传感器类型', '热电偶', '热敏电阻', '热电阻', '4线热电阻'])

        def chooseSensor(index):
            if self.sensorType.count() > 0:
                self.sensorType.clear()
            if index == 0:
                self.sensorType.addItem('-传感器型号-')
            if index == 1:
                self.sensorType.addItems(
                    ['热电偶型号', 'K', 'J', 'T', 'E', 'N', 'R', 'S', 'B'])
            elif index == 2:
                self.sensorType.addItems(['热敏电阻型号', '2252', '5000', '10000'])
            elif index == 3:
                self.sensorType.addItems(['热电阻型号', '85', '91'])
            elif index == 4:
                self.sensorType.addItems(['4线热电阻型号', '85', '91'])
            else:
                self.sensorType.clear()
        self.probeType.currentIndexChanged.connect(chooseSensor)
        self.temperatureUnit.addItems(['温度单位', 'C', 'F', 'K'])     # 温度单位

        # 设置按钮点击事件
        self.tempConfButton.clicked.connect(self.tempConfButtonOnClicked)    

    def tempConfButtonOnClicked(self):
        '''
        配置温度通道
        '''
        if not self.inst.connectState:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器未连接，请先初始化仪器')
            return
        # 设置默认值
        probe_type = None
        sensor_type = ''
        channel_list = ''
        temperature_unit = 'C'
        # 判断输入是否正确
        if self.probeType.currentIndex() == 0:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '请选择传感器类型')
            return
        else:
            probe_type = self.probeType.currentIndex()
        if self.sensorType.currentIndex() == 0:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '请选择传感器型号')
            return
        else:
            sensor_type = self.sensorType.currentText()
        _tempChannelList = self.tempChannelList.toPlainText().replace('，', ',').replace('：', ':')
        if _tempChannelList == '':
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '请输入通道列表')
            return
        elif not channelInputCheck(_tempChannelList):
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '通道输入格式错误')
            return
        else:
            channel_list = _tempChannelList
        if self.temperatureUnit.currentIndex() == 0:
            CreateInfoBar.createWarningInfoBar(self.mainWindow,'警告', '未选择温度单位，设置为默认值℃')
        else:
            temperature_unit = self.temperatureUnit.currentText()
        # 配置温度通道
        # print(probe_type, sensor_type, channel_list, temperature_unit)
        try:
            self.inst.confTemp(probeType = probe_type, 
                               sensorType = sensor_type,
                               channelListStr = channel_list, 
                               temperatureUnit = temperature_unit
                               )
            # time.sleep(0.1)
            # self.mainWindow.scanResultData = self.inst.channelListDict
            CreateInfoBar.createSuccessInfoBar(self.mainWindow,'成功', '已配置温度通道')
            
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '配置失败: ' + str(e))
            return

        ...

class InitCurrChannelFrame(Frame, QWidget):
    def __init__(self,inst, parent=None):
        self.inst:Agilent34970A = inst
        super().__init__(parent)
        self.mainWindow = parent
        self.toolBar = ToolBar(parent=None)
        self.card = CardWidget(self)
        self.widgetLayout = QVBoxLayout()
        self.__initCurrChannelView()
        self.addWidget(self.card)

    def __initCurrChannelView(self):
        
        comboBoxLayout = QHBoxLayout()
        textBoxLayout = QHBoxLayout()
        buttonBoxLayout = QHBoxLayout()

        self.currType = ComboBox()
        self.currRange = ComboBox()
        self.currChannelList = PlainTextEdit()
        self.currConfButton= PushButton()
        self.currType.setText('AC/DC')
        self.currRange.setText('电流范围')
        self.currConfButton.setText('提交配置')
        self.currConfButton.setIcon(FIF.ACCEPT)
        self.currChannelList.setPlaceholderText(
            '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。例如:\n101,102,109\n104:111')

        # 设置控件大小
        self.currType.setFixedSize(120, 32)
        self.currRange.setFixedSize(120, 32)
        self.currChannelList.setMaximumHeight(100)
        self.currChannelList.setMaximumWidth(800)
        self.currConfButton.setFixedSize(120, 32)
        
        # 添加控件到布局
        comboBoxLayout.addWidget(self.currType)
        comboBoxLayout.addWidget(self.currRange)
        textBoxLayout.addWidget(self.currChannelList)
        buttonBoxLayout.addWidget(self.currConfButton)
        # 设置布局间隔
        comboBoxLayout.setSpacing(20)
        textBoxLayout.setSpacing(20)
        buttonBoxLayout.setSpacing(20)
        # 设置布局对齐方式
        comboBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout.setContentsMargins(0, 0, 0, 0)
        buttonBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignRight)
        buttonBoxLayout.setContentsMargins(0, 0, 0, 20)
        # 添加布局到主布局
        self.widgetLayout.addLayout(comboBoxLayout)
        self.widgetLayout.addLayout(textBoxLayout)
        self.widgetLayout.addLayout(buttonBoxLayout)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.widgetLayout.setSpacing(20)
        self.widgetLayout.setContentsMargins(20, 20, 20, 0)
        # 添加布局到卡片控件
        self.card.setLayout(self.widgetLayout)
        self.setFixedHeight(300)
        # 添加控件内容
        self.currChannelList.setPlaceholderText(
            '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。例如:\n101,102,109\n104:111')
        self.currType.addItems(['AC/DC', 'AC', 'DC'])
        self.currRange.addItems(['电流范围(mA)', 'AUTO', '10', '100', '1000'])
        # 设置按钮点击事件
        self.currConfButton.clicked.connect(self.currConfButtonOnClicked)    

    def currConfButtonOnClicked(self):
        '''
        配置温度通道
        '''
        if not self.inst.connectState:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器未连接，请先初始化仪器')
            return
        # 设置默认值
        curr_type = 'DC'
        curr_range = 'AUTO'
        channel_list = ''
        # 判断输入是否正确
        _currChannelList = self.currChannelList.toPlainText().replace('，', ',').replace('：', ':')
        if _currChannelList:
            CreateInfoBar.createErrorInfoBar(self.mainWindow, '错误', '请输入通道列表')
            return
        elif not channelInputCheck(_currChannelList):
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '通道输入格式错误')
            return
        else:
            channel_list = _currChannelList
        if self.currType.currentIndex() == 0:
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未选择电流类型，设置为默认值DC')
        else:
            curr_type = self.currType.currentText()
        if self.currRange.currentIndex() == 0:
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未选择电流范围，设置为默认值AUTO')
        else:
            curr_range = self.currRange.currentText()

        # 初始化电流通道
        try:
            self.inst.confCurr(curr_type, curr_range, channel_list)
            # time.sleep(0.1)
            # self.mainWindow.scanResultData = self.inst.channelListDict

            CreateInfoBar.createSuccessInfoBar(self.mainWindow, '成功', '已配置电流通道')
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.mainWindow, '错误', '配置失败: '+str(e))
            return

class InitCalculatedFrame(Frame, QWidget):
    def __init__(self,inst, parent=None):
        self.inst:Agilent34970A = inst
        super().__init__(parent)
        self.mainWindow = parent
        self.toolBar = ToolBar(parent=None)
        self.card = CardWidget(self)
        self.widgetLayout = QVBoxLayout()
        self.__initCurrChannelView()
        self.addWidget(self.card)

    def __initCurrChannelView(self):
        
        comboBoxLayout = QHBoxLayout()
        textBoxLayout0 = QHBoxLayout()
        textBoxLayout = QHBoxLayout()
        buttonBoxLayout = QHBoxLayout()

        self.currType = ComboBox()
        self.currRange = ComboBox()
        self.measureType = ComboBox()
        self.measureUnits = EditableComboBox()
        self.currRangeMax = LineEdit()
        self.currRangeMin = LineEdit()
        self.mesureRangeMin = LineEdit()
        self.mesureRangeMax = LineEdit()

        self.currChannelList = PlainTextEdit()
        self.currConfButton= PushButton()
        
        self.currType.setText('AC/DC')
        self.currRange.setText('电流范围')
        self.currConfButton.setText('提交配置')
        self.currConfButton.setIcon(FIF.ACCEPT)
        self.currChannelList.setPlaceholderText(
            '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。对于34901A 20通道多路复用器，电流仅支持21，22通道')

        # 设置控件大小
        self.currType.setFixedSize(120, 32)
        self.currRange.setFixedSize(120, 32)
        self.measureType.setFixedSize(120, 32)
        self.measureUnits.setFixedSize(120, 32)
        self.currRangeMax.setFixedSize(120, 32)
        self.currRangeMin.setFixedSize(120, 32)
        self.mesureRangeMin.setFixedSize(120, 32)
        self.mesureRangeMax.setFixedSize(120, 32)
        self.currChannelList.setMaximumHeight(100)
        self.currChannelList.setMaximumWidth(800)
        self.currConfButton.setFixedSize(120, 32)
        
        # 添加控件到布局
        comboBoxLayout.addWidget(self.currType)
        comboBoxLayout.addWidget(self.currRange)
        comboBoxLayout.addWidget(self.measureType)
        comboBoxLayout.addWidget(self.measureUnits)
        textBoxLayout0.addWidget(self.currRangeMin)
        textBoxLayout0.addWidget(self.currRangeMax)
        textBoxLayout0.addWidget(self.mesureRangeMin)
        textBoxLayout0.addWidget(self.mesureRangeMax)
        textBoxLayout.addWidget(self.currChannelList)
        buttonBoxLayout.addWidget(self.currConfButton)
        # 设置布局间隔
        comboBoxLayout.setSpacing(20)
        textBoxLayout.setSpacing(20)
        buttonBoxLayout.setSpacing(20)
        textBoxLayout0.setSpacing(20)
        # 设置布局对齐方式
        comboBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout.setContentsMargins(0, 0, 0, 0)
        buttonBoxLayout.setAlignment(Qt.AlignTop|Qt.AlignRight)
        buttonBoxLayout.setContentsMargins(0, 0, 0, 20)
        textBoxLayout0.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        textBoxLayout0.setContentsMargins(0, 0, 0, 0)
        # 添加布局到主布局
        self.widgetLayout.addLayout(comboBoxLayout)
        self.widgetLayout.addLayout(textBoxLayout0)
        self.widgetLayout.addLayout(textBoxLayout)
        self.widgetLayout.addLayout(buttonBoxLayout)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.widgetLayout.setSpacing(20)
        self.widgetLayout.setContentsMargins(20, 20, 20, 0)
        # 添加布局到卡片控件
        self.card.setLayout(self.widgetLayout)
        self.setFixedHeight(300)
        # 添加控件内容
        self.currChannelList.setPlaceholderText(
                '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。\
                计算通道仅支持21及22的电流通道')
        self.currType.addItems(['AC/DC', 'AC', 'DC'])
        self.currRange.addItems(['电流范围', 'AUTO', '10mA', '100mA', '1A'])
        self.measureType.addItems(['测量类型', '电流', '流量', '压力', '温度变送器', '其他'])
        self.measureUnits.setPlaceholderText('选择测量类型')
        def chooseMesureType(index):
            if self.measureType.count() > 0:
                self.measureUnits.clear()
            if index == 0:
                # self.measureUnits.addItem('-选择单位-')
                self.measureUnits.setPlaceholderText('选择测量类型')
            if index == 1:
                self.measureUnits.setPlaceholderText('电流单位')
                self.measureUnits.addItems(['电流单位','A', 'mA', 'uA'])
            elif index == 2:
                self.measureUnits.setPlaceholderText('流量单位')
                self.measureUnits.addItems(['流量单位','kg/h', 'kg/s', 'm3/h', 'm3/s'])            
            elif index == 3:
                self.measureUnits.setPlaceholderText('压力单位')
                self.measureUnits.addItems(['压力单位','kPa', 'MPa', 'bar'])
            elif index == 4:
                self.measureUnits.setPlaceholderText('温度变送器单位')
                self.measureUnits.addItems(['温度单位','C', 'K', 'F'])
            elif index == 5:
                self.measureUnits.setPlaceholderText('输入单位')
            else:
                self.measureUnits.clear()
        
        self.measureType.currentIndexChanged.connect(chooseMesureType)
        self.currRangeMin.setPlaceholderText('电流范围下限')
        self.currRangeMax.setPlaceholderText('电流范围上限')
        self.mesureRangeMin.setPlaceholderText('测量范围下限')
        self.mesureRangeMax.setPlaceholderText('测量范围上限')


        # 设置按钮点击事件
        self.currConfButton.clicked.connect(self.currConfButtonOnClicked)    

    def currConfButtonOnClicked(self):
        '''
        配置电流通道
        '''
        if not self.inst.connectState:
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '仪器未连接，请先初始化仪器')
            return
        # 设置默认值
        currType = 'DC'
        currRange = 'AUTO'
        measureType = '电流'
        measureUnits = 'mA'
        currRangeMin = 4
        currRangeMax = 20
        mesureRangeMin = 4
        mesureRangeMax = 20
        channelList = ''
        # 判断输入是否正确
        _currChannelList = self.currChannelList.toPlainText().replace('，', ',').replace('：', ':')
        if _currChannelList == '':
            CreateInfoBar.createErrorInfoBar(self.mainWindow, '错误', '请输入通道列表')
            return
        elif not channelInputCheck(_currChannelList):
            CreateInfoBar.createErrorInfoBar(self.mainWindow,'错误', '通道输入格式错误')
            return        
        else:
            channelList = _currChannelList
        if self.currType.currentIndex() == 0:
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未选择电流类型，设置为默认值DC')
        else:
            currType = self.currType.currentText()
        if self.currRange.currentIndex() == 0:
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未选择电流范围，设置为默认值AUTO')
        else:
            currRange = self.currRange.currentText()
        if self.measureType.currentIndex() == 0:
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未选择测量类型，设置为默认值电流')
        else:
            measureType = self.measureType.currentText()
        if self.measureUnits.text() == '':
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未输入测量单位，设置为默认值mA')
        else:
            measureUnits = self.measureUnits.text()
        if self.currRangeMin.text() == '':
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未输入电流范围下限，设置为默认值4')
        else:
            currRangeMin = float(self.currRangeMin.text())
        if self.currRangeMax.text() == '':
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未输入电流范围上限，设置为默认值20')
        else:
            currRangeMax = float(self.currRangeMax.text())
        if self.mesureRangeMin.text() == '':
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未输入测量范围下限，设置为默认值4')
        else:
            mesureRangeMin = float(self.mesureRangeMin.text())
        if self.mesureRangeMax.text() == '':
            CreateInfoBar.createWarningInfoBar(self.mainWindow, '警告', '未输入测量范围上限，设置为默认值20')
        else:
            mesureRangeMax = float(self.mesureRangeMax.text())

        # 初始化计算通道
        try:
            self.inst.confCalulated(currType, currRange, channelList,
                               measureType, measureUnits,
                               currRangeMin,currRangeMax,
                               mesureRangeMin,mesureRangeMax
                               )
            # time.sleep(0.1)
            # self.mainWindow.scanResultData = self.inst.channelListDict
            CreateInfoBar.createSuccessInfoBar(self.mainWindow, '成功', '已配置计算通道')
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.mainWindow, '错误', '配置失败: '+str(e))
            return

