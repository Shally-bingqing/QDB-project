import scrapy
from .tools import  write_excel_xls as w2xl
from .tools import write_excel_xls_append as a2xl

class janaf(scrapy.Spider):
    #all the element index
    element = ["C", "H", "Ac", "Ag", "Al", "Am", "Ar", "As", "At","Au", 
               "B", "Ba", "Be", "Bi", "Bk", "Br", "Ca", "Cd", "Ce", "Cf", "Cl",
               "Cm", "Co", "Cr", "Cs", "Cu", "D", "Dy", "Er", "Es", "Eu", "F", "Fe",
               "Fm", "Fr", "Ga", "Gd", "Ge", "He", "Hf", "Hg", "Ho", "I", "In", "Ir",
               "K", "Kr", "La", "Li", "Lr", "Lu", "Md", "Mg", "Mn", "Mo", "N", "Na",
               "Nb", "Nd", "Ne", "Ni", "No", "Np", "O", "Os", "P", "Pa", "Pb", "Pd",
               "Pm", "Po", "Pr", "Pt", "Pu", "Ra", "Rb", "Re", "Rh", "Rn", "Ru", "S",
               "Sb", "Sc", "Se", "Si", "Sm", "Sn", "Sr", "T", "Ta", "Tb", "Tc", "Te",
               "Th", "Ti", "Tl", "Tm", "U", "V", "W", "Xe", "Y", "Yb", "Zn", "Zr"]
    # store the attribute title
    # the data must be 2 demensions ,which would be stored
    title=[["Name","Formula","T/K","Cp°","S°"," -[G°-H°(Tr)]/T","H-H°(Tr)", "fH°","fG°","log Kf"]]
    # file path
    path="./dataset/janaf.xls"
    # name of spider & xls sheet
    name="janaf"
    # create & wtrite title into file
    w2xl(path,name,title)
    # the target domains allowed
    allow_domains = ['https://janaf.nist.gov/']
    # urls' common prefix
    prefix = "https://janaf.nist.gov/tables/"
    # urls' common endfix
    endfix = ".html"
    # urls' common connect char
    conn = "-"
    #爬取的连接集合
    start_urls=[]
    #构造每个元素的所有连接
    for individual  in element:
        #构造多个序号连接,，没有000号网页
        for i in range(1,999):
            # transfer int in2 string
            no=str(i)
            # fix string's length
            while(len(no)<3):
                #append "0" in the front of the string
                no="0"+no
                pass#while
            #前缀+元素名称+-+三位字符的序号+后缀
            #在此处验证是否存在
            tmp=prefix+individual+conn+no+endfix
            #加入列表
            start_urls.append(tmp)
            pass#for i
        pass#for every

    def parse(self,response):
        #获取内容标题
        #/html/body/p
        p = response.xpath("//p/text()").extract()
        #判断是否可爬
        if p[0].find("not found")!=-1:
            #若是有not found字眼，说明不可爬
            return
        else:
            #待写入的存值列表
            value=[]
            #声明目标值
            target=["298.15"]
            #获取所有的行
            rows = response.xpath("//tr")
            #遍历所有的行
            for no,row in enumerate(rows):
                #得到每一行的每个数据格
                everys = row.xpath(".//td")
                #每行的缓存    
                tmp=[]
                #处理每个数据
                for i,every in enumerate(everys):
                    #得到每个数据格的值
                    each = every.xpath(".//text()").extract()
                    #得到每行的缓存
                    tmp.append(each)
                    #对一个元素进行目标值判断
                    pass# everys
                #对每一行做处理
                #首先判断取出第一行的最后一个元素名字
                #首先进行非空校验
                if tmp!=[]:
                    if no==0:
                        #将元素的名字拼接在一起
                        Name="".join(tmp[0])
                        value.append(Name)
                        #将元素的符号拼接在一起
                        Formula=''.join(tmp[-1])
                        value.append(Formula)
                        continue
                    # 非空校验之后再判断是否符合值
                    if tmp[0]==target :
                        #填充为单值列表的方式
                        line=[i for item in tmp for i in item]
                        for i in line:
                            value.append(i)
                            pass#for
                        value=[value]
                        break
                    pass#if tmp
                pass#for
            print("->",value,"<-")
            #store the value
            path="./dataset/janaf.xls"
            #append every loop
            a2xl(path,value)

# scrapy crawl janaf -o ./dataset/janaf.csv