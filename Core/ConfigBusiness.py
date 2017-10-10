"""配置信息"""
import os
import json
from Core.Model.Config import ConfigModel
from AppConfig import AppConfig
from Store.ConfigRepository import ConfigRepository



def add(configpath=''):
    """信则配置信息:传入目录路径则遍历，文件路径直接使用"""
    rootpath = AppConfig().DownConfigPath
    configpath = os.path.join(rootpath, configpath)
    try:
        if os.path.isdir(configpath):
            adddir(configpath)
        elif os.path.isfile(configpath):
            addfile(configpath)
        else:
            print("路径不正确:%s" % (configpath))
    except Exception as err:
        print(err)
        raise

def configdictbyfile(configpath):
    """从文件获取dict"""
    print(configpath)
    with open(configpath) as f:
        configcontent = f.read()
        configdict = json.loads(configcontent)
        return configdict

def addfile(configpath):
    """来自文件信则配置信息"""
    configdict = configdictbyfile(configpath)
    configmodel = ConfigModel(configdict)
    ConfigRepository().add(configmodel.config())


def adddir(configpath):
    """来自文件夹信则配置信息"""
    configs = []
    for parent, dirnames, filenames in os.walk(configpath):
        for filename in filenames:
            if filename.find(".json") > 0:
                configdict = configdictbyfile(os.path.join(parent, filename))
                configmodel = ConfigModel(configdict)
                configs.append(configmodel.config())
    ConfigRepository().adds(configs)
