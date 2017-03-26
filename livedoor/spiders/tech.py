# -*- coding: utf-8 -*-
import scrapy


class TechSpider(scrapy.Spider):
    name = "tech"
    ## tech 
    # start_urls = ['http://news.livedoor.com/article/category/210/']
    ## entertainment
    # start_urls = ['http://news.livedoor.com/article/category/10/']
    ## sports
    # start_urls = ['http://news.livedoor.com/topics/category/sports/']
    ## world
    # start_urls = ['http://news.livedoor.com/article/category/3/']
    ## politics
    start_urls = ['http://news.livedoor.com/article/category/1/']


    def parse(self, response):
        for href in response.css('ul.articleList a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_single)

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = 'http://news.livedoor.com/article/category/1/'+next_page
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_single(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()
        
        yield {
                'title': extract_with_css('h1.articleTtl::text'),
                'content': ''.join(response.css('div.articleBody p::text').extract()).replace('\xa0', '')
                }
