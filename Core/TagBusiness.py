"""配置信息"""
import os
import shutil
import Tool
import Store
import Store.Entity
from AppConfig import AppConfig

def detail():
    """设置详情"""
    data = Store.FileHistoryRepository().getspage(pageindex=0)
    total = data["total"]
    progressbar = Tool.ProgressBar(total=total)
    successcount = 0
    while True:
        pageindex = 0        
        datapage = Store.FileHistoryRepository().getspage(pageindex=pageindex)
        for item in datapage["list"]:
            tags = item.remrk2.split(" ")
            for tag in tags:
                Store.TagRepository().addorupdate(tag)
            successcount = successcount + 1
            progressbar.move("成功%s;" % (successcount))
        if len(datapage["list"]) == 0:
            break
        pageindex = pageindex + 1
    print("共需处理%s;成功%s;" % (total, successcount))
