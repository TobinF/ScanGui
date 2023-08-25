from math import log
import pyvisa
import time
import numpy as np
from loguru import logger

class Agilent34970A():

    def __init__(self) -> None:

        self.scanInterval:int = 10
        self.channelListDict:dict = {}               # 用于保存通道数据
        self.channelListStr:str = str()
        self.physicalType:list = []
        self.channelList:list = []
        self.unitsList:list = []
        self.connectState:bool = False
        self.session = None
        self.rm = pyvisa.ResourceManager()
        ...

    @property
    def getComList(self):
        return self.rm.list_resources()
    
    @property
    def getInstId(self) -> str:
        return self.inst.query("*idn?")
    @property
    def getInstSession(self):
        return self.inst.session
    @property
    def closeInstrument(self):
        self.inst.close()
        self.connectState = False
        ...

    def connectInstrument(self,com:str, baude_rate: str ,timeout:str, **kargs)->str:
        id = '未获取到id'
        try:
            self.inst = self.rm.open_resource(com)
            self.session = self.getInstSession
            self.inst.read_termination = '\n'    # 读取终止符
            self.inst.write_termination = '\n'   # 写入终止符
            self.inst.baude_rate = int(baude_rate)       #波特率
            self.inst.timeout = int(timeout)           #超时时间
            self.inst.write("FORM:READ:TIME ON")
            self.connectState = True            # 连接状态           
            if 'scanInterval' in kargs.keys():   
                self.scanInterval = kargs['scanInterval']   #扫描间隔
            if 'reset' in kargs.keys() and kargs['reset']:
                self.inst.write("*rst")                     # 重置仪器
            if 'cls' in kargs.keys() and kargs['cls']:
                self.inst.write("*cls")                     # 清除仪器状态
            id = self.getInstId             # 获取仪器id
            return id                
        except Exception as e:
            if self.connectState:
                self.inst.write("*cls")                 # 清除仪器状态
            return str(e)

    def testInst(self,**kargs):
        # if self.getInstSession is None:

        if 'timeout' in kargs.keys():
            self.inst.timeout = kargs['timeout']
        try:
            tst = self.inst.query("*tst?")
            if '0' in  tst:
                return 'passed'
            else:
                return 'failed'
        except Exception as e:
            self.inst.write("*cls")
            return e
    
    def confTemp(self, 
                 probeType: int = 1,
                 sensorType: str = 'K',
                 channelListStr: str = '',
                 temperatureUnit: str = 'C'):
        '''
        配置温度通道
        ---
        ProbeType[int]: 1: 热电偶[default] 2: 热敏电阻 3: 热电阻 4: 四线热电阻\n
        SensorType[str]: 热电偶: 'B','E','J','K'[default],'N','R','S','T','U'\n
                         热敏电阻: '2252', '5000', '10000'\n
                         热电阻/4线热电阻: '85', '91'\n
        Channel_list[str]: 通道列表, 以","分隔，连续通道以":"分隔，例如: '101,102' '101:110'\n
        TemperatureUnit[str]: 温度单位, 'C'[default],'F','K'\n

        '''
        logger.info(
            '\n 配置温度通道:' +\
            '通道: ' + str(channelListStr) + '\n' +\
            '单位: ' + str(temperatureUnit) + '\n' +\
            '类型: ' + str(probeType) + '\n' +\
            '传感器类型: ' + str(sensorType) + '\n'
        )
        # 1-热电偶 2-热敏电阻 3-热电阻 4-4线热电阻
        if probeType == 1:
            probeType = 'TCouple'
        elif probeType == 2:
            probeType = 'THERmistor' 
        elif probeType == 3:
            probeType = 'RTD'
        elif probeType == 4:
            probeType = 'FRTD'
        else:
            return 'ProbeType Error'
        self.channelListStr = self.channelListStr+','+channelListStr
        _unitsList = [temperatureUnit]*len(channelListStr.split(','))
        _typeList = [probeType]*len(channelListStr.split(','))
        self.addNewChannel(channelListStr, _unitsList, _typeList)
        # 配置通道
        self.inst.write("CONF:TEMP %s,%s,(@%s)"%(probeType ,sensorType ,channelListStr))
        self.inst.write("UNIT:TEMP %s,(@%s)"%(temperatureUnit ,channelListStr))
        time.sleep(0.1)
        self.getConfig


    def confCurr(self,currType:str='DC',currRange:str='AUTO',channelListStr:str=''):
        '''
        配置电流通道
        ---
        CurrType[str]: 电流类型, 'DC'[default],'AC'\n
        CurrRange[str]: 电流量程, 'AUTO', '10mA', '100mA', '1A'\n
        channelList[str]: 通道列表, 以","分隔，连续通道以":"分隔，例如: '101,102' '101:110'\n
        '''
        self.channelListStr = self.channelListStr+','+channelListStr
        _unitsList = ['mA']*len(channelListStr.split(','))
        _typeList = [currType]*len(channelListStr.split(','))
        self.addNewChannel(channelListStr, _unitsList, _typeList)
        # 配置通道
        if currRange != 'AUTO':
            currRange = str(float(currRange)/1000)
            self.inst.write("CONF:CURR:%s %s,0.001,(@%s)" %(currType ,currRange, channelListStr))
        else:
            self.inst.write("CONF:CURR:%s %s,(@%s)" %(currType ,currRange, channelListStr))
        self.getConfig
        # CONFigure:CURRent:%s [{%s}[,{%s}],] (@%s) %(currType ,currRange, 0.00001,channelListStr)
        # 1A=1000mA
        ...
    def confCalulated(self, channelListStr:str='',currRange:str='', expression:str=''):
        self.inst.write("CONF:CALC:SCAL:FORM %s,(@%s)" %(expression, channelListStr))
        # inst = 0
        ...

    def scan(self, channelListStr):
        self.inst.write("ROUT:SCAN (@%s)"%channelListStr)
        time.sleep(0.5)
        ...

    def scanAll(self):
        # self.startScanTime = self.startScanTime
        # self.transString(self.channelListStr,self.unitsList,self.physicalType)
        # print("ROUT:SCAN (@%s)"%str(self.channelList))
        self.inst.write("ROUT:SCAN (@%s)"%self.channelListStr)
        # time.sleep(self.ScanInterval)
        ...

    @property
    def readResult(self):
        data = self.inst.query_ascii_values('READ?',container=np.array)
        # data2 = self.inst.query('READ?')
        # print('data:----------------------------\n',data2)
        scanTime = self.startTime
        return data, scanTime
    
    # @property
    def parseResult(self):
        self.scanAll()
        data, scanTime = self.readResult
        channelListResults = np.array(data).tolist()
        
        for i in range(len(self.channelList)):
            self.channelListDict[self.channelList[i]]['data'].append(channelListResults[i])
            self.channelListDict[self.channelList[i]]['time'].append(scanTime if self.channelListDict[self.channelList[i]]['time'] == [] else scanTime - self.channelListDict[self.channelList[i]]['time'][0])
            self.channelListDict[self.channelList[i]]['maxValue'] = max(self.channelListDict[self.channelList[i]]['data'])
            self.channelListDict[self.channelList[i]]['minValue'] = min(self.channelListDict[self.channelList[i]]['data'])
        logger.info(
            '\n 读取数据:' +\
            '通道: ' + str(self.channelList) + '\n' +\
            '数据: ' + str(channelListResults) + '\n' +\
            '时间: ' + str(scanTime) + '\n'
        )
        return self.channelListDict
    
    def test(self):
        time.sleep(2)
        return {"test":1}

    # @property
    # def breakScan(self):
    #     self.inst.write("ROUT:SCAN:BRK")
    #     ...
    @property
    def getConfig(self):
        channelConfig = self.inst.query("CONF? (@%s)"%self.channelListStr)
        logger.info(
            '当前配置:' +\
            str(channelConfig) + '\n'
        )
        return channelConfig

    # @property
    # def getBeginScanTime(self):
    #     self.startTime = self.inst.query("SYSTem:TIME:SCAN?").split('.')[0]

    @property
    def getBeginStartScanTime(self):
        # This query returns the time at the start of the scan. 
        # The string returned has the form yyyy,mm,dd,hh,mm,ss.sss:
        # Typical Response: 2009,07,26,22,03,10.314
        startTime = self.inst.query("SYSTem:TIME:SCAN?").split('.')[0]
        # 转化为时间戳
        self.startTime = time.mktime(time.strptime(startTime, "%Y,%m,%d,%H,%M,%S"))
        # return startTime

    def transString(self, channelListStr, unitList, typeList ,channelListDict):
        
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

    def addNewChannel(self, channelListStr, unitList, typeList):
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
        # channelListAdd.sort()
        # print(channelListAdd)
        for i in range(len(channelListAdd)):
            channelListDict[channelListAdd[i]] = {
                'data':[],
                'type':typeResult[i],
                'unit':unitResult[i],
                'time':[],
                'maxValue':0,
                'minValue':0,
            }
        channelListDict = dict(sorted(channelListDict.items(), key=lambda x: x[0], reverse=False))
        sep = ','
        self.channelListStr = sep.join(str(k) for k in channelListDict.keys())
        self.channelList = list(channelListDict.keys())
        self.channelListDict = channelListDict
        # self.unitsList, self.physicalType = [channelListDict.get(key).get('unit') for key in channelListDict.keys()]
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
        # return channelListDict

    def saveData(self):
        with open('scanData.json','w') as f:
            f.write(str(self.channelListDict))
        ...
    # @property
    # def transString(self):
    #     s = self.channelList
    #     # 定义一个空列表，用于存放最终结果
    #     result = []
    #     # 用 , 或 : 分割字符串
    #     parts = s.split(",")
    #     # 如果存在空字符串，则删除
    #     if "" in parts:
    #         parts.remove("")
    #     # print(parts)
    #     # 遍历分割后的列表
    #     for part in reversed(parts):
    #         # 如果包含 : ，则表示是连续的数字
    #         if ":" in part:
    #             # 用 : 分割数字，并转换为整数
    #             start, end = map(int, part.split(r"\:", part))
    #             # 用 range() 函数生成连续的数字，并添加到结果列表中
    #             result.extend(range(start, end + 1))
    #         else:
    #             # 否则，直接把数字转换为整数，并添加到结果列表中
    #             result.append(int(part))
    #     # 对结果列表进行排序
    #     result.sort()
    #     # 打印结果列表
    #     self.channelList = str(result).replace('[','').replace(']','')
    #     ...
    # @staticmethod
    # def transString(self):
    #     channelListStr = self.channelListStr
    #     unitList = self.unitsList
    #     typeList = self.physicalType
    #     # 定义一个空列表，用于存放最终结果
    #     channelResult = []
    #     unitResult = []
    #     typeResult = []
    #     # 用 , 或 : 分割字符串,
    #     channelParts = channelListStr.split(",")
    #     # 如果存在空字符串，则删除
    #     if "" in channelParts:
    #         channelParts.remove("")
    #         # unitParts.remove("")
    #     partsLength = len(channelParts)
    #     # 遍历分割后的列表
    #     for i in range(partsLength):
    #         # 如果包含 : ，则表示是连续的数字
    #         if ":" in channelParts[i]:
    #             # 用 : 分割数字，并转换为整数
    #             start, end = channelParts[i].split(":")
    #             # 用 range() 函数生成连续的数字，并添加到结果列表中
    #             channelResult.extend(range(int(start), int(end) + 1))
    #             unitResult.extend([unitList[i]]*len(range(int(start), int(end) + 1)))
    #             typeResult.extend([typeList[i]]*len(range(int(start), int(end) + 1)))
    #         else:
    #             # 否则，添加到结果列表中
    #             channelResult.append(int(channelParts[i]))
    #             unitResult.append(unitList[i])
    #             typeResult.append(typeList[i])
    #     # 对结果列表进行排序
    #     # result.sort()
    #     # 打印结果列表
    #     # return str(channelResult).replace('[','').replace(']','')
    #     # return channelResult, unitResult, typeResult
    #     # self.channelList
    #     for i in range(len(channelResult)):
    #         self.channelListDict[channelResult[i]] = {
    #             'data':[],
    #             'unit':unitResult[i],
    #             'time':[],
    #             'type':typeResult[i],
    #             'maxValue':0,
    #             'minValue':0,
    #         }
    #     self.channelListDict = dict(sorted(self.channelListDict.items(), key=lambda x: x[0], reverse=False))
    #     sep = ','
    #     self.channelListStr = sep.join(str(k) for k in self.channelListDict.keys())
    #     self.channelList = list(self.channelListDict.keys())

    # def transString(self):
    #     '''
    #     字符串形如: 308,305:307,302
    #     对应的单位:  K,    C,    F
    #     转化为: [308,305,306,307,302]
    #     单位:   [K,  C,  C,  C,  F]
    #     添加新的通道时，拼接到原通道字符串，如添加101,102:104，对应单位为: V, A
    #     拼接为: 308,305,306,307,302,101,102,103,104
    #     同时拼接单位，K,  C,  C,  C,  F,   V, A, A, A
    #     如果原通道字符串为空，则直接拼接
    #     如果新通道已在原通道字符串中，则不拼接，但是要更新单位
    #     如原通道字符串为: 308,305:307,302
    #     新通道为: 306，单位为V
    #     则不拼接，但是更新单位为: K,  C,  V,  C,  F
    #     '''
        
    #     ...


    # def testTran(self):
    #     self.transString(self.channelList,self.unitsList,self.physicalType)
    #     print(self.channelListDict)
    #     print(self.channelListDict.keys())


# if __name__ == 'main':
#     AG = Agilent34970A()
#     print(AG.getComList())
#     id = AG.connectInstrument(AG.getComList()[-1],9600,20000,reset=True,cls=True,ScanInterval=10)
#     print(id)
#     print(AG.testInst())

