import time

import numpy as np
from app.components.agilent34970a import Agilent34970A

inst = Agilent34970A()

# instLst = inst.getComList
# print(instLst)
id = inst.connectInstrument(
    'ASRL6::INSTR',
    baude_rate='9600',
    data_bits='8',
    timeout=10000,
    scanInterval=3,
    cls = True,
    rst = True,
)
print(id)


# 配置测温通道
# inst.inst.close()
# inst.confTemp(
#     probeType=4,
#     sensorType='85',
#     temperatureUnit='C',
#     channelListStr='305:307',
# )
# inst.confTemp(
#     probeType=4,
#     sensorType='85',
#     temperatureUnit='F',
#     channelListStr='301',
# )
# # inst.transString()

# inst.confTemp(
#     probeType=1,
#     sensorType='K',
#     temperatureUnit='K',
#     channelListStr='306',
# )

# inst.confCurr(
#     currType='DC',
#     channelListStr='321,322',
#     currRange='AUTO',
# )
# inst.addNewChannel
# import time
# print(inst.channelListDict)
# while True:
#     # print(inst.channelList)
#     # inst.inst.write("ROUT:SCAN (@%s)"%inst.channelList)
#     # time.sleep(1)
#     # res = inst.readResult
#     # print(res)
#     # time.sleep(inst.scanInterval - 1)
#     inst.parseResult()
#     print(inst.channelListDict)
#     time.sleep(inst.scanInterval - 1)

# inst.testTran()
channelList = '305:308'

inst.inst.write("CONF:TEMP FRTD,85,(@%s)"%channelList)
inst.inst.write("ROUT:SCAN (@%s)"%channelList)
inst.inst.write("FORM:READ:TIME ON")
inst.inst.write("FORM:READ:TIME:TYPE ABS")
inst.inst.write("FORMat:READing:CHANnel ON")
inst.inst.write("TRIG:SOUR TIM")
print(inst.inst.query("ROUTe:CHANnel:DELay?"))

# inst.inst.write("TRIG:TIM 5")
inst.inst.write("TRIG:COUN 1")
# inst.inst.write("INIT;*OPC")

while True:
    inst.inst.write("INIT;*OPC")
    # data = inst.inst.query_ascii_values("READ?",container=np.array)
    data = inst.inst.query_ascii_values("FETC?",container=np.array)
    print(
        f'数据: {data}\n')
    result = data[::8]
    time0 = data[1::7]
    channel = data[2::6]
    print(
        f'结果: {result}\n'
        f'时间: {time0}\n')
    # print(time0)
    time.sleep(1)

# data = inst.parseResult()
# print(data)

# data = inst.parseResult()
# print(data)

# print(inst.channelListDict)