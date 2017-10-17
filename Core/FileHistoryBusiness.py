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
    adddatacount = 0 #插入数据数量
    filecopycount = 0 #复制文件数量
    for filepath in filepaths:
        filehistory = Store.Entity.FileHistory(filepath)
        filename = filehistory.md5 + "." +os.path.split(filepath)[1].split(".")[1]
        newfiledir = os.path.join(historypath, filehistory.md5[0:2])
        Tool.FileHelper.noexitcreatdir(newfiledir)
        newfilepath = os.path.join(newfiledir, filename)
        if not os.path.exists(newfilepath):# 不存在则复制
            shutil.copy(filepath, newfilepath)
            filecopycount = filecopycount + 1
            print("从：%s到：%s" % (filepath, newfilepath))
        filehistory.filepath = newfilepath
        if Store.FileHistoryRepository().add(filehistory):
            adddatacount = adddatacount + 1
    print("全部完成，文件总数:%s;复制文件数量:%s;数据:%s" % (len(filepaths), filecopycount, adddatacount))
