# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout,QVBoxLayout)
from qfluentwidgets import EditableComboBox, PushButton, TextEdit

from app.components.info_bar import CreateInfoBar
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from ..components.agilent34970a import Agilent34970A

from functools import wraps
from func_timeout import func_set_timeout

class CommandInterface(GalleryInterface):
    """ Command interface """

    def __init__(self, inst:Agilent34970A, parent=None):
        self.inst = inst
        super().__init__(
            title='调试工具',
            subtitle="测试仪器SCPI指令",
            parent=parent
        )
        self.setObjectName('commandInterface')

        self.addExampleCard(
            title=self.tr('选择或输入命令'),
            widget=CommandFrame(parent=self),
        )

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.DEFAULT_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class CommandFrame(Frame):

    def __init__(self, parent=None):
        self.MainWindow = parent
        super().__init__(parent)
        self.inst:Agilent34970A = parent.inst
        self.__initCommandFrame()
        self.counts = 1

    def __initCommandFrame(self):
        vBoxLayout = QVBoxLayout()
        buttonBoxLayout = QHBoxLayout()
        self.commandComboBox = EditableComboBox()
        self.commandComboBox.addItems(['---选择或输入指令---', 
                                        '*IDN?--查询仪器ID', 
                                        '*CLS--清除仪器状态', 
                                        '*RST--恢复仪器默认设置',
                                        '*TST?--自检',
                                        '*OPC--等待操作完成',
                                        '*OPC?--查询操作完成状态',
                                        '*WAI--等待操作完成',
                                        '*ESE--使能事件状态寄存器',
                                        '*ESE?--查询事件状态寄存器',
                                        '*ESR?--查询事件状态寄存器',
                                        '*SRE--使能服务请求',
                                        '*SRE?--查询服务请求',
                                        '*STB?--查询状态字节',])

        self.writeButton = PushButton('写入')
        self.writeButton.setFixedSize(120, 32)
        self.writeButton.clicked.connect(self.writeButtonOnClicked)
        self.queryButton = PushButton('查询')
        self.queryButton.setFixedSize(120, 32)
        self.queryButton.clicked.connect(self.queryButtonOnClicked)
        self.readButton = PushButton('读取')
        self.readButton.setFixedSize(120, 32)
        self.readButton.clicked.connect(self.readButtonOnClicked)
        self.clearButton = PushButton('清除')
        self.clearButton.setFixedSize(120, 32)
        self.clearButton.clicked.connect(self.clearButtonOnClicked)        
        buttonBoxLayout.addWidget(self.writeButton)
        buttonBoxLayout.addWidget(self.queryButton)
        buttonBoxLayout.addWidget(self.readButton)
        buttonBoxLayout.addWidget(self.clearButton)
        buttonBoxLayout.setAlignment(Qt.AlignCenter)
        buttonBoxLayout.setSpacing(20)

        self.commandTextEdit = TextEdit()
        self.commandTextEdit.setFixedHeight(300)
        self.commandTextEdit.setReadOnly(True)

        vBoxLayout.addWidget(self.commandComboBox)
        vBoxLayout.addLayout(buttonBoxLayout)
        vBoxLayout.addWidget(self.commandTextEdit)
        self.vBoxLayout = vBoxLayout
        self.hBoxLayout.addLayout(vBoxLayout)

    def isConnect(func):
        @wraps(func)
        def inner(self,*args,**kwargs):
            if self.inst.connectState == False:
                CreateInfoBar.createErrorInfoBar(self.MainWindow, '错误', '请先连接仪器')
                return
            else:
                func(self)
        return inner
        
    @isConnect
    @func_set_timeout(5)
    def writeButtonOnClicked(self):
        try:
            ret = self.inst.inst.write(self.commandComboBox.currentText().split('--')[0])
            self.commandTextEdit.append(str(self.counts)+': write')
            self.commandTextEdit.append('send:  '+str(self.commandComboBox.currentText()))
            self.commandTextEdit.append('return \n:'+str(ret))
            self.counts += 1
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.MainWindow, '错误', str(e))
            return

    @isConnect
    @func_set_timeout(20)
    def queryButtonOnClicked(self):
        try:
            ret = self.inst.inst.query(self.commandComboBox.currentText().split('--')[0])
            self.commandTextEdit.append(str(self.counts)+': query')
            self.commandTextEdit.append('send:  '+self.commandComboBox.currentText())
            self.commandTextEdit.append('return: \n'+ret)
            self.counts += 1
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.MainWindow, '错误', str(e))
            return
    
    @isConnect
    @func_set_timeout(5)
    def readButtonOnClicked(self):
        try:
            ret = self.inst.inst.read()
            self.commandTextEdit.append(str(self.counts)+': read \t')
            self.commandTextEdit.append('return: \n'+ret)
            self.counts += 1
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.MainWindow, '错误', str(e))
            return

    @isConnect
    @func_set_timeout(20)
    def clearButtonOnClicked(self):
        try:
            self.inst.inst.write('*CLS')
            self.commandTextEdit.clear()
            self.counts = 1
        except Exception as e:
            CreateInfoBar.createErrorInfoBar(self.MainWindow, '错误', str(e))
            return

