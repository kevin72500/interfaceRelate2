# coding:utf-8
import configparser
import itertools
import queue


class iniReader():
    def __init__(self, filePath, encoding='utf-8'):
        self.cf = configparser.ConfigParser()
        self.cf.read(filePath, encoding=encoding)

    def getSections(self):
        return self.cf.sections()

    def getOptions(self, sectId):
        return self.cf.options(sectId)

    def getItem(self, section, option):
        return self.cf.get(section, option)


def production(*args):
    # 对列表进行笛卡儿积，并按照一个列表返回
    all = []
    for i in itertools.product(*args):
        all.append(i)
    return all


class UrlObj():
    __slots__=['method','host','url','name','desc','retCode','retContent']
    def __init__(self,method="",host="",url="",name="",desc="",retCode="",retContent=""):
        self.method=method
        self.host=host
        self.url=url
        self.name=name
        self.desc=desc
        self.retCode=retCode
        self.retContent=retContent



def getParams(iniFilePath):
    cf = iniReader(iniFilePath)
    alldata = queue.deque()
    host=""
    method=""
    url=""
    name=""
    desc=""
    for section in cf.getSections():
        #区域数据
        sectionData=[]
        for option in cf.getOptions(section):
            #获取主机信息
            if option.lower()=='host':
                host=cf.getItem(str(section),str(option))
            #获取方法头
            elif option.lower()=='method':
                method=cf.getItem(str(section),str(option))
            #获取名字
            elif option.lower()=='name':
                name=cf.getItem(str(section),str(option))
            #获取描述
            elif option.lower()=='desc':
                desc=cf.getItem(str(section),str(option))
            elif option.lower()=='url':
                url=cf.getItem(str(section),str(option))
            #其他数据判断
            else:
                data = cf.getItem(str(section), str(option))
                #判断是否是参数
                if data.startswith('(') and len(data) > 2:
                    paraName = option
                    paraValue = data
                    paraList = []
                    #拼接参数url参数部分
                    for one in eval(paraValue):
                        paraList.append(paraName + "=" + str(one))
                    # print(paraList)
                    #添加到列表
                    sectionData.append(paraList)
        # print(sectionData)
        urls=production(*sectionData)
        for one in urls:
            tempUrl=UrlObj(method,host,host+url+"?"+"&".join(one),name,desc)
            alldata.append(tempUrl)
    # alldata.append(production(*sectionData))R
    # print(alldata)

    return alldata






if __name__ == '__main__':
    res=getParams("interfaceDef.ini")
    # for sec in res:
    #         print(sec.desc,sec.name,sec.method,sec.host,sec.url)
    print(len(res))