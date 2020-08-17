import csv
#Todo continue
path='./source_data/'
#name='NASA_poly70-72.csv'
def read(path,name):
    filepath = path+name
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
            #处理文件头
            print(no,":",i)
            pass#for no
        pass#with
    return output