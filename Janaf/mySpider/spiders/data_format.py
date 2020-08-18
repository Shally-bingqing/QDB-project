import csv
from .tools import  write_excel_xls as w2xl

#考虑直接在遍历的时候通过查找table字眼的时候删除
def isHead(x,key):
    #是否查找table
    if x.find(key)!=-1:
        #如果找不到
        return False
        pass#if
    else:
        return True
        pass#else
    pass#def

#改行为单个元素，计算表达页码字符串的长度，时候是否<3即可
def isTail(x,length):
    #得到字符串的长度
    if len(x)<=length:
        #如果小于长度
        return False
        pass #if
    else:
        return True
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

# 处理每一行的数据，由于每一行都是科学计数，
# 但是是有符号数，也就是每个数前面要么带-号，
# 要么不带，所以从科学计数法入手，
# 科学计数E之后都会有3位，第一位代表符号，
# 后面两位代表计数值，每一行最后一个字符是行号，
# 可以选择遗弃或者放到最后 
def separation(x,char):
    #存放结果
    y=[]
    #先去掉分离最后一个 
    tail=x[-1]
    #从原来的
    x=x[:-2]
    #先去掉所有的空格
    x.replace(" ","")
    while(len(x)>0):
        #通过找来分割
        if x.index(char)!=-1:
            #E的后面3位代表一个数的结束
            y.append(x[:x.index(char)+3])
            #去除已经加入结果的值
            x=x[x.index(char)+3:]
            pass #if
        pass #while
    return y.append(tail)
    pass#def


#要处理的文件路径
path='./source_data/'
#文件名
name='NASA_poly70-72.csv'
def read(path,name):
    filepath = path + name
    #以只读的方式打开文件
    with open(filepath,'r') as f:
        #将文件转为csv的reader对象
        reader = csv.reader(f)
        #将数据转为2维列表
        data = list(reader)
        #存储格式化后的数据
        output=[]
        #获取每一行
        for no, i in enumerate(data):
            #输出每一行
            print(no,":",i)
            
            #ToDo 这里实现每一行的处理逻辑
            

            pass#for no
        pass#with
    #将结果写入文件
    save_path = './dataset/output_test.xls'
    sheet_name="NASA_test"
    return w2xl(save_path,sheet_name,output)