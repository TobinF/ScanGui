import os
import configparser
from ..components.info_bar import CreateInfoBar

class TemperatureConfig():
    probe_type: str
    channel_list: str
    sensor_type: str
    temperature_Unit: str


class CurrentConfig():
    curr_type: str
    curr_range: str
    channel_list: str


class VotageConfig():
    ...


class CalculatedConfig():
    curr_type: str
    curr_range: str
    channel_list: str
    measure_type: str
    measure_unit: str
    curr_range_min: float
    curr_range_max: float
    measure_range_min: float
    measure_range_max: float

class ConfigImport():
    configParseList = ['Temperature', 'Current', 'Votage', 'Calculated']
    TemperatureConf = TemperatureConfig()
    CurrentConf = CurrentConfig()
    VotageConf = VotageConfig()
    CalculatedConf = CalculatedConfig()

    def __init__(self,fileName,parent=None):
        self.fileName = fileName
        self.parent = parent
        self.load_config()

    def load_config(self) -> None:
        if not os.path.exists(self.fileName):
            CreateInfoBar.createErrorInfoBar(self.parent, '错误', '配置文件不存在,请检查app/config文件夹下的instConfig.ini文件')
        try:
            conf = configparser.RawConfigParser()
            conf.read(self.fileName,encoding="utf-8")
            sections = conf.sections()
            for section in sections:
                items = conf.items(section)
                for item in items:
                    if section in self.configParseList:
                        parse = eval('self.{}Conf'.format(section))
                        setattr(parse, item[0], eval(item[1]))
            # return("配置文件加载成功")
            CreateInfoBar.createSuccessInfoBar(self.parent, '提示', '配置文件加载成功')
        except Exception as e:
            # return f"配置文件加载失败{e}"
            CreateInfoBar.createErrorInfoBar(self.parent, '错误', f'配置文件加载失败{e}')

if __name__ == "__main__":
    conf = ConfigImport(r'instConfig.ini')
    print(conf.TemperatureConf.channel_list)
