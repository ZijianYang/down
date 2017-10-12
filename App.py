# -*- coding: utf-8 -*-
"""down"""
from Core import *
import getopt
import sys
import sqlalchemy


def usage():
    """用法"""
    print("datebase.py usage:")
    print("-h,--help:print help message")
    print("-v,--version:print script version")
    print("--content:输入执行内容（默认空）")
    print("--config:执行,:add:新增(相同key则不新增);update:更新;delete：删除;select:查询;")
    print("--execute,执行:star:开始(不输入key则都开始，都不重复);pardondata:仅重复数据;pardonall:文件和数据都重复;")


def version():
    """版本"""
    print("App.py 1.0.0")


def main(argv):
    """主函数"""
    content = ""
    try:
        opts, args = getopt.getopt(argv[1:], 'hv', ['config=', 'content=', 'execute='])
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
            if arg == "add":# 相同key则不新增
                Core.ConfigBusiness.addpath(content)
            elif arg == "update":
                Core.ConfigBusiness.updatepath(content)
            elif arg == "delete":
                Core.ConfigBusiness.deletebykey(content)
            elif arg == "select":
                Core.ConfigBusiness.select(content)
            sys.exit(0)
        elif opt in ('--execute', ):
            if arg == "new":# 相同key则不新增
                Core.ConfigBusiness.addpath(content)
            elif arg == "pardondata":
                Core.ConfigBusiness.updatepath(content)
            elif arg == "pardonall":
                Core.ConfigBusiness.deletebykey(content)
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
