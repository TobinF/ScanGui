######################################信息展示######################################
from qfluentwidgets import InfoBar, InfoBarPosition, IndeterminateProgressBar
from PyQt5.QtCore import Qt 

class CreateInfoBar():
    # 信息栏-成功
    @staticmethod
    def createSuccessInfoBar(parent, title='Success', message=''):
        # convenient class mothod
        InfoBar.success(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=1500,
            parent=parent
        )
    # 信息栏-错误
    @staticmethod
    def createErrorInfoBar(parent, title = 'Error', message=''):
        # convenient class mothod
        InfoBar.error(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=5000,
            parent=parent
        )
    # 信息栏-警告
    @staticmethod
    def createWarningInfoBar(parent, title='Warning', message=''):
        # convenient class mothod
        InfoBar.warning(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=1500,
            parent=parent
        )
            # 信息栏-警告
    @staticmethod
    def createInfoBar(parent, title='info', message=''):
        # convenient class mothod
        InfoBar.info(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=1500,
            parent=parent
        )

class CreateProcessBar():
    def __init__(self , parent=None) -> None:
        self.bar = IndeterminateProgressBar(parent)
        self.__initBar()
    
    def __initBar(self):
        return self.bar

    def start(self):
        self.bar.start()

    def stop(self):
        self.bar.stop()