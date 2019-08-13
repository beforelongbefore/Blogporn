import csv
import random
import time
import re
import requests
import urllib.request
from contextlib import closing
import os


#-----------------------------------------------------网页下载------------------------------------------------
print('\n-----------------------------------------------选择文件----------------------------------------\n')
url = r'http://10.75.1.151:50070/webhdfs/v1/complaint/mblog/?op=LISTSTATUS'
res = urllib.request.urlopen(url)
html1 = res.read().decode('utf-8')
#print(html)
files=re.findall(u'"pathSuffix":"(.*?)"',html1)
#files
print('已更新文件：')
for i in range(len(files)):
    print(str(i+1)+'.\t'+files[i])

path=u'/Users/litian/PROGRAMMING/python/色情举报/数据/'
myfiles=os.listdir(path)
if len(myfiles)==0:
    print('\n本地文件夹为空！')
else:
    print('\n已处理至：'+max(myfiles))


choice=input('\n请选择要下载的文件：')
day=files[int(choice)-1]


os.mkdir(path+day)
path=path+day
print('\n创建文件夹：'+path)


print('\n-----------------------------------------------下载文件---------------------------------------\n')
print('开始下载文件: '+files[int(choice)-1])
url2 = r'http://10.75.1.151:50070/webhdfs/v1/complaint/mblog/'+files[int(choice)-1]+'?op=LISTSTATUS'
res = urllib.request.urlopen(url2)
html2 = res.read().decode('utf-8')
#print(html2)
files2=re.findall(u'"pathSuffix":"(.*?)"',html2)
originame=files2[1]
#origname
print('获取源文件名称：'+originame+'\n')



#print("downloading with requests")
url3 = 'http://10.75.1.151:50075/webhdfs/v1/complaint/mblog/'+files[int(choice)-1]+'/'+originame+'?op=OPEN&namenoderpcaddress=0.0.0.0:9000&offset=0' 


#下载进度

        
#从网站下载下来的源文件，即后续处理的输入文件     files[int(choice)-1]+
inname=path+'/'+originame
        
with closing(requests.get(url3, stream=True)) as response:
    chunk_size = 1024 # 单次请求最大值
    content_size = int(response.headers['content-length']) # 内容体总大小
    with open(inname, "wb") as file:
        mycount=1
        for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
            #progress.refresh(count=len(data))
            mycount = mycount+len(data)
            old=0
            if int(mycount/content_size*100)>old:
                out='下载进度：'+str(int(mycount/content_size*100))+'%\t\t'+str(round(mycount/chunk_size,2))+' KB/ '+str(round(content_size/chunk_size,2))+' KB'
                print('\r',out.ljust(40),end='',flush=True)
                old=int(mycount/content_size*100)
        print('下载成功！')




#-----------------------------------------------处理excel-----------------------------

print('\n-----------------------------------------------处理文件---------------------------------------\n')
#fname=input('输入文件：')
#fname=str(sys.argv[1])#现在全自动处理，所以也不需要输入文件这个参数了
f=open(inname,'r')
line1=f.readline()
date=line1.split('\t')[2].replace('\n','')
count=len(f.readlines())+1#前面readline()使其减少了一行
f.close()
print('文件\t'+inname+'\n共\t'+str(count)+'条数据!'+'\n数据日期\t'+str(date))
#outname=input('输出文件：')
outname=path+'/Blogporn'+date.replace('-','')+u'.csv'
print('\n输出路径：'+outname+'\n')




if count>20000 and count<40000:
    n=count-20000
    #注意生成的随机数不能是重复的，否则失败
    #rmlist=[random.randint(0,count-1) for i in range(n)]
    list=[i for i in range(count)]
    rmlist=random.sample(list,n)
    #rlist=rmlist
    
    with open(inname,'r') as rf:
        lines=rf.readline()
        #lines=csv.reader(open(fname))
        with open(outname,'w') as f:
            f.write(u'\ufeff')
            w=csv.writer(f)
            i=0
            start=time.clock()
            #for line in lines: #注意每一个line是一个list
            while lines:#注意readline()返回的不是迭代器，不能用next和for，只是当前行的str
                if i%1000==0:
                    end=time.clock()
                    t1=end-start
                    left=(count-i)*t1/(i+1)
                    out='处理至\t'+str(i)+',\t已用时\t'+str(round(t1,2))+'s'+',\t预计剩余\t'+str(round(left,2))+'s'
                    print('\r',out.ljust(40),end='',flush=True)

                if i not in rmlist:
                    #line=line.replace('\t',',')
                    #line=[line[0].replace('\t',',')]    #用了这个之后又出现乱码了
                    line=lines.split('\t')  #
                    w.writerow(line)  #这里写的时候也是一个list,通过这个list来分隔，这是关键！
                i=i+1
                lines=rf.readline()
            
            
elif count>=40000:
   
    list=[i for i in range(count)]
    savelist=random.sample(list,20000)
    
    with open(inname,'r') as rf:
        lines=rf.readline()
    
        with open(outname,'w') as f:
            f.write(u'\ufeff')
            w=csv.writer(f)
            i=0
            start=time.clock()
            #for line in lines: #注意每一个line是一个list
            while lines:
                if i%1000==0:
                    end=time.clock()
                    t1=end-start
                    left=(count-i)*t1/(i+1)
                    out='处理至\t'+str(i)+',\t已用时\t'+str(round(t1,2))+'s'+',\t预计剩余\t'+str(round(left,2))+'s'
                    print('\r',out.ljust(40),end='',flush=True)

                if i in savelist:
                    line=lines.split('\t')  
                    w.writerow(line)  #这里写的时候也是一个list,通过这个list来分隔，这是关键！
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