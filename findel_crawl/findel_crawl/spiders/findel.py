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
            print(real_url)
            yield scrapy.Request(real_url, meta={'real_url': real_url},callback=self.parse)  #本来想用meta传递url参数，但是meta参数不可以变化，只好后面使用response.request.url


    def parse(self, response):
        #now_url = response.meta['real_url']
        findels = response.css('.product-pod')
        for findel in findels:
            item = findelItem()
            item['title'] = findel.css('.product-pod__title::text').extract_first()
            item['price'] = findel.css('.product-pod__price::text').extract_first()
            item['img'] = [findel.css('.product-pod__image::attr("src")').extract_first()]
            img_clear = item['img'][0][0:item['img'][0].rindex('=')+1] + '1000'
            item['img'].append(img_clear)
            item['link'] = 'https://www.findel-international.com'+findel.css('a.product-pod__link::attr(href)').extract_first()
            item['code'] = item['link'][item['link'].rindex('/')+1:].upper()
            item['classsify'] = item['link'][37:-len(item['code'])]
            yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse_detail) #此处进入详情页调用parse_detail
                    
        if response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first() is not None: # 如果有下一页标签,没有表示结束了
            page = response.css('a.pager__link.page-link.page-link--next::attr(data-page)').extract_first()     
            next = response.request.url + "?p=" + page + "&show=100"
            print(next)
            url =next
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=False)

    def parse_detail(self, response):
        #调用进入详情页获得详细信息
        item = response.meta['item']
        if response.css('.product-details__delivery-notice::text').extract_first() is not None:
            item['delivery'] = response.css('.product-details__delivery-notice::text').extract_first()
        if response.css('#facetGroup-433').extract_first() is not None:
            item['nature'] = response.css('#facetGroup-433 option::text').extract()
        if response.css('#facetGroup-434').extract_first() is not None:
            item['size'] = response.css('#facetGroup-434 option::text').extract()
        item['describe'] = response.css('.product-description__content div p::text').extract()  
        yield item 

           
 
    
