# -*- coding: utf-8 -*
import csv
import random
import time
import re
import requests
import urllib.request
from contextlib import closing
import os
import sys
import subprocess
import shutil



#-----------------------------------------------------网页下载------------------------------------------------
def fonline():
    url = r'http://10.75.1.151:50070/webhdfs/v1/complaint/mblog/?op=LISTSTATUS'
    print('\n----------------------------------选择文件-----------------------------------\n')

    res = urllib.request.urlopen(url)
    html = res.read().decode('utf-8')
    files=re.findall(u'"pathSuffix":"(.*?)"',html)
    print('已更新文件：')
    if len(files)>7:
        print(str(1)+'.\t'+'...')
        for i in range(6):
            print(str(i+2)+'.\t'+files[len(files)-6+i])
    else:       
        for i in range(len(files)):
            print(str(i+1)+'.\t'+files[i])
    return files



def flocal():
    path=u'/Users/litian/PROGRAMMING/python/色情举报/数据/'
    try:
        myfiles=os.listdir(path)
    except:
        try:
            os.mkdir('数据')
            print('创建本地文件夹: /数据')
        except:
            print('本地文件夹路径: /数据')
        path='数据/'
        myfiles=os.listdir(path)

    if len(myfiles)==0:
        print('\n本地文件夹为空！')
    else:
        print('\n已处理至：'+max([f for f in myfiles if 'cplt' not in f]))
    return myfiles,path


def choose(files, myfiles,path):
    choice=input('\n请选择要下载的文件：')
    day='2000-01-01'

    if len(files)>7:
        if choice!='1':
            day=files[len(files)-8+int(choice)]
            while 'cplt' in day:
                choice=input('\n请选择正确格式的文件: ')
                day=files[len(files)-8+int(choice)]
            if choice=='1':
                print('显示所有文件：')
                for i in range(len(files)):
                    print(str(i+1)+'.\t'+files[i])
                choice=input('\n请选择要下载的文件：')
                day=files[int(choice)-1]
                while 'cplt' in day:
                    choice=input('\n请选择正确格式的文件: ')
                    day=files[int(choice)-1]    
        elif choice=='1':#展开
            print('显示所有文件：')
            for i in range(len(files)):
                print(str(i+1)+'.\t'+files[i])
            choice=input('\n请选择要下载的文件：')
            day=files[int(choice)-1]
            while 'cplt' in day:
                choice=input('\n请选择正确格式的文件: ')
                day=files[int(choice)-1]
    else:
        day=files[int(choice)-1]
        while 'cplt' in day:
            choice=input('\n请选择正确格式的文件: ')
            day=files[int(choice)-1]

    if day in myfiles:
        op=input('文件夹已存在！确定要覆盖吗(y/n)：')
        if op!='y':
            sys.exit()
        else:
            shutil.rmtree(path+day)
    return day




def geturl(day):
    print('开始下载文件: '+day)
    url = r'http://10.75.1.151:50070/webhdfs/v1/complaint/mblog/'+day+'?op=LISTSTATUS'
    res = urllib.request.urlopen(url)
    html = res.read().decode('utf-8')
    files=re.findall(u'"pathSuffix":"(.*?)"',html)
    originame=files[1]
    print('获取源文件名称：'+originame+'\n')
    url = 'http://10.75.1.151:50075/webhdfs/v1/complaint/mblog/'+day+'/'+originame+'?op=OPEN&namenoderpcaddress=0.0.0.0:9000&offset=0' 
    return url,originame

#下载进度
def downloading(url,inname):
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024 # 单次请求最大值
        content_size = int(response.headers['content-length'])
        with open(inname, "wb") as file:
            mycount=1
            old=0
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                #progress.refresh(count=len(data))
                mycount = mycount+len(data)
                if int(mycount/content_size*100)>old:
                    out='下载进度：'+str(int(mycount/content_size*100))+'%\t\t'+str(round(mycount/chunk_size,2))+' KB/ '+str(round(content_size/chunk_size,2))+' KB'
                    print('\r',out.ljust(40),end='')
                    old=int(mycount/content_size*100)
            print('下载成功！')




