import re

def channelInputCheck(input:str):
    '''
    检测通道输入是否合法
    '''
    pattern = r'^[1-3][0-9][0-9]([,|:][1-3][0-9][0-9])*$'
    return re.match(pattern, input) is not None