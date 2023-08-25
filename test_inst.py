import time
from app.components.agilent34970a import Agilent34970A

inst = Agilent34970A()

# instLst = inst.getComList
# print(instLst)
id = inst.connectInstrument(
    'ASRL6::INSTR',
    baude_rate='9600',
    data_bits='8',
    timeout=20000,
    scanInterval=3,
)
print(id)


# 配置测温通道
# inst.inst.close()
inst.confTemp(
    probeType=4,
    sensorType='85',
    temperatureUnit='C',
    channelListStr='305:307',
)
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
print(inst.channelListDict)
while True:
    # print(inst.channelList)
    # inst.inst.write("ROUT:SCAN (@%s)"%inst.channelList)
    # time.sleep(1)
    # res = inst.readResult
    # print(res)
    # time.sleep(inst.scanInterval - 1)
    inst.parseResult()
    print(inst.channelListDict)
    time.sleep(inst.scanInterval - 1)

# inst.testTran()