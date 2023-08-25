# coding:utf-8
import sys
from time import sleep
import time

from PyQt5.QtCore import Qt, QUrl, pyqtSlot, QEasingCurve
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout,
                             QStyleOptionToolBar, QWidget,QVBoxLayout)

from InstConfig_ui import Ui_InstConfig
from app.components.agilent34970a import Agilent34970A
from qfluentwidgets import FluentIcon
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (InfoBar, InfoBarIcon, InfoBarManager,StateToolTip,
                            InfoBarPosition, MessageBox, MSFluentWindow,
                            NavigationAvatarWidget, NavigationItemPosition,
                            PushButton, SubtitleLabel, Theme, qrouter, setFont,
                            setTheme,ScrollArea)


class InstConfig(ScrollArea, QWidget, Ui_InstConfig, Agilent34970A):

    def __init__(self, inst):
        self.inst = inst
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        # UI设置
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.view.setObjectName('view')
        self.view.setStyleSheet('background-color: #f5f5f5;')
        # self.view.setStyleSheet('border: none;background-color: transparent;')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        # 仪器配置
        comlist = self.inst.getComList
        self.SetCom.addItems(['选择端口']+list(comlist)+['刷新'])    # 选择端口

        def flush_com():
            if self.SetCom.currentIndex() == self.SetCom.count()-1:
                self.SetCom.clear()
                comlist = self.inst.getComList
                self.SetCom.addItems(['选择端口']+list(comlist)+['刷新'])    # 选择端口
                self.SensorType.setCurrentIndex(0)
                self.createSuccessInfoBar('成功', '已刷新端口列表')
        self.SetCom.currentIndexChanged.connect(flush_com)
        self.Baudrate.addItems(
            ['波特率', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        self.Timeout.addItems(['超时时间(s)', '0', '5', '10', '20', '30', '60'])
        self.ScanInterval.setPlaceholderText('扫描间隔(s)')
        self.InitInstButton.clicked.connect(self.init_button_clicked)
        self.CheckInstButton.clicked.connect(self.check_button_clicked)

        # 温度测量
        # '热电偶','热敏电阻','热电阻',
        self.ProbeType.addItems(['传感器类型', '热电偶', '热敏电阻', '热电阻', '4线热电阻'])

        def choose_sensor(index):
            if self.SensorType.count() > 0:
                self.SensorType.clear()
            if index == 0:
                self.SensorType.addItem('-传感器型号-')
            if index == 1:
                self.SensorType.addItems(
                    ['热电偶型号', 'K', 'J', 'T', 'E', 'N', 'R', 'S', 'B'])
            elif index == 2:
                self.SensorType.addItems(['热敏电阻型号', '2252', '5000', '10000'])
            elif index == 3:
                self.SensorType.addItems(['热电阻型号', '85', '91'])
            elif index == 4:
                self.SensorType.addItems(['4线热电阻型号', '85', '91'])
            else:
                self.SensorType.clear()
        self.ProbeType.currentIndexChanged.connect(choose_sensor)
        self.TemperatureUnit.addItems(['温度单位', 'C', 'F', 'K'])     # 温度单位
        self.TempChannelList.setPlaceholderText(
            '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。例如:\n101,102,109\n104:111')

        self.TempConfButton.clicked.connect(self.temp_conf_button_clicked)

        # 电流测量
        self.CurrChannelList.setPlaceholderText(
            '输入要配置的通道，通道之间用逗号分隔。对于一系列通道，输入以冒号分隔的第一个和最后一个通道。例如:\n101,102,109\n104:111')
        self.CurrType.addItems(['AC/DC', 'AC', 'DC'])
        self.CurrRange.addItems(['电流范围', 'AUTO', '10mA', '100mA', '1A'])
        self.CurrConfButton.clicked.connect(self.curr_conf_button_clicked)

        # Test
        self.TestB.clicked.connect(self.test_button_clicked)


    def test_button_clicked(self):
        sleep(1)


    def init_button_clicked(self):
        '''
        连接和初始化仪器
        '''
        # 设置默认值
        com = None
        baude_rate = 9600
        timeout = 10*1000
        reset = False
        cls = False
        ScanInterval = 10
        # 判断输入是否正确
        if self.SetCom.currentIndex() == 0:
            self.createErrorInfoBar('错误', '请选择端口')
            return
        else:
            com = self.SetCom.currentText()
        if self.Baudrate.currentIndex() == 0:
            self.createErrorInfoBar('警告', '未选择波特率，设置为默认值9600')
        else:
            baude_rate = int(self.Baudrate.currentText())
        if self.Timeout.currentIndex() == 0:
            self.createErrorInfoBar('警告', '未选择超时时间，设置为默认值10s')
        else:
            timeout = int(self.Timeout.currentText())*1000
        if self.ScanInterval.text() == '':
            self.createErrorInfoBar('警告', '未输入扫描间隔，设置为默认值10s')
        else:
            ScanInterval = int(self.ScanInterval.text())
        # 初始化仪器
        id = self.inst.connectInstrument(
            com, baude_rate, timeout, reset=reset, cls=cls, ScanInterval=ScanInterval)
        if type(id) == str:
            self.createSuccessInfoBar('成功', '已初始化仪器'+str(id))
        else:
            self.createErrorInfoBar('错误', '初始化失败: '+str(id)+'请重试')
            return
        return id


    def check_button_clicked(self, **kargs):
        '''
        执行仪器自检
        '''
        if not self.inst.connectState:
            self.createErrorInfoBar('错误', '仪器未连接，请先初始化仪器')
            return
        flag = self.inst.testInst()
        if flag == 'passed':
            self.createSuccessInfoBar('成功', '仪器检查通过')
            return
        elif flag == 'failed':
            self.createErrorInfoBar('错误', '仪器自检未通过，请检查仪器!')
            return
        else:
            self.createErrorInfoBar('错误', '仪器自检操作失败: '+str(flag)+'建议增加超时时间')
            return

    def temp_conf_button_clicked(self):
        '''
        配置温度通道
        '''
        if not self.inst.connectState:
            self.createErrorInfoBar('错误', '仪器未连接，请先初始化仪器')
            return
        # 设置默认值
        probe_type = None
        sensor_type = ''
        channel_list = ''
        temperature_unit = 'C'
        # 判断输入是否正确
        if self.ProbeType.currentIndex() == 0:
            self.createErrorInfoBar('错误', '请选择传感器类型')
            return
        else:
            probe_type = self.ProbeType.currentIndex()
        if self.SensorType.currentIndex() == 0:
            self.createErrorInfoBar('错误', '请选择传感器型号')
            return
        else:
            sensor_type = self.SensorType.currentText()
        if self.TempChannelList.toPlainText() == '':
            self.createErrorInfoBar('错误', '请输入通道列表')
            return
        else:
            channel_list = self.TempChannelList.toPlainText()
        if self.TemperatureUnit.currentIndex() == 0:
            self.createWarningInfoBar('警告', '未选择温度单位，设置为默认值℃')
        else:
            temperature_unit = self.TemperatureUnit.currentText()
        # 配置温度通道
        # print(probe_type, sensor_type, channel_list, temperature_unit)
        try:
            self.inst.confTemp(probe_type, sensor_type,
                               channel_list, temperature_unit)
            self.createSuccessInfoBar('成功', '已配置温度通道')
        except Exception as e:
            self.createErrorInfoBar('错误', '配置失败: ' + str(e))
            return
        ...

    def curr_conf_button_clicked(self):
        '''
        配置电流通道
        '''
        if not self.inst.connectState:
            self.createErrorInfoBar('错误', '仪器未连接，请先初始化仪器')
            return
        # 设置默认值
        curr_type = 'DC'
        curr_range = 'AUTO'
        channel_list = ''
        # 判断输入是否正确
        if self.CurrChannelList.toPlainText() == '':
            self.createErrorInfoBar('错误', '请输入通道列表')
            return
        else:
            channel_list = self.CurrChannelList.toPlainText()
        if self.CurrType.currentIndex() == 0:
            self.createWarningInfoBar('警告', '未选择电流类型，设置为默认值DC')
        else:
            curr_type = self.CurrType.currentText()
        if self.CurrRange.currentIndex() == 0:
            self.createWarningInfoBar('警告', '未选择电流范围，设置为默认值AUTO')
        else:
            curr_range = self.CurrRange.currentText()

        # 初始化电流通道
        try:
            self.inst.confCurr(curr_type, curr_range, channel_list)
            self.createSuccessInfoBar('成功', '已配置电流通道')
        except Exception as e:
            self.createErrorInfoBar('错误', '配置失败: '+str(e))
            return
        ...

    def scan_button_clicked(self):
        while True:
            self.inst.scanAll()
            sleep(self.inst.ScanInterval)

        ...
######################################信息展示######################################
    # 信息栏-成功
    def createSuccessInfoBar(self, title='Success', message=''):
        # convenient class mothod
        InfoBar.success(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=1000,
            parent=self
        )
    # 信息栏-错误
    def createErrorInfoBar(self, title = 'Error', message=''):
        # convenient class mothod
        InfoBar.error(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=5000,
            parent=self
        )
    # 信息栏-警告
    def createWarningInfoBar(self, title='Warning', message=''):
        # convenient class mothod
        InfoBar.warning(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=1500,
            parent=self
        )

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = InstConfig()
    w.show()
    sys.exit(app.exec_())
