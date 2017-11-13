# -*- coding: utf-8 -*-
"""down"""
import Core
import getopt
import sys
import sqlalchemy
import os
import Tool.FileHelper
from AppConfig import AppConfig


def usage():
    """用法"""
    print("datebase.py usage:")
    print("-h,--help:print help message")
    print("-v,--version:print script version")
    print("--content:输入执行内容（默认空）")
    print("--config:执行,:add:新增(相同key则不新增);update:更新;delete：删除;select:查询;")
    print("--execute,执行:star:开始(需要key);pardondata:仅重复数据;pardonall:文件和数据都重复;")


def version():
    """版本"""
    print("App.py 1.0.0")


def main(argv):
    """主函数"""
    content = ""
    try:
        opts, args = getopt.getopt(
            argv[1:], 'hv', ['config=', 'content=', 'execute=', 'history='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif opt in ('-v', '--version'):
            version()
            sys.exit(0)
        elif opt in ('--content', ):
            content = arg
        elif opt in ('--config', ):
            if arg == "add":  # 相同key则不新增
                Core.ConfigBusiness.addpath(content)
            elif arg == "update":
                Core.ConfigBusiness.updatepath(content)
            elif arg == "delete":
                if content == "":
                    print("缺少参数")
                else:
                    Core.ConfigBusiness.deletebykey(content)
            elif arg == "select":
                Core.ConfigBusiness.select(content)
            sys.exit(0)
        elif opt in ('--execute', ):
            if content == "":
                print("缺少参数")
            elif arg == "new":  # 相同key则不新增
                if content == "all":
                    configpaths = Tool.FileHelper.filesfrompath(
                        os.path.join(AppConfig().DownConfigPath, ""))
                    configs = Core.ConfigBusiness.configsfrompaths(configpaths)
                    for item in configs:
                        Core.ProcessBusiness.new(item.key)
                else:
                    Core.ProcessBusiness.new(content)
            elif arg == "pardondata":
                Core.ProcessBusiness.clear(content)
                Core.ProcessBusiness.new(content)
            elif arg == "pardonall":
                Core.ProcessBusiness.clear(content, True)
                Core.ProcessBusiness.new(content)
            elif arg == "newpardon":
                if content == "all":
                    configpaths = Tool.FileHelper.filesfrompath(
                        os.path.join(AppConfig().DownConfigPath, ""))
                    configs = Core.ConfigBusiness.configsfrompaths(configpaths)
                    for item in configs:
                        #Core.ProcessBusiness.clearnew(item.key)
                        Core.ProcessBusiness.newpardon(item.key)
                else:
                    #Core.ProcessBusiness.clearnew(content)
                    Core.ProcessBusiness.newpardon(content)
            sys.exit(0)
        elif opt in ('--history', ):
            if arg == "detail":
                Core.FileHistoryBusiness.detail()
            else:
                if content == "":
                    print("缺少参数")
                elif arg == "add":
                    Core.FileHistoryBusiness.add(content, [".jpg", ".png"])
                elif arg == "move":
                    Core.FileHistoryBusiness.add(content, [".jpg", ".png"],
                                                 True)
            sys.exit(0)
        else:
            print("unhandled option")
            sys.exit(3)
    print("unhandled option")
    sys.exit(3)


if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("")
        print("程序被强行停止！")
