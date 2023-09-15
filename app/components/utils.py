import re

from loguru import logger
from .agilent34970a import Agilent34970A

def channelInputCheck(input:str):
    '''
    检测通道输入是否合法
    '''
    pattern = r'^[1-3][0-9][0-9]([,|:][1-3][0-9][0-9])*$'
    return re.match(pattern, input) is not None

class ParseStrInput(Agilent34970A):
    def __init__(self) -> None:
        super().__init__()

    def transString(self, channelListStr:str, unitList:list, typeList:list ,channelListDict:dict):
        '''
        处理通道字符串
        '''
        channelListStr = channelListStr
        # 定义一个空列表，用于存放最终结果
        channelResult = []
        unitResult = []
        typeResult = []
        # 用 , 或 : 分割字符串,
        channelParts = channelListStr.split(",")
        # 如果存在空字符串，则删除
        if "" in channelParts:
            channelParts.remove("")
            # unitParts.remove("")
        partsLength = len(channelParts)
        # 遍历分割后的列表
        for i in range(partsLength):
            # 如果包含 : ，则表示是连续的数字
            if ":" in channelParts[i]:
                # 用 : 分割数字，并转换为整数
                start, end = channelParts[i].split(":")
                # 用 range() 函数生成连续的数字，并添加到结果列表中
                channelResult.extend(range(int(start), int(end) + 1))
                unitResult.extend([unitList[i]]*len(range(int(start), int(end) + 1)))
                typeResult.extend([typeList[i]]*len(range(int(start), int(end) + 1)))
            else:
                # 否则，添加到结果列表中
                channelResult.append(int(channelParts[i]))
                unitResult.append(unitList[i])
                typeResult.append(typeList[i])
        for i in range(len(channelResult)):
            channelListDict[channelResult[i]] = {
                'data':[],
                'type':typeResult[i],
                'unit':unitResult[i],
                'time':[],
                'maxValue':0,
                'minValue':0,
            }
        return channelListDict, typeResult, unitResult

    def addNewChannel(self, channelListStr, unitList, typeList,**kwargs):
        channelListDict = self.channelListDict
        # 判断是否有新通道
        channelListStr = channelListStr
        channelList = list(channelListDict.keys())
        channelListNew = []
        channelListNew, typeResult, unitResult = self.transString(channelListStr, unitList, typeList, channelListDict)
        channelListNew = list(channelListNew.keys())
        # 对比新旧通道的差异，并且保持原来的顺序
        channelListAdd = []
        for i in range(len(channelListNew)):
            if channelListNew[i] not in channelList:
                channelListAdd.append(channelListNew[i])
        waitConverte = kwargs.get('waitConverted', None)
        if waitConverte:
            currRangeMin = kwargs.get('currRangeMin')
            currRangeMax = kwargs.get('currRangeMax')
            mesureRangeMin = kwargs.get('mesureRangeMin')
            mesureRangeMax = kwargs.get('mesureRangeMax')
        for i in range(len(channelListAdd)):
            transPara = None
            if waitConverte:
                transPara = {
                    'currRangeMin':currRangeMin,
                    'currRangeMax':currRangeMax,
                    'mesureRangeMin':mesureRangeMin,
                    'mesureRangeMax':mesureRangeMax
                }
            channelListDict[channelListAdd[i]] = {
                'data':[],
                'type':typeResult[i],
                'unit':unitResult[i],
                'time':[],
                'maxValue':0,
                'minValue':0,
                'transPara':transPara,
            }
        channelListDict = dict(sorted(channelListDict.items(), key=lambda x: x[0], reverse=False))
        sep = ','
        self.channelListStr = sep.join(str(k) for k in channelListDict.keys())
        self.channelList = list(channelListDict.keys())
        self.channelListDict = channelListDict
        _unitsList=[]
        _physicalType=[]
        for k,v in channelListDict.items():
            _unitsList.extend([v['unit']])
            _physicalType.extend([v['type']])
        self.unitsList = _unitsList
        self.physicalType = _physicalType
        logger.info(
            '\n 写入通道配置:' +\
            '通道: ' + str(self.channelListStr) + '\n' +\
            '单位: ' + str(self.unitsList) + '\n' +\
            '类型: ' + str(self.physicalType) + '\n'
        )
    # def addNewChannel(self, channelListStr, unitList, typeList, **kwargs):
    #     return super().addNewChannel(channelListStr, unitList, typeList, **kwargs)


class ContributorList():
    contributorList = [
            {
                'name':'Tobin',
                'email':'',
                'github':'',
                'avatar':r'app\resource\avatar\db.png',
            },
            {
                'name':'XX',
                'email':'',
                'github':'',
                'avatar':r'app\resource\avatar\db.png',
            },
            {
                'name':'XX',
                'email':'',
                'github':'',
                'avatar':r'app\resource\avatar\db.png',
            }
        ]
