# -*- coding: utf-8 -*-
import scrapy
from findel_crawl.items import findelItem


class FindelSpider(scrapy.Spider):
    name = 'findel'
    allowed_domains = ['www.findel-international.com']
    #start_urls = ['https://www.findel-international.com/products?p=1&show=100/']

    def start_requests(self):
        first_url = 'https://www.findel-international.com'
        yield scrapy.Request(first_url,callback=self.parse_col)

    def parse_col(self,response):
        some_urls = response.css('ul.site-menu.site-menu--top.site-menu--level-1 a.site-menu__link.site-menu__link--level-1::attr(href) ').extract()
        print(some_urls)        
        for url in some_urls:
            real_url = 'https://www.findel-international.com' + url + '?p=1&show=100'
            yield scrapy.Request(real_url,callback=self.parse2)  
            

    def parse2(self, response):
        findels = response.css('.product-pod')
        for findel in findels:
            item = findelItem()
            item['title'] = findel.css('.product-pod__title::text').extract_first()
            item['link'] = 'https://www.findel-international.com'+findel.css('a.product-pod__link::attr(href)').extract_first()
            item['code'] = item['link'][item['link'].rindex('/')+1:].upper()
            item['classify'] = item['link'][45:item['link'][item['link'][item['link'][45:].index('/')+46:].index('/')+item['link'][45:].index('/')+47:].index('/')+item['link'][item['link'][45:].index('/')+46:].index('/')+item['link'][45:].index('/')+47]
            #存在title中含有/字符的情况，这里只从URL中提取前三级分类
            item['age_range'] = '无年龄范围'
            yield item
                    
        if response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first() is not None: # 如果有下一页标签,没有表示结束了
            page2 = response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first()     
            next2 = response.request.url[0:response.request.url.rindex('?')+3] + page2 + '&show=100'
            print(next2)
            yield scrapy.Request(next2,callback=self.parse2)


    #以上部分可以直接爬取所有的商品的信息包括（title，link，code，classsify），但是没有年龄范围
    #接下来利用mongo的更新功能，将年龄范围属性更新上去


   

            

