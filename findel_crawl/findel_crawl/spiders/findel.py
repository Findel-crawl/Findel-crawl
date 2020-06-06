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
            yield scrapy.Request(real_url,callback=self.parse_agerange)  
            

    #以上部分可以直接爬取所有的商品的信息包括（title，link，code，classsify），但是没有年龄范围
    #接下来利用mongo的更新功能，将年龄范围属性更新上去


    def parse_agerange(self, response):
        Age_ranges = response.css('div.filter-panel.filter-panel--closed[data-facet-type="Age Range"] .filter-panel__list.js-filter-panel-list a.filter-variant::attr(href)').extract()
        if Age_ranges:
            print(Age_ranges)
            for age_range in Age_ranges:
                age_url = 'https://www.findel-international.com' + age_range + "&sort=&p=1"
                yield scrapy.Request(age_url,callback=self.parse1)


    def parse1(self, response):
        findels = response.css('.product-pod')
        print(response.request.url + '****************************************')
        age = response.request.url[response.request.url.index('filter')+7:response.request.url.index('&f=')]
        for findel in findels:
            item = findelItem()
            item['title'] = findel.css('.product-pod__title::text').extract_first()
            item['link'] = 'https://www.findel-international.com'+findel.css('a.product-pod__link::attr(href)').extract_first()
            item['code'] = item['link'][item['link'].rindex('/')+1:].upper()
            item['age_range'] = age
            yield item
                    
        if response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first() is not None: # 如果有下一页标签,没有表示结束了
            page1 = response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first()     
            next1 = response.request.url[:-1] + page1
            print(next1 + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+page1)
            yield scrapy.Request(next1,callback=self.parse1)


            

