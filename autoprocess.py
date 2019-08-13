import sys
import csv
import random
import time

print('\n')
#fname=input('输入文件：')
fname=str(sys.argv[1])
f=open(fname,'r')
line1=f.readline()
date=line1.split('\t')[2].replace('\n','')
count=len(f.readlines())+1#前面readline()使其减少了一行
f.close()
print('文件\t'+fname+'\n共\t'+str(count)+'条数据!'+'\n数据日期\t'+str(date))
#outname=input('输出文件：')
outname=u'/Users/litian/PROGRAMMING/f-porndata/Blogporn'+date.replace('-','')+u'.csv'
print('输出路径：'+outname)



#主要代码
if count>20000 and count<40000:
    n=count-20000
    #注意生成的随机数不能是重复的，否则失败
    #rmlist=[random.randint(0,count-1) for i in range(n)]
    list=[i for i in range(count)]
    rmlist=random.sample(list,n)
    #rlist=rmlist
    
    with open(fname,'r') as rf:
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
    
    with open(fname,'r') as rf:
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
     with open(fname,'r') as rf:
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
print('\n随机抽样+分隔+BOM  处理完成!\n')