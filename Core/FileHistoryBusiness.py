"""配置信息"""
import os
import shutil
import Tool
import Store
import Store.Entity
from AppConfig import AppConfig

def add(dirpath, includes, ishandleurl=False):
    """处理历史文件"""
    filepaths = Tool.FileHelper.allfilefromdir(dirpath, includes)
    adddatacount = 0 #插入数据数量
    filecopycount = 0 #复制文件数量
    totalcount = len(filepaths)
    i = 1
    for filepath in filepaths:
        print("文件总数:%s;复制文件数量:%s;数据:%s;当前%s" % (totalcount, filecopycount, adddatacount, i))
        i = i + 1
        filehistory = handlefilepath(filepath)
        if not os.path.exists(filehistory.filepath):# 不存在则复制
            shutil.copy(filepath, filehistory.filepath)
            filecopycount = filecopycount + 1
            print("从：%s到：%s" % (filepath, filehistory.filepath))
        if Store.FileHistoryRepository().add(filehistory):
            if ishandleurl:
                handleurl(filepath, filehistory.filepath)
            adddatacount = adddatacount + 1
    print("全部完成，文件总数:%s;复制文件数量:%s;数据:%s" % (totalcount, filecopycount, adddatacount))

def handlefilepath(filepath):
    """处理路径为histotyfile"""
    historypath = AppConfig().HistoryPath
    filehistory = Store.Entity.FileHistory(filepath)
    filename = filehistory.md5 + os.path.splitext(os.path.split(filepath)[1])[1]
    newfiledir = os.path.join(historypath, filehistory.md5[0:2])
    Tool.FileHelper.noexitcreatdir(newfiledir)
    newfilepath = os.path.join(newfiledir, filename)
    filehistory.filepath = newfilepath
    return filehistory

def handleurl(filepath, newfilepath):
    """处理url数据和文件"""
    Store.UrlRepository().setnewfilepath(filepath, newfilepath)
    print("修改成功", end="")
    os.remove(filepath)
    print("删除成功")
