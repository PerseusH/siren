#! /usr/bin/env python
# encoding=utf-8


import requests
import time, random, json
from bs4 import BeautifulSoup


today = time.strftime('%Y-%m-%d', time.localtime())
GAMES_URL = 'https://www.zhibo8.cc/nba/json/%s.htm?key=%s' % (today, str(random.random()))


def download(url):
    return requests.get(url)


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


def game_info(gid):
    ginfo = {}

    ginfo_url = 'https://news.zhibo8.cc/nba/%s/%s.htm' % (today, gid)
    gifo_soup = parse_html(download(ginfo_url).content)
    ginfo['title'] = gifo_soup.find('div', attrs={'class': 'title'}).h1.getText()
    ginfo['brief1'] = gifo_soup.find('div', attrs={'class': 'content'}).find_all('p')[3].getText()
    ginfo['brief2'] = gifo_soup.find('div', attrs={'class': 'content'}).find_all('p')[4].getText()

    score_url = 'https://bifen4pc.qiumibao.com/json/%s/%s.htm' % (today, gid)
    score = download(score_url).json()
    sinfo = '%s %s:%s %s' % (
            score['home_team'],
            score['home_score'],
            score['visit_score'],
            score['visit_team']
            )
    ginfo['score'] = sinfo

    return ginfo


def ec(s):
    return s.encode('utf-8')


if __name__ == '__main__':
    data = download(GAMES_URL).json()
    items = data['video_arr']
    for i in filter(lambda i: i['title'].startswith('NBA常规赛'), items):
        #print ec(i['saishiid']), ec(i['shortTitle']), i['updatetime'], i['url']
        ginfo = game_info(i['saishiid'])
        print ec(ginfo['title'])
        print ec(ginfo['score'])
        print ec(ginfo['brief1'])
        print ec(ginfo['brief2'])
        print '---------------------------------------------------------------------------------------'
