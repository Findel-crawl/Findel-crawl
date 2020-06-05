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
            real_url = 'https://www.findel-international.com' + url
            yield scrapy.Request(real_url,callback=self.parse_agerange)  #本来想用meta传递url参数，但是meta参数不可以变化，只好后面使用response.request.url
            
    def parse(self, response):
        findels = response.css('.product-pod')
        for findel in findels:
            item = findelItem()
            item['title'] = findel.css('.product-pod__title::text').extract_first()
            item['link'] = 'https://www.findel-international.com'+findel.css('a.product-pod__link::attr(href)').extract_first()
            item['code'] = item['link'][item['link'].rindex('/')+1:].upper()
            item['classsify'] = item['link'][45:-(len(item['code'])+len(item['title'])+2)]
            yield item
                    
        if response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first() is not None: # 如果有下一页标签,没有表示结束了
            page = response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first()     
            next = response.request.url + "?p=" + page + "&show=100"
            url =next
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=False)

    def parse_agerange(self, response);
        Age_ranges = response.css('div.filter-panel__list js-filter-panel-list a.filter-variant::attr(href)').extract()
        print(Age_ranges)
        for age_range in Age_ranges:
            age_url = 'https://www.findel-international.com' + url
            yield scrapy.Request(age_url,callback=self.parse)
        
