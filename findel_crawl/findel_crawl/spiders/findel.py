# -*- coding: utf-8 -*-
import scrapy
from findel_crawl.items import findelItem


class FindelSpider(scrapy.Spider):
    name = 'findel'
    allowed_domains = ['www.findel-international.com/products']
    start_urls = ['http://www.findel-international.com/products/']

    def parse(self, response):
        findels = response.css('.product-pod')
        for findel in findels:
            item = findelItem()
            item['title'] = findel.css('.product-pod__title::text').extract_first()
            item['code'] = findel.css('.product-pod__code::text').extract_first()
            item['price'] = findel.css('.product-pod__price::text').extract_first()
            item['img'] = findel.css('.product-pod__image::attr("src")').extract_first()
            item['link'] = findel.css('a.product-pod__link::attr(href)').extract_first()
            #item['nature'] = findel.css('.product-pod__price::text').extract_first()
            #item['delivery'] = findel.css('.product-pod__price::text').extract_first()
            #item['describe'] = findel.css('.product-pod__price::text').extract_first()
            #item['classsify'] = findel.css('.product-pod__price::text').extract_first()
            yield item
            
        if response.css('.pager__link page-link page-link--next::attr(data-page)').extract_first() is not None: # 如果有下一页标签,没有表示结束了
            page = response.css('.pager__link page-link page-link--next::attr(data-page)').extract_first()
            if page<3: #测试两页试试
                next = "?p=" + page
                url = response.urljoin(next)
                yield scrapy.Request(url=url,callback=self.parse)

           
 
    
