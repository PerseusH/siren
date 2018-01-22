# -*- coding:utf-8 -*-
import scrapy, time, json, random, re
from scrapy import Selector


class Zhibo8Spider(scrapy.Spider):
    name = 'zhibo8'
    #allowed_domains = ['zhibo8.com']
    prefix = 'https://www.zhibo8.cc'
    today = time.strftime('%Y-%m-%d', time.localtime())
    start_urls = [
            'https://www.zhibo8.cc/nba/json/%s.htm?key=%s' %
            (today, str(random.random()))
            ]

    def parse(self, response):
        current_url = response.url
        body = response.body
        games = json.loads(body)['video_arr']
        for game in games:
            title = game['title'].encode('utf-8')
            if 'NBA常规赛' in title:
                url = '%s%s' % (self.prefix, game['url'])
                yield scrapy.Request(url, callback=self.transfer)

    def transfer(self, response):
        selector = Selector(response)
        body = response.body
        pos_game_id = body.find('p_saishi_id')
        pattern = re.compile(r"\'[\S\s]+?\'")
        url = 'https://news.zhibo8.cc/nba/%s/%s.htm' % (self.today, pattern.findall(body[pos_game_id:])[0][1: -1])
        yield scrapy.Request(url, callback=self.game_info)

    def game_info(self, response):
        selector = Selector(response)
        title = selector.xpath('//div[@class="tzhanbao"]/div[@class="title"]/h1/text()').extract()[0].encode('utf-8')
        brief1 = selector.xpath('//div[@class="tzhanbao"]/div[@class="content"]/p[4]/text()').extract()[0].encode('utf-8')
        brief2 = selector.xpath('//div[@class="tzhanbao"]/div[@class="content"]/p[5]/text()').extract()[0].encode('utf-8')
        print title
        print ''
        print brief1
        print brief2
        print '---------------------------------------------------------------------------------------------'
