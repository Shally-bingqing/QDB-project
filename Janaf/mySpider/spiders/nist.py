import scrapy
from .tools import write_excel_xls_append as a2xl
from .tools import write_excel_xls as w2xl
from ..items import Nist

class NistSpider(scrapy.Spider):
    name = 'nist'
    #start_urls = ['https://webbook.nist.gov/cgi/formula/',]
    start_urls = ['https://webbook.nist.gov/cgi/formula/Te',]
    prefix="https://webbook.nist.gov"
    output=[]
    next_url=[]
    #path="./dataset/nist.xls"
    path4all="./dataset/nist_url.xls"
    #start_urls = ['https://webbook.nist.gov/cgi/formula?ID=C54038016','https://webbook.nist.gov/cgi/inchi/InChI%3D1S/No','https://webbook.nist.gov/cgi/inchi/InChI%3D1S/Ba']
    #start_urls = ['https://webbook.nist.gov/cgi/inchi?ID=C7440393&Mask=20#Ion-Energetics','https://webbook.nist.gov/cgi/inchi?ID=C10028145&Mask=20#Ion-Energetics']

    def parse(self, response):
        urls=[]
        items=response.xpath('//*[@id="main"]//ul//li')
        for no,item in enumerate(items):
            element=item.xpath("string(.)").extract_first()
            url=self.prefix+item.xpath("./a/@href").extract_first()
            if element.find("species")!=-1:
                self.next_url.append(url)
            else:
                yield scrapy.Request(url,callback=self.idea_parse)
                #self.output.append([element,url])
                #urls.append([element,url])
        #a2xl(self.path,urls)
        if self.next_url!=[]:
            print("len:",len(self.next_url))
            for i in self.next_url:
                url=i
                self.next_url.remove(url)
                yield scrapy.Request(url,callback=self.parse)

    def idea_parse(self, response):
        items=response.xpath('//*[@id="main"]//ul//li')
        for no,item in enumerate(items):
            tmp=item.xpath("./strong/text()").extract_first()
            if  tmp!=None and tmp.find("Other data")!=-1:
                eachs = item.xpath(".//li")
                for each in eachs:
                    temp=each.xpath("./a/text()").extract_first()
                    if temp!=None and temp.find("ion energetics")!=-1:
                        #output.append([prefix+each.xpath("./a/@href").extract_first()])
                        url=self.prefix+each.xpath("./a/@href").extract_first()
                        yield scrapy.Request(url,callback=self.data_parse)
    
    def data_parse(self, response):
        data=[]
        y=Nist()
        items= response.xpath("//table")
        for no,item in enumerate(items):
            tmp=item.xpath("./@aria-label").extract_first()
            if tmp !=None and tmp.find("Ionization energy")!=-1:
                eachs=item.xpath(".//tr")
                for nu,each in enumerate(eachs):
                    if nu==1:
                        everys= each.xpath(".//td")
                        tmp=[]
                        for every in everys:
                            text=every.xpath("./text()").extract_first()
                            if text!=None:
                                tmp.append(text)
                            else:
                                text=every.xpath("./a/text()").extract_first()
                                if text != None:
                                    tmp.append(text)
                                else:
                                    text= every.xpath("./em/text()").extract_first()
                                    tmp.append(text)
                        if len(tmp)>0:
                            y['IE'] = tmp[0]
                        if len(tmp)>1:
                            y['Method']=tmp[1]
                        if len(tmp)>2:
                            y['Refer']=tmp[2]
                        if len(tmp)>3:
                            y['Comment']=tmp[3]
                        if y['IE']!="":
                            y['Name']=response.xpath('//*[@id="Top"]/text()').extract_first()
                            items= response.xpath('//*[@id="main"]//ul//li')
                            for no,item in enumerate(items):
                                tmp=item.xpath("./strong/text()").extract_first()
                                if no==0:
                                    y['Formula']=item.xpath("./text()").extract_first()
                                if tmp!=None and tmp.find("CAS")!=-1:
                                    y['CAS']=item.xpath("./text()").extract_first()
                        print("y",y)
                        data.append([y])
                        #a2xl(self.path4all,data)
                        yield y
        