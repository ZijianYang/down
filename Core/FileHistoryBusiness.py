"""配置信息"""
import os
import shutil
import Tool
import Store
import Store.Entity
from AppConfig import AppConfig

def handle(dirpath):
    """处理历史文件"""
    filepaths = Tool.FileHelper.allfilefromdir(dirpath)
    historypath = AppConfig().HistoryPath
    for filepath in filepaths:
        filehistory = Store.Entity.FileHistory(filepath)
        filename = os.path.split(filepath)[1]
        newfiledir = os.path.join(historypath, filehistory.md5[0:2])
        Tool.FileHelper.noexitcreatdir(newfiledir)
        newfilepath = os.path.join(newfiledir, filename)
        if not os.path.exists(newfilepath):# 不存在则复制
            shutil.copy(filepath, newfilepath)
            print("从：%s到：%s" % (filepath, newfilepath))
        filehistory.filepath = newfilepath
        Store.FileHistoryRepository().add(filehistory)
    print("全部完成")
