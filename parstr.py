
class ParStr:

    def __init__(self):
        self.channelListDict = {}

    def transString(self, channelListStr, unitList, typeList ,channelListDict):
        
        channelListStr = channelListStr
        # channelListDict =self.channelListDict
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
                # 'data':[],
                'unit':unitResult[i],
                # 'time':[],
                'type':typeResult[i],
                # 'maxValue':0,
                # 'minValue':0,
            }
        # # channelListDict = dict(sorted(channelListDict.items(), key=lambda x: x[0], reverse=False))
        # sep = ','
        # channelListStr = sep.join(str(k) for k in channelListDict.keys())
        # channelList = list(channelListDict.keys())
        # print(channelListStr+'\n')
        # print(channelList+'\n')

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
        print(channelListAdd)
        for i in range(len(channelListAdd)):
            channelListDict[channelListAdd[i]] = {
                # 'data':[],
                'unit':unitResult[i],
                # 'time':[],
                'type':typeResult[i],
                # 'maxValue':0,
                # 'minValue':0,
            }
        channelListDict = dict(sorted(channelListDict.items(), key=lambda x: x[0], reverse=False))
        sep = ','
        channelListStr = sep.join(str(k) for k in channelListDict.keys())
        channelList = list(channelListDict.keys())
        print('channelListStr: ', channelListStr)
        print( 'channelList: ', channelList)
        return channelListDict
        ...


STR = ParStr()

# # ch0 = '305,302:304,301'
# # un0 = ['C','K','F']
# # ty0 = ['rtd','4rtd','DC']
# channelListDict = {}
# # channelListDict = transString(ch0, un0, ty0, channelListDict)
# # print(channelListDict)

# ch1 = '305,306'
# un1 = ['V','K']
# ty1 = ['4rtd','DC']
# channelListDict = addNewChannel(ch1, un1, ty1, channelListDict)
# print(channelListDict)

ch0 = '305,302:304,301'
un0 = ['C','K','F']
ty0 = ['rtd','4rtd','DC']
# 301-F-DC,302-K-4rtd,303-K-4rtd,304-K-4rtd,305-C-rtd
channelListDict = STR.addNewChannel(ch0, un0, ty0)
print(channelListDict)

ch1 = '305,306'
un1 = ['V','K']
ty1 = ['4rtd','DC']
channelListDict = STR.addNewChannel(ch1, un1, ty1)
print(channelListDict)






# class ParStr:

#     def __init__(self):
#         self.channelListDict = {}

#     def transString(self, channelListStr, unitList, typeList ,):
        
#         channelListStr = channelListStr
#         # channelListDict =self.channelListDict
#         # 定义一个空列表，用于存放最终结果
#         channelResult = []
#         unitResult = []
#         typeResult = []
#         # 用 , 或 : 分割字符串,
#         channelParts = channelListStr.split(",")
#         # 如果存在空字符串，则删除
#         if "" in channelParts:
#             channelParts.remove("")
#             # unitParts.remove("")
#         partsLength = len(channelParts)
#         # 遍历分割后的列表
#         for i in range(partsLength):
#             # 如果包含 : ，则表示是连续的数字
#             if ":" in channelParts[i]:
#                 # 用 : 分割数字，并转换为整数
#                 start, end = channelParts[i].split(":")
#                 # 用 range() 函数生成连续的数字，并添加到结果列表中
#                 channelResult.extend(range(int(start), int(end) + 1))
#                 unitResult.extend([unitList[i]]*len(range(int(start), int(end) + 1)))
#                 typeResult.extend([typeList[i]]*len(range(int(start), int(end) + 1)))
#             else:
#                 # 否则，添加到结果列表中
#                 channelResult.append(int(channelParts[i]))
#                 unitResult.append(unitList[i])
#                 typeResult.append(typeList[i])

#         return channelResult, unitResult, typeResult
#         # for i in range(len(channelResult)):
#         #     channelListDict[channelResult[i]] = {
#         #         # 'data':[],
#         #         'unit':unitResult[i],
#         #         # 'time':[],
#         #         'type':typeResult[i],
#         #         # 'maxValue':0,
#         #         # 'minValue':0,
#         #     }
#         # channelListDict = dict(sorted(channelListDict.items(), key=lambda x: x[0], reverse=False))
#         # sep = ','
#         # channelListStr = sep.join(str(k) for k in channelListDict.keys())
#         # channelList = list(channelListDict.keys())
#         # print(channelListStr+'\n')
#         # print(channelList+'\n')

#         # return channelListDict


#     def addNewChannel(self, channelListStr, unitList, typeList):
#         channelListDict = self.channelListDict
#         # 判断是否有新通道
#         channelListStr = channelListStr
#         channelList = list(channelListDict.keys())
#         channelListNew = []
#         channelListNew, unitList, typeList = self.transString(channelListStr, unitList, typeList)
#         # channelListNew = list(channelListNew.keys())
#         channelListAdd = list(set(channelListNew).difference(set(channelList)))
#         channelListAdd.sort()
#         print(channelListAdd)
#         for i in range(len(channelListAdd)):
#             channelListDict[channelListAdd[i]] = {
#                 # 'data':[],
#                 'unit':unitList[i],
#                 # 'time':[],
#                 'type':typeList[i],
#                 # 'maxValue':0,
#                 # 'minValue':0,
#             }
#         channelListDict = dict(sorted(channelListDict.items(), key=lambda x: x[0], reverse=False))
#         sep = ','
#         channelListStr = sep.join(str(k) for k in channelListDict.keys())
#         channelList = list(channelListDict.keys())
#         # return channelListDict
#         ...


# STR = ParStr()

# ch0 = '305,302:304,301'
# un0 = ['C','K','F']
# ty0 = ['rtd','4rtd','DC']
# STR.addNewChannel(ch0, un0, ty0)
# print(STR.channelListDict)

# ch1 = '305,306'
# un1 = ['V','K']
# ty1 = ['4rtd','DC']
# STR.addNewChannel(ch1, un1, ty1)
# print(STR.channelListDict)