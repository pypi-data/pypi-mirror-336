"""
-*- coding: utf-8 -*-
@Author : XerCis
@Time : 2024/7/2 15:00
@Function:
@Contact: 
"""


def setdevice(self, deviceList: Union[int, list]):
    gpus = GPUtil.getGPUs()
    gpuidList = [gpu.id for gpu in gpus]
    if isinstance(deviceList, int):
        deviceList = [deviceList]
    for deviceid in deviceList:
        if deviceid not in gpuidList:
            raise ValueError("设置设备ID不存在")
    self.isgpu = True
    self.deviceid = deviceList
