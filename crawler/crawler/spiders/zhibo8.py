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
        body = response.body
        pos_game_id = body.find('p_saishi_id')
        if pos_game_id is not -1:
            pattern = re.compile(r"\'[\S\s]+?\'")
            game_id = pattern.findall(body[pos_game_id:])[0][1: -1]
            score_url = 'https://bifen4pc.qiumibao.com/json/%s/%s.htm' % (self.today, game_id)
            ginfo_url = 'https://news.zhibo8.cc/nba/%s/%s.htm' % (self.today, game_id)
            yield scrapy.Request(ginfo_url, meta={'score_url': score_url}, callback=self.game_info)

    def game_info(self, response):
        selector = Selector(response)
        sel_score = selector.xpath('//div[@class="bifen radt5"]')
        title = selector.xpath('//div[@class="tzhanbao"]/div[@class="title"]/h1/text()').extract()[0].encode('utf-8')
        brief1 = selector.xpath('//div[@class="tzhanbao"]/div[@class="content"]/p[4]/text()').extract()[0].encode('utf-8')
        brief2 = selector.xpath('//div[@class="tzhanbao"]/div[@class="content"]/p[5]/text()').extract()[0].encode('utf-8')
        yield scrapy.Request(response.meta['score_url'], meta={'title': title, 'brief1': brief1, 'brief2': brief2}, callback=self.score)

    def score(self, response):
        body = json.loads(response.body)
        meta = response.meta
        print body['home_team'].encode('utf-8'), body['home_score'], ':', body['visit_score'], body['visit_team'].encode('utf-8')
        print meta['title']
        print ''
        print meta['brief1']
        print meta['brief2']
        print '---------------------------------------------------------------------------------------------'
