"""down"""
import getopt
import sys
import urllib.request
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image# pip install pillow

class DownHandle(object):
    """下载配置"""   
    def __init__(self,comicid):
        """从文件获取dict"""
        self.comicid =comicid
        self.rootUrl = "https://nyaso.com/comic/"
        self.rootPath = os.path.join(sys.path[0],"SouMiao")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #对应的chromedriver的放置目录
        self.driver = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)

    def Down(self,words,page):
        """开始下载"""
        print("漫画"+str(self.comicid)+";开始话数:"+str(words)+";开始页数:"+str(page))
        if not os.path.exists(self.rootPath):
            os.mkdir(self.rootPath)  
        self.ComicHandle(words,page)        
        self.driver.close()  
        self.driver.quit()  
        print("Success")


    def ComicHandle(self,starWords,page):
        comicUrl=self.rootUrl+self.comicid+".html"
        comicDir=os.path.join(self.rootPath, self.comicid)
        print("漫画地址:"+str(comicUrl)+";漫画路径"+str(comicDir)+";")
        comicHtml=self.Downfile(comicUrl,comicDir,"Index.html",True)
        self.WordsHandle(comicHtml.decode('utf-8'),starWords)

    def WordsHandle(self,content,starWords):
        regex='<a href="(?P<wordsUrl>\\d+\\.html)" target="new">(?P<wordsNo>\\d+)话 <span style="color:#777;font-size:13px">(?P<pageCount>\\d+)P</span></a>'
        matches = re.finditer(regex,content)
        WordsList=[]
        for match in matches:
            WordsList.append({"wordsNo":match.group("wordsNo"),"wordsUrl":match.group("wordsUrl"),"pageCount":int(match.group("pageCount"))})
        WordsList.reverse()
        WordsList=WordsList[int(starWords)-1:]
        print("共%s话"%len(WordsList))
        for words in WordsList:
            wordsDir=os.path.join(self.rootPath, self.comicid,words["wordsNo"])
            wordUrl=self.rootUrl+words["wordsUrl"]
            print(words["wordsNo"]+"话(共"+str(words["pageCount"])+"页)地址:"+wordUrl+";")
            # wordsHtml=self.Downfile(self.rootUrl+words["wordsUrl"],wordsDir,"Index.html",True) #下载每话页面
            # self.PageHtml(wordUrl,words["pageCount"],wordsDir)  #模拟浏览器获取路径
            self.DownByRecord(wordsDir,"Record.txt")
    
    def PageHtml(self,wordsUrl,count,wordsDir):
        self.driver.get(wordsUrl + "/")
        imgXPath='//*[@id="slideshow"]/span/a/img'
        nextXPath='//*[@id="nav"]/div/a[2]'
        urlList=[]
        # self.driver.save_screenshot('screen.png')
        imgElement=self.getEement(imgXPath)
        imgUrl=imgElement.get_attribute("src")
        urlList.append(imgUrl)
        # self.Downfile(imgUrl,wordsDir,imgUrl[-7:],True)
        while count>1:
            nextElement=self.driver.find_element_by_xpath(nextXPath)
            nextElement.click()
            imgElement=self.getEement(imgXPath)
            imgUrl=imgElement.get_attribute("src")
            urlList.append(imgUrl)
            # self.Downfile(imgUrl,wordsDir,imgUrl[-7:],True)
            count=count-1   
        self.WriteRecord(urlList,os.path.join(wordsDir,"Record.txt"))

    def Downfile(self,url,dir,name="",isSave=False):
        """下载文件"""
        if not os.path.exists(dir):
            os.mkdir(dir)     
        if name!="":
            filePath=os.path.join(dir, name)
            if os.path.exists(filePath):
                with open(filePath, "rb") as filestream:
                    return filestream.read()   
            else:    
                print(url)
                headers = {"Upgrade-Insecure-Requests": "1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                requestContent= urllib.request.Request(url=url,headers=headers) 
                request = urllib.request.urlopen(requestContent,data=None,timeout=60)
                if request.getcode() == 200:
                    data = request.read()
                    if isSave:                
                        with open(filePath, 'wb') as filestream:
                            # print(filePath)
                            filestream.write(data)
                    return data
    # 写保存文件
    def WriteRecord(self,list,path):
        list=[item+'\r\n' for item in list]
        with open(path, "a") as filestream:
            filestream.writelines(list)
    # 从保存文件中下载图片
    def DownByRecord(self,dir,name):
        recordPath=os.path.join(dir,name)
        with open(recordPath, "r") as filestream:
            record=filestream.read()
        records=record.split("\n")
        records=[item for item in records if item!=""] 
        for recordUrl in records:
            # print(recordUrl[-7:])
            # print(recordUrl)            
            imgPath=os.path.join(dir,recordUrl[-7:])
            if not os.path.exists(imgPath):
                headers = {"Upgrade-Insecure-Requests": "1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                requestContent= urllib.request.Request(url=recordUrl,headers=headers)                 
                Flag=True
                while Flag:
                    try:
                        request = urllib.request.urlopen(requestContent,data=None,timeout=60)
                        data = request.read()                        
                        Flag=False
                    except:
                        time.sleep(1)
                        print("读取超时")
                
                with open(imgPath, 'wb') as filestream:
                    filestream.write(data)

    # def ConvetJpg(self,dir,name):
    #     recordPath=os.path.join(dir,name)
    #     with open(recordPath, "r") as filestream:
    #         record=filestream.read()
    #     records=record.split("\n")
    #     records=[item for item in records if item!=""] 
    #     for recordUrl in records:           
    #         imgPath=os.path.join(dir,recordUrl[-7:])
    #         if os.path.exists(imgPath):
                
    #             with open(imgPath, 'wb') as filestream:
    #                 filestream.write(data)

    # 获取页面元素，防止一次没获取到,没加载完等
    def getEement(self,xPath): 
        count=0   
        while count <= 10:
            count += 1         
            try:          
                ele=self.driver.find_element_by_xpath(xPath)
                if ele.get_attribute('src')!='':
                    return ele
                else:  
                    print(u'没有找到element')
                    continue
            except:
                print(u'没有找到element')
            time.sleep(1)

def usage():
    """用法"""
    print("SouMiaoComicDown.py usage:")
    print("-h,--help:print help message")
    print("-v,--version:print script version")
    print("--content:输入执行内容（默认空）")
    print("--config:执行,:add:新增(相同key则不新增);update:更新;delete：删除;select:查询;")
    print("--execute,执行:star:开始(需要key);pardondata:仅重复数据;pardonall:文件和数据都重复;")


def version():
    """版本"""
    print("SouMiaoComicDown.py 1.0.0")


def main(argv):
    """主函数"""
    words = 1
    page=1
    try:
        opts, args = getopt.getopt(
            argv[1:], 'hvt', ['words=', 'page=', 'star='])
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
        elif opt in ('-t', '--version'):
            imgUrl="1234567890"
            print(imgUrl[-7:])
            sys.exit(0)
        elif opt in ('--words', ):
            words = arg
        elif opt in ('--page', ):
            page = arg
        elif opt in ('--star', ):
            comicid = arg
            if comicid == "":
                print("缺少参数")
            else:
                # print("1")
                DownHandle(comicid).Down(words,page)
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



        
# open(path, ‘-模式-‘,encoding=’UTF-8’) 
# 即open(路径+文件名, 读写模式, 编码)

# 在python对文件进行读写操作的时候，常常涉及到“读写模式”，整理了一下常见的几种模式，如下：

# 读写模式：
# r ：只读 
# r+ : 读写 
# w ： 新建（会对原有文件进行覆盖） 
# a ： 追加 
# b ： 二进制文件

# 常用的模式有：
# “a” 以“追加”模式打开， (从 EOF 开始, 必要时创建新文件) 
# “a+” 以”读写”模式打开 
# “ab” 以”二进制 追加”模式打开 
# “ab+” 以”二进制 读写”模式打开

# “w” 以”写”的方式打开 
# “w+” 以“读写”模式打开 
# “wb” 以“二进制 写”模式打开 
# “wb+” 以“二进制 读写”模式打开

# “r+” 以”读写”模式打开 
# “rb” 以”二进制 读”模式打开 
# “rb+” 以”二进制 读写”模式打开

# rU 或 Ua 以”读”方式打开, 同时提供通用换行符支持 (PEP 278)

# 需注意：
# 1、使用“w”模式。文件若存在，首先要清空，然后重新创建 
# 2、使用“a”模式。把所有要写入文件的数据都追加到文件的末尾，即使你使用了seek（）指向文件的其他地方，如果文件不存在，将自动被创建。

# 3、f.read([size]) ：size未指定则返回整个文件，如果文件大小>2倍内存则有问题。f.read()读到文件尾时返回”“(空字串) 
# 4、file.readline() 返回一行 
# 5、file.readline([size]) 返回包含size行的列表,size 未指定则返回全部行 
# 6、”for line in f: print line” #通过迭代器访问 
# 7、f.write(“hello\n”) #如果要写入字符串以外的数据,先将他转换为字符串. 
# 8、f.tell() 返回一个整数,表示当前文件指针的位置(就是到文件头的比特数). 
# 9、f.seek(偏移量,[起始位置]) ： 用来移动文件指针 
# 偏移量 : 单位“比特”,可正可负 
# 起始位置 : 0 -文件头, 默认值; 1 -当前位置; 2 -文件尾 
# 10、f.close() 关闭文件
# --------------------- 
# 作者：W-大泡泡 
# 来源：CSDN 
# 原文：https://blog.csdn.net/u011389474/article/details/60140311 
# 版权声明：本文为博主原创文章，转载请附上博文链接！

