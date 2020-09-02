import scrapy
from .tools import write_excel_xls_append as a2xl

class NistSpider(scrapy.Spider):
    name = 'nist'
    allowed_domains = ['webbook.nist.gov/']
    start_urls = ['https://webbook.nist.gov/cgi/formula/',]

    def parse(self, response):
        output=[]
        prefix="https://webbook.nist.gov"
        items=response.xpath('//*[@id="main"]//ul//li')
        for no,item in enumerate(items):
            element=item.xpath("string(.)").extract_first()
            url=prefix+item.xpath("./a/@href").extract_first()
            if element.find("species")!=-1:
                self.start_urls.append(url)
            else:
                output.append([element,url])
        path="./dataset/nist.xls"
        name="nist"
        a2xl(path,output)
        return self
    