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
    pageindex = 0
    while True:
        datapage = Store.FileHistoryRepository().getspage(pageindex=pageindex)
        for item in datapage["list"]:
            # print(item)
            tags = item.remark2.split(" ")
            for tag in tags:
                if tag:
                    Store.TagRepository().addorupdate(tag)
            successcount = successcount + 1
            progressbar.move("成功%s;" % (successcount))
        if len(datapage["list"]) == 0:
            break
        pageindex = pageindex + 1
    print("共需处理%s;成功%s;" % (total, successcount))
