import scrapy

#from mySpider.items import Element

class janaf(scrapy.Spider):

    element = ["C", "H", "Ac", "Ag", "Al", "Am", "Ar", "As", "At","Au", 
               "B", "Ba", "Be", "Bi", "Bk", "Br", "Ca", "Cd", "Ce", "Cf", "Cl",
               "Cm", "Co", "Cr", "Cs", "Cu", "D", "Dy", "Er", "Es", "Eu", "F", "Fe",
               "Fm", "Fr", "Ga", "Gd", "Ge", "He", "Hf", "Hg", "Ho", "I", "In", "Ir",
               "K", "Kr", "La", "Li", "Lr", "Lu", "Md", "Mg", "Mn", "Mo", "N", "Na",
               "Nb", "Nd", "Ne", "Ni", "No", "Np", "O", "Os", "P", "Pa", "Pb", "Pd",
               "Pm", "Po", "Pr", "Pt", "Pu", "Ra", "Rb", "Re", "Rh", "Rn", "Ru", "S",
               "Sb", "Sc", "Se", "Si", "Sm", "Sn", "Sr", "T", "Ta", "Tb", "Tc", "Te",
               "Th", "Ti", "Tl", "Tm", "U", "V", "W", "Xe", "Y", "Yb", "Zn", "Zr"]

    # #test code ->>
    # element=["Al"]
    # #<<-
    name = "janaf"
    allow_domains = ['https://janaf.nist.gov/']
    prefix = "https://janaf.nist.gov/tables/"
    endfix = ".html"
    conn = "-"
    #爬取的连接集合
    start_urls=[]
    #构造每个元素的所有连接
    for every_element  in element:
        # #test code ->>
        # for i in range(1,10):
        # #<<-
        #构造多个序号连接,，没有000号网页
        for i in range(1,999):
            no=str(i)
            while(len(no)<3):
                no="0"+no
                pass#while
            #前缀+元素名称+-+三位字符的序号+后缀
            #在此处验证是否存在
            tmp=prefix+every_element+conn+no+endfix
            #加入列表
            start_urls.append(tmp)
            pass#for i
        pass#for every
   

    dic ={}
    def parse(self,response):
        #存储值数据
        name=[]
        line=[]
        #获取内容标题
        #/html/body/p
        p = response.xpath("//p/text()").extract()
        # print("********************")
        # print(p)
        # print("********************")
        #判断是否可爬
        if p[0].find("not found")!=-1:
            #说明不可爬
            return
        else:
            dic={}
            #声明目标值
            target=["298.15"]
            #获取所有的行
            rows = response.xpath("//tr")
            #遍历所有的行
            for no,row in enumerate(rows):
                #得到每一行的每个数据格
                everys = row.xpath(".//td")
                #设置捕捉标示
                flag=False
                #每行的缓存
                tmp=[]
                #处理每个数据
                for i,every in enumerate(everys):
                    # print("+++++++++++++++++++")
                    # print(i)
                    # print("+++++++++++++++++++")
                    #得到每个数据格的值
                    each = every.xpath(".//text()").extract()
                    # print("++++++++++++")
                    # if each!=[]:
                        # print(each[0])
                    # print("++++++++++++")
                    #得到每行的缓存
                    tmp.append(each)
                    #对一个元素进行目标值判断
                    pass# everys
                #对每一行做处理
                #首先判断取出第一行的最后一个元素名字
                if no==0:
                    #print("name:",tmp[-1])
                    #name.append(tmp[-1][0])
                    name=''.join(tmp[-1])
                    #print("name:",name)
                    continue
                #print(tmp)
                if tmp!=[] and tmp[0]==target :
                    line=[i for item in tmp for i in item]
                    #line.append(tmp)
                    #print("line:",line)
                    dic[name]=line
                    break
                pass#for
        return dic

# scrapy crawl janaf -o ./dataset/janaf.csv