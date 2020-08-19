import csv
from tools import  write_excel_xls as w2xl

#考虑直接在遍历的时候通过查找table字眼的时候删除
def isHead(x,key):
    #是否查找table
    if x.find(key)!=-1:
        #如果找到了
        return True
        pass#if
    else:
        return False
        pass#else
    pass#def

#改行为单个元素，计算表达页码字符串的长度，时候是否<3即可
def isTail(x,length):
    #得到字符串的长度
    if len(x)<=length:
        #如果小于长度
        return True
        pass #if
    else:
        return False
        pass#else
    pass#else

#将所有列拼接为一列 
def connect(list):
    y=""
    for i in list:
        y+=i
        pass#for
    return [y]
    pass#def connext

#查找一行中是否同时出现（与），来判断元素信息行
def isTitle(x,key):
    y=0
    for i in key:
        #找到的话
        if x.find(i)!=-1:
            #找到+1
            y=y+1
            pass#if
        pass#for
    #如果不是全部找到
    if y<len(key):
        #则说明不是标题
        return False
        pass#if
    else:
        return True
        pass#else
    pass#def 

'''
 处理每一行的数据，由于每一行都是科学计数，
 但是是有符号数，也就是每个数前面要么带-号，
 要么不带，所以从科学计数法入手，
 科学计数E之后都会有3位，第一位代表符号，
 后面两位代表计数值，每一行最后一个字符是行号，
 可以选择遗弃或者放到最后 
'''
def separation(x,char):
    #存放结果
    y=[]
    #先去掉分离最后一个 
    tail=x[-1]
    #从原来的
    x=x[:-2]
    #先去掉所有的空格
    x=x.replace(" ","")
    #却掉所有的换行符号
    x=x.replace("\t","")
    while(len(x)>3):
        #通过找来分割
        print("x:",x)
        if x.index(char)!=-1:
            #E的后面3位代表一个数的结束
            y.append([x[:x.index(char)+4]])
            print("y:",y)
            #去除已经加入结果的值
            x=x[x.index(char)+4:]
            pass #if
        else:
            if len(x)<3:
                break
        pass #while
    y.append([tail])
    return y
    pass#def

def read(path,name):
    #记录文件页码和处理个数
    flag=0
    record=[]
    page=[]
    filepath = path + name
    #以只读的方式打开文件
    with open(filepath,'r') as f:
        #将文件转为csv的reader对象
        reader = csv.reader(f)
        #将数据转为2维列表
        data = list(reader)
        #存储格式化后的数据
        y=[]
        #获取每一行
        for no, i in enumerate(data):
            #输出每一行
            print(no,":",i)
            
            #ToDo 这里实现每一行的处理逻辑
            #首先将所有的每行都并成一列
            i=connect(i)
            #其次判断是不是标题
            if isHead(i[0],"THERMODYNAMIC"):
                #如果是将起始标记写入
                if flag==0:
                    record.append(no)
                    pass
                else:
                    record[flag]=no
                    pass
                continue
            #判断是否为子标题
            if isHead(i[0],"CETPC"):
                if flag==0:
                    record.append(no)
                    pass
                else:
                    record[flag]=no
                    pass
                continue
            #判断是否为页码
            if isTail(i[0],3):
                #记录页码
                page.append(i[0])
                #将当前页码坐标减去最近的标题坐标便为处理数量
                record[flag]=no-record[flag]
                #之后进行下一页的处理记录
                flag=flag+1
                continue
            mark=["(",")"]
            #判断是否为元素的标题
            if isTitle(i[0],mark):
                y.append(i)
                continue
            else:
                #排除所有其他可能，不是元素标题则为数据
                y.append(separation(i[0],"E"))
            pass#for no
        pass#with
    #将结果写入文件
    #!!!!!!!这里改为自己的目录
    save_path = 'mySpider/mySpider/spiders/dataset/output_test.xls'
    sheet_name="NASA_test"
    return w2xl(save_path,sheet_name,y)

if __name__ =="__main__":
    # #test isTail
    # x="TABLE II. - THERMODYNAMIC DATA COEFFICIENTS"
    # key="TABLE"
    # print(isHead(x,key))
    # x = "10"
    # length=3
    # print(isTail(x,length))
   #l=["ZrN(L)	J 6/61ZR	l.N	1.	0.	0.C	3225.000	5000.000	106","23074	1"]
   #print(connect(l))
   #l=['ZrN(L)\tJ 6/61ZR\tl.N\t1.\t0.\t0.C\t3225.000\t5000.000\t10623074\t1']
   #key=["(",")"]
   #print(isTitle(l[0],key))
   #x=["0.00000000E+00 0.00000000E+00-7.45375000E+02-1.17208122E+01 0.00000000E+00	4"]
    #x=["-1.284274B0E+05-5.45922640E+01 1.05676750E+01	0.00000000E+00	0.00000000E-f00	3"]
    #x=["0.00000000E+00 0.00000000E+00-1.28427450E+05-5.45922640E+01 0.00000000E-(-00	4"]
    #char="E"
    #print(x[0].index(char))
    #print(separation(x[0],char))
    ##combine test
    #要处理的文件路径,
    #!!!!!!!这里改为自己的目录
    path='mySpider/mySpider/spiders/source_data/'
    #文件名
    name='NASA_poly73.csv'
    read(path,name)
