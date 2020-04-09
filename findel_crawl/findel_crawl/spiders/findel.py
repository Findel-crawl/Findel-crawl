# -*- coding: utf-8 -*-
import scrapy
from findel_crawl.items import findelItem


class FindelSpider(scrapy.Spider):
    name = 'findel'
    allowed_domains = ['www.findel-international.com']
    start_urls = ['http://www.findel-international.com/products/']

    def parse_detail(self, response):
        #调用进入详情页获得详细信息
        item = response.meta['item']
        if response.css('.product-details__delivery-notice::text').extract_first() is not None:
            item['delivery'] = response.css('.product-details__delivery-notice::text').extract_first()
        if response.css('#facetGroup-433').extract_first() is not None:
            item['nature'] = response.css('#facetGroup-433 option::text').extract()
        item['describe'] = response.css('.product-description__content div p::text').extract()  
        yield item 
        

    def parse(self, response):
        findels = response.css('.product-pod')
        for findel in findels:
            item = findelItem()
            item['title'] = findel.css('.product-pod__title::text').extract_first()
            item['price'] = findel.css('.product-pod__price::text').extract_first()
            item['img'] = findel.css('.product-pod__image::attr("src")').extract_first()
            item['link'] = 'https://www.findel-international.com'+findel.css('a.product-pod__link::attr(href)').extract_first()
            item['code'] = item['link'][item['link'].rindex('/')+1:]
            item['classsify'] = item['link'][37:-len(item['code'])]
            yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse_detail) #此处进入详情页调用parse_detail
            
            
            
        if response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first() is not None: # 如果有下一页标签,没有表示结束了
            page = response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first()     
                next = "?p=" + page
                print(page)
                url = "https://www.findel-international.com/products" + next
                yield scrapy.Request(url=url,callback=self.parse,dont_filter=False)

           
 
    
