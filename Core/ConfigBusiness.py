"""配置信息"""
import os
import json
import Tool.FileHelper
#from Core.Model.ConfigModel import ConfigModel
from Core.Model import ConfigModel
from AppConfig import AppConfig
from Store.ConfigRepository import ConfigRepository

def configsfrompaths(configpaths):
    """来自文件新增配置信息"""
    configs = []
    for configpath in configpaths:
        configmodel = ConfigModel(configpath)
        configs.append(configmodel.config())
        print("检查路径:%s" % (configpath))
    return configs

def addpath(configpath=''):
    """新增配置信息:传入目录路径则遍历，文件路径直接使用"""
    rootpath = AppConfig().DownConfigPath
    configpath = os.path.join(rootpath, configpath)
    try:
        configpaths = Tool.FileHelper.filesfrompath(configpath)
        configs = configsfrompaths(configpaths)
        addconfigs = ConfigRepository().adds(configs)
        for addconfig in addconfigs:
            print("新增成功,key：%s" % (addconfig.key))
        print("新增完成")
    except Exception as err:
        print(err)
        raise

def updatepath(configpath=''):
    """修改配置信息:传入目录路径则遍历，文件路径直接使用"""
    rootpath = AppConfig().DownConfigPath
    configpath = os.path.join(rootpath, configpath)
    try:
        configpaths = Tool.FileHelper.filesfrompath(configpath)
        configs = configsfrompaths(configpaths)
        updateconfigs = ConfigRepository().updates(configs)
        for updateconfig in updateconfigs:
            print("修改成功,key：%s" % (updateconfig.key))
        print("修改完成")
    except Exception as err:
        print(err)
        raise

def deletebykey(key):
    """根据key设置删除标记"""
    deleteconfig = ConfigRepository().deletebykey(key)
    if deleteconfig:
        print("删除完成,key:%s" % (deleteconfig.key))
    else:
        print("删除错误,key:%s" % (key))


def select(select):
    """查询(不传则全查，bool根据结束标记，string根据key)"""
    configs = []
    if select == "":
        configs = ConfigRepository().gets()
    elif type(select) == bool:
        configs = ConfigRepository().getbyisend(select)
    else:
        config = ConfigRepository().getbykey(select)
        if config:
            configs.append(config)
    for config in configs:
        print(config)
