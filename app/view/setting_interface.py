# coding:utf-8
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,CardWidget,
                            OptionsSettingCard, PushSettingCard,ToolButton,AvatarWidget,IconWidget,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,SettingCard,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,CaptionLabel,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme,FluentStyleSheet)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths,QSize
from PyQt5.QtWidgets import QWidget, QLabel,QPushButton, QFileDialog,QHBoxLayout,QVBoxLayout,QFrame
from PyQt5.QtGui import QPixmap
from .gallery_interface import GalleryInterface,ToolBar

from ..common.config import cfg, AUTHOR, VERSION, YEAR, isWin11
from ..common.style_sheet import  StyleSheet
from ..common.signal_bus import signalBus
from ..components.utils import ContributorList


class SettingInterface(GalleryInterface,ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(
            title='设置',
            subtitle='',
            parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName('settingInterface')

        # personalization
        self.personalGroup = SettingCardGroup(
            '个性化', self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            '云母效果',
            '窗口和表面显示半透明',
            cfg.micaEnabled,
            self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            '界面缩放',
            '调整小部件和字体的大小',
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                '使用系统设置'
            ],
            parent=self.personalGroup
        )
        # about
        self.aboutGroup = SettingCardGroup('关于', self.scrollWidget)
        # contributorList = QWidget()
        # from ..components.utils import ContributorList
        # for i in range(len(ContributorList.contributorList)):
        #     contributorButton = ToolButton(ContributorList.contributorList[i]['name'],parent = contributorList)
        #     contributorButton.setIconSize(QSize(40, 40))
        #     contributorButton.resize(70, 70)
        #     contributorButton.setToolTip(ContributorList.contributorList[i]['name'])
            
        self.aboutCard = SettingCard(
            icon = FIF.INFO,
            title='版本信息',
            content='© ' + 'Copyright' + f" {YEAR}. " +
            '当前版本' + " " + VERSION +'\n'+ 'Powerd by PyQt-Fluent-Widgets & pyvisa',
            parent=self.aboutGroup
        )
        # self.contributorCard = ContributorCard(
        #     icon=FIF.PEOPLE,
        #     title="贡献者",
        #     content=0,
        #     parent=self.aboutGroup
        # )
        # self.contributorCard.initLayout()
        self.contributorCard2 = ContributorCard(
            parent=self.aboutGroup
        )
        # self.contributorCard2.initLayout()        
        # url = QPixmap(r'app\resource\avatar\db.png')
        # self.card = AvatarWidget(url,self)

        # self.nameLable = QLabel()
        # self.nameLable.setText('name')

        self.__initWidget()
        # self.aboutCard.
    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        # self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.micaCard.setEnabled(isWin11())


        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):

        # add cards to group
        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        # self.aboutGroup.addSettingCard(self.contributorCard)
        self.aboutGroup.addSettingCard(self.contributorCard2)
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        # personalization
        self.themeColorCard.colorChanged.connect(setThemeColor)
        self.micaCard.checkedChanged.connect(signalBus.micaEnableChanged)

class ContributorCard_old(SettingCard):
    """ Setting card """
       
    def initLayout(self):
        self.setFixedHeight(150)

        contributorBoxLetout = QHBoxLayout()
        contributorBoxLetout.addSpacing(30)
        # contributorBoxLetout.setAlignment()
        # url = QPixmap(r'app\resource\avatar\db.png')
        # card = AvatarWidget(url,self)
        # self.vBoxLayout.addWidget(card)        
        for contributor in ContributorList.contributorList:
            avatarBoxLayout = QVBoxLayout()

            name = contributor['name']
            nameLable = CaptionLabel()
            nameLable.setText(name)

            avatar = QPixmap(contributor['avatar'])
            ava = AvatarWidget(avatar, self)
            ava.setRadius(40)
            
            avatarBoxLayout.addWidget(ava,alignment=Qt.AlignHCenter)
            avatarBoxLayout.addWidget(nameLable,alignment=Qt.AlignHCenter)
            avatarBoxLayout.setContentsMargins(3, 3, 3, 3)
            contributorBoxLetout.addLayout(avatarBoxLayout)
       
        self.vBoxLayout.addLayout(contributorBoxLetout)
        self.vBoxLayout.addSpacing(30)

class ContributorCard(QFrame):
    """ Setting card """
    def __init__(self, parent=None):
        """ parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.iconLabel = IconWidget(FIF.PEOPLE, self)
        self.titleLabel = QLabel('贡献者', self)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.initLayout()
        self.setFixedHeight(200)
        self.iconLabel.setFixedSize(16, 16)
        
    def initLayout(self):
        self.setFixedHeight(150)
        titleAndIconBoxLetout = QHBoxLayout()
        contributorBoxLetout = QHBoxLayout()
       
        for contributor in ContributorList.contributorList:
            avatarBoxLayout = QVBoxLayout()

            name = contributor['name']
            link = contributor['github']
            nameLable = QLabel()
            nameLable.setText('<a href="'+link+'">'+name+'</a>')
            nameLable.setOpenExternalLinks(True)

            avatar = QPixmap(contributor['avatar'])
            ava = AvatarWidget(avatar, self)
            ava.setRadius(32)
            
            avatarBoxLayout.addWidget(ava,alignment=Qt.AlignHCenter)
            avatarBoxLayout.addWidget(nameLable,alignment=Qt.AlignHCenter)
            avatarBoxLayout.setContentsMargins(0, 0, 0, 0)
            avatarBoxLayout.setSpacing(5)
            contributorBoxLetout.addLayout(avatarBoxLayout)

        contributorBoxLetout.addSpacing(32)
        contributorBoxLetout.setContentsMargins(32, 0, 0, 0)
        contributorBoxLetout.setAlignment(Qt.AlignLeft)
        contributorBoxLetout.setSpacing(32)

        titleAndIconBoxLetout.addSpacing(16)
        titleAndIconBoxLetout.addWidget(self.iconLabel, 0, Qt.AlignLeft)
        titleAndIconBoxLetout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        titleAndIconBoxLetout.addStretch(1)

        self.vBoxLayout.addLayout(titleAndIconBoxLetout)
        self.vBoxLayout.addLayout(contributorBoxLetout)
        self.vBoxLayout.addSpacing(30)

        # 使用qss设置背景颜色
        self.setStyleSheet(
            '''
            ContributorCard {
                border: 1px solid rgba(0, 0, 0, 0.095);
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.667);
            }
            '''
        )

