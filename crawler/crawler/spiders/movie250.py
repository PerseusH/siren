# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from crawler.items import MovieItem


class Movie250Spider(Spider):
    name = 'movie250'
    url = 'https://movie.douban.com/top250'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        #item = MovieItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        #for movie in movies:
        #    title = movie.xpath('div[@class="hd"]/a/span/text()').extract()
        #    fullTitle = ''
        #    for each in title:
        #        fullTitle += each
        #    movieInfo = movie.xpath('div[@class="bd"]/p/text()').extract()
        #    star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
        #    quote = movie.xpath('div[@class="bd"]/p/span/text()').extract()
        #    if quote:
        #        quote = quote[0]
        #    else:
        #        quote = ''
        #    item['title'] = fullTitle
        #    item['movieInfo'] = ';'.join(movieInfo).replace(' ', '').replace('\n', '')
        #    item['star'] = star[0]
        #    item['quote'] = quote
        #    yield item
        for movie in movies:
            yield {'title': movie.xpath('div[@class="hd"]/a/span/text()').extract()}
        nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextPage:
            nextPage = nextPage[0]
            print(self.url + str(nextPage))
            yield Request(self.url + str(nextPage), callback=self.parse)
