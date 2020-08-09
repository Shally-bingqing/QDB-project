import scrapy

class ApiSpider(scrapy.Spider):
    name = 'cccb'
    allowed_domains = ['https://cccbdb.nist.gov/']
    start_urls = ['https://cccbdb.nist.gov/pollistx.asp',]
    
    def parse(self, response):
        #the name set 
        name = []
        #the value set 
        alpha = []
        # the Molecule index for every line
        name_no = 1
        #the alpha index for every line
        alpha_no = 5
        #get all the tables in target url
        tables = response.xpath("//table")
        #the target table is no.2
        for number, table in enumerate(tables):
            if number ==1:
                # get all the rows in target table
                rows = table.xpath(".//tr")
                # deal with every row in rows we get , which contains all data
                for no,row in enumerate(rows):
                    #the 1st row is ths
                    if no==1:
                        continue
                    # get all element data in every row
                    everys = row.xpath(".//td")
                    #deal with every element data in  one row
                    for i, every in enumerate(everys):
                        if i==name_no-1:
                            #get the name
                            name.append(every.xpath("string(.)").extract()[0])
                            continue
                        if i==alpha_no-1:
                            #get the alpha value
                            alpha.append(every.xpath("string(.)").extract()[0])
                            break
                        pass#forevery
                    pass#for everys
                pass#for rows
            pass#for tables
        dic=dict(zip(name,alpha))
        return dic
        
#scrapy crawl cccb -o ./dataset/cccb.csv

#Todo
#存在Molecule相同的元素，但是不同的alpha
#如果使用了dic每次会保留最后一个，因为是集合