def excel(inname,outname,count,num):
    if count>num and count<2*num:
        n=count-num
        list=[i for i in range(count)]
        rmlist=random.sample(list,n)
        with open(inname,'r') as rf:
            lines=rf.readline()
            with open(outname,'w') as f:
                f.write(u'\ufeff')
                w=csv.writer(f)
                i=0
                start=time.clock()
              
                while lines:
                    if i%1000==0:
                        end=time.clock()
                        t1=end-start
                        left=(count-i)*t1/(i+1)
                        out='处理至\t'+str(i)+',\t已用时\t'+str(round(t1,2))+'s'+',\t预计剩余\t'+str(round(left,2))+'s'
                        print('\r',out.ljust(40),end='',flush=True)

                    if i not in rmlist:
                        line=lines.split('\t')  #
                        w.writerow(line)
                    i=i+1
                    lines=rf.readline()


    elif count>=2*num:

        list=[i for i in range(count)]
        savelist=random.sample(list,num)

        with open(inname,'r') as rf:
            lines=rf.readline()

            with open(outname,'w') as f:
                f.write(u'\ufeff')
                w=csv.writer(f)
                i=0
                start=time.clock()
                while lines:
                    if i%1000==0:
                        end=time.clock()
                        t1=end-start
                        left=(count-i)*t1/(i+1)
                        out='处理至\t'+str(i)+',\t已用时\t'+str(round(t1,2))+'s'+',\t预计剩余\t'+str(round(left,2))+'s'
                        print('\r',out.ljust(40),end='',flush=True)

                    if i in savelist:
                        line=lines.split('\t')  
                        w.writerow(line)  
                    i=i+1  
                    lines=rf.readline()

    else:
         with open(inname,'r') as rf:
            lines=rf.readline()
            with open(outname,'w') as f:
                f.write(u'\ufeff')
                w=csv.writer(f)
                i=0
                start=time.clock()
                #for line in lines:
                while lines:
                    if i%1000==0:
                        end=time.clock()
                        t1=end-start
                        left=(count-i)*t1/(i+1)
                        out='处理至\t'+str(i)+',\t已用时\t'+str(round(t1,2))+'s'+',\t预计剩余\t'+str(round(left,2))+'s'
                        print('\r',out.ljust(40),end='',flush=True)

                    line=lines.split('\t')  
                    w.writerow(line)  
                    i=i+1
                    lines=rf.readline()
    print('\n\n随机抽样+分隔+BOM  处理完成!\n')

    

if __name__ == '__main__':
    files=fonline()
    myfiles,path0=flocal()
    day=choose(files,myfiles,path0)
    path=path0+day
    os.mkdir(path)
    print('\n创建文件夹：'+path)

    print('\n----------------------------------下载文件----------------------------------\n')
    url,originame=geturl(day)


    inname=path+'/'+originame
    downloading(url,inname)#将url的文件下载至本地inname文件


    print('\n----------------------------------处理文件----------------------------------\n')
    f=open(inname,'r')
    line1=f.readline()
    date=line1.split('\t')[2].replace('\n','')#显示数据中的日期，作为检查
    count=len(f.readlines())+1#前面readline()使其减少了一行
    f.close()
    print('文件\t'+inname+'\n共\t'+str(count)+'条数据!'+'\n数据日期\t'+str(date))
    outname=path+'/Blogporn'+date.replace('-','')+u'.csv'
    print('\n输出路径：'+outname+'\n')


    num=25000
    excel(inname,outname,count,num) #原数据，输出文件，原数据总量，抽样数量


    print('请检查...正在打开文件......')
    subprocess.call(["open", outname])
    time.sleep(10)
