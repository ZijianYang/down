import os, time, shutil,sys
from PIL import Image

def AllToJpg(dirPath):
    paths=allfilefromdir(dirPath,[".jpg"])
    for path in paths:
        ToJpg(path)
#移动到一个新的文件夹
def AllToNewTotal(dirPath,newDir):
    paths=allfilefromdir(dirPath,[".jpg"])
    newDir=os.path.join(dirPath, newDir)
    if not os.path.exists(newDir):
        os.mkdir(newDir)  
    for path in paths:
        first=os.path.split(os.path.split(path)[0])[1]
        second=os.path.split(path)[1]
        newpath=os.path.join(newDir,first+second)
        if not os.path.exists(newpath):
            shutil.copyfile(path,newpath)
def allfilefromdir(dirpath, includes=None):
    """遍历文件夹下所有文件，所有层"""
    filelist = os.listdir(dirpath) #列出文件夹下所有的目录与文件
    result = []
    for i in range(0, len(filelist)):
        path = os.path.join(dirpath, filelist[i])
        if os.path.isfile(path):
            if includes:
                ext = os.path.splitext(os.path.split(path)[1])[1]
                if ext in includes:
                    result.append(path)
            else:
                result.append(path)
        else:
            result = result + allfilefromdir(path, includes)
    return result

def ToJpg(path):
    if os.path.exists(path):
        image = Image.open(path)
        image_format = image.format
        if image_format == 'WEBP':
            image.save(path, 'JPEG')
            image_format = 'JPEG' 
# ToJpg("008.jpg")
# AllToJpg(os.path.join(sys.path[0],"SouMiao"))
# path=os.path.join(sys.path[0],"008.jpg") 
# print(os.path.split(os.path.split(path)[0])[1])      
# print(os.path.split(path)[1])
# print(os.path.splitext(os.path.split(path)[1])[1])
AllToNewTotal(os.path.join(sys.path[0],"SouMiao\\1427"),"Total")