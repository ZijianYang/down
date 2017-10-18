# down

初始化数据库和文件
python Console.py -i
重新初始化数据库
python Console.py -r

在默认路径查找配置文件并加入库中
python App.py --config add #新增配置
python App.py --config update #新增配置
python App.py  --config select #查询

开始
python App.py --content bd  --execute new #开始或继续
python App.py --content bd  --execute pardondata #清除数据开始

向历史文件添加
python App.py --content path --history add

*****************
进度条效果
pip install git+https://github.com/WoLpH/python-progressbar