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

    name = "janaf"
    allow_domains = ['https://janaf.nist.gov/']
    start_urls = ["https://janaf.nist.gov/tables/Al-004.html",]
    target="298.15"
    def parse(self,response):    
        out=[]
        idea={}
        target=["298.15"]
        print("-------------------------------------------------------------")
        #获取所有的列
        lines = response.xpath("//tr")
        print(len(lines.extract()))
        i=0
        #用户记录元素名字
        name=[]
        #用于最后记录关键值
        values=[]
        #标记是否已经取到目标值
        flag=True
        #处理每一行
        for each in lines:
            every=each.xpath(".//td")
            #print(len(every.extract()))
            #首先判断是否已经得到目标值 
            if flag==True:
                #暂存每一行的处理结果
                tmp = []
                #没有得到继续处理每一行中的每个单元格
                for i in every:
                    #如果获取单元格
                    value = i.xpath("string(.)").extract()
                    #print(len(value))
                    # 值不为空
                    if value!=[""]:
                        #则暂存
                        tmp.append(i.xpath(".//text()").extract())
                        pass#if
                    pass#for
                #print("////////////////////////////////////////")
                #print(len(tmp))
                #print("////////////////////////////////////////")
                #处理获取元素名和列值
                #首先考虑获取元素名
                if name==[]:
                    #则说明是第一列
                    #最后一个为元素名
                    name=tmp[-1]
                    print("**************************")
                    print("name:",name)
                    idea["name"]=name
                    print("**************************")
                    pass#if
                else:
                    #考虑获取目标列
                    #print(tmp[0])
                    if tmp!=[]:
                        #print(type(tmp[0]))
                        if tmp[0]==target:
                            #如果是为目标列
                            values.append(tmp)
                            #以获取到则将判断条件置为不再继续
                            print("+++++++++++++++++++++")
                            print(values)
                            idea["value"]=values[0]
                            print("+++++++++++++++++++++")
                            flag=False
                            pass#if
                        pass#if
                    pass#else
                pass#if
            else:
                #已经获取到，则不再继续
                break
            pass#for
        #pass#def
        out.append(idea)
        return out
        
            
    