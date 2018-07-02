import requests
from concurrent import futures
from iniReader import getParams,UrlObj
from threading import Thread
from queue import deque
import time,datetime
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def singleSender(method,url,**kwargs):
    res=None
    if method.lower()=="get":
        res=requests.get(url,**kwargs)
    elif method.lower()=='post':
        res=requests.post(url,**kwargs)
    return res.status_code,res.content


async def gevnetSender(urlObj):
    retObj=UrlObj()
    retObj.desc = urlObj.desc
    retObj.name = urlObj.name
    retObj.method = urlObj.method
    retObj.url = urlObj.url
    retObj.retCode, retObj.retContent = singleSender(urlObj.method, urlObj.url)
    return retObj


#继承多线程类
class multiThreadSender(Thread):
    #初始化
    def __init__(self,urlOjb):
        super(multiThreadSender,self).__init__()
        self.UrlObj=urlOjb
        self.ret=None
    #执行单线程，并获取返回
    def run(self):
        # for one in self.UrlObj:
        retObj=UrlObj()
        retObj.desc=self.UrlObj.desc
        retObj.name=self.UrlObj.name
        retObj.method=self.UrlObj.method
        retObj.url=self.UrlObj.url
        retObj.retCode,retObj.retContent=singleSender(self.UrlObj.method,self.UrlObj.url)
        self.ret=retObj
    #获取返回
    def getReturn(self):
        return self.ret



def multiSender(thread_num,requestList):
    workers=min(thread_num,len(requestList))
    with futures.ThreadPoolExecutor(workers) as runner:
        res=runner.map(singleSender,requestList)


#单进程，顺序执行
def singleExecute():
    starttime=datetime.datetime.now()
    items=getParams("interfaceDef.ini")
    retList=[]
    for one in items:
        one.retCode,one.retContent=singleSender(one.method,one.url)
        tempOjb=UrlObj(one.method,one.host,one.url,one.name,one.desc,one.retCode,one.retContent)
        retList.append(tempOjb)
    endtime=datetime.datetime.now()
    for one in retList:
        print(one.desc,one.retCode,one.name,one.url,one.retContent)
    print((endtime-starttime).seconds)

#多进程
def multiExcuteor():
    starttime = datetime.datetime.now()
    items=getParams("interfaceDef.ini")

    threadList=deque()
    for one in items:
        threadList.append(multiThreadSender(one))

    resultList=[]
    for t in threadList:
        t.start()
        t.join()
        resultList.append(t.getReturn())
    endtime = datetime.datetime.now()
    for one in resultList:
        print(one.desc,one.retCode,one.name,one.url,one.retContent)
    print((endtime - starttime).seconds)

def eventExecute():
    starttime = datetime.datetime.now()
    items = getParams("interfaceDef.ini")

    taskList=[]
    for one in items:
        taskList.append(asyncio.ensure_future(gevnetSender(one)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(taskList))
    endtime = datetime.datetime.now()

    for one in taskList:
        print(one.result().desc,one.result().retCode,one.result().name,one.result().url,one.result().retContent)
    print((endtime - starttime).seconds)


def eventExecute2():
    items = getParams("interfaceDef.ini")

    taskList=[]
    for one in items:
        taskList.append(asyncio.ensure_future(gevnetSender(one)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(taskList))

async def start(executor):
    await asyncio.get_event_loop().run_in_executor(executor,eventExecute2)

if __name__=='__main__':
    starttime = datetime.datetime.now()
    exec=ProcessPoolExecutor()
    asyncio.get_event_loop().run_until_complete(start(exec))
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)

# 3000个15秒
# singleExecute()
#3000个16秒
#51888个242秒
# multiExcuteor()
#3000个14秒
#51888个233秒
# eventExecute()