# -*- coding:utf-8 -*-
import scrapy, json
from scrapy import Selector


class Zhibo8Spider(scrapy.Spider):
    name = 'zhibo8'
    #allowed_domains = ['zhibo8.com']
    start_urls = ['https://www.zhibo8.cc']

    def parse(self, response):
        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()
        games = Selector(response).xpath(
                '//div[@class="schedule_container left"]/div[@class="box"]/div[@class="content"]/ul/li[contains(@label, "NBA")]'
                )
        for game in games:
            label = game.xpath('@label').extract()[0].encode('utf-8')
            link = game.xpath('a[1]/@href').extract()[0]
            start_time = game.xpath('@data-time').extract()[0]
            print label,' ', start_time, ' ', '%s%s' % (self.start_urls[0], link) 
