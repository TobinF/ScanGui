; 配置文件编写说明：
; 1.配置文件中的参数名不区分大小写，但是参数值区分大小写
; 2.配置文件包含三Temperature、Current、Voltage、Calculated四部分
; 3.变量格式为：下划线式命名
[Temperature]
; probe_type:  1:Thermocouple, 2:Thermistor, 3:RTD, 4:4-wire RTD
; sensor_type: Thermocouple: 'B','E','J','K','N','R','S','T'
;              Thermistor: '2252', '5000', '10000'
;              RTD: '85', '385'
;              FRTD: '85', '385'
; channel_list: 101,102,305:309
; temperature_Unit: 'C','F','K'
probe_type = 'FRTD'
sensor_type = '85'
channel_list = '101,102'
temperature_unit = 'C'
[Current]
; curr_type: 'DC'/ 'AC'
; curr_range: 'AUTO'/'MIN'/'MAX'
; channel_list: 121,122,305:309
curr_type = 'DC'
curr_range = 'AUtO'
channel_list = '121,122'
[Votage]
;暂未实现
[Calculated]
; curr_type: 'DC'/ 'AC'
; curr_range: 'AUTO'/'MIN'/'MAX'
; channel_list: 221,222,305:309
; measure_type: 测量类型，字符串格式
; measure_units: 测量单位，字符串格式
; curr_range_min: 电流最小值，浮点数格式
; curr_range_max: 电流最大值，浮点数格式
; mesure_range_min: 测量最小值，浮点数格式
; mesure_range_max: 测量最大值，浮点数格式
curr_type = 'DC'
curr_range = 'AUtO'
channel_list = '221'
measure_type = '流量'
measure_units = 'm3/h'
curr_range_min = 4
curr_range_max = 20
mesure_range_min = 0.4
mesure_range_max = 4
;