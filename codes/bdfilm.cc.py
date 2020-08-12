import pickle
import time
import sys
import os
import re
import random
import base64
from bs4 import BeautifulSoup
from faker import Faker
import json
import requests
import urllib
from termcolor import colored
import timeout_decorator
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pprint
from telegm import ServerLogger

logging.basicConfig(level=logging.ERROR, format='%(message)s')


class BDFilm():
    def __init__(self):
        self.mainpage = 'https://www.bd-film.cc/top100.htm'
        self.fake = Faker()
        self.filmlog = json.load(open('film.json', 'r'))
        self.sl = ServerLogger()
        self.s = requests.Session()

    def parseFilm(self, url):
        options = Options()
        options.add_argument('--headless')
        d = webdriver.Chrome(options=options)
        d.get(url)
        html = d.page_source
        d.quit()
        # html = open('test.html', 'r')
        soup = BeautifulSoup(html, 'lxml')

        dblink = soup.find('a', href=re.compile(
            r'https://movie.douban.com/*')).attrs['href']  # douban link
        douban = Helper().parseDoubanInfo(dblink)
        status = []
        ed2k = {}
        dupan = {}
        filmname = douban['name'].split()[0].replace("：", '_')

        for t in soup.findAll('textarea'):
            ed2k_href = re.search(r'h=(.*)\|', t.text)
            if ed2k_href:
                hashvalue = ed2k_href.groups()[0]
                ed2k[hashvalue] = Helper().parseEd2kLink(t.text, filmname)
                status.append(
                    '链接({}G) {}'.format(
                        ed2k[hashvalue]['size'],
                        ed2k[hashvalue]['newlink']))

            magnet = re.search(r'(magnet:.*)\&', t.text)
            if magnet:
                status.append('链接 {}'.format(magnet.groups()[0]))

        for p in soup.findAll('div', {'class': 'option'}):
            if '版权方' in p.text:
                break  # copyright problem
            href = p.a.attrs['href']
            if not href.startswith('https'):
                continue
            shareaddr = href.split('/')[-1]
            dupan[shareaddr] = Helper().parseBaiduLink(p)
            status.append(
                '度盘 {}\n密码 {}'.format(
                    dupan[shareaddr]['href'],
                    dupan[shareaddr]['pwd']))

        # There is no download link due to copyright problem.
        if not status:
            return None
        text = douban['name']
        while len(status) > 0 and len(
                (text + status[-1]).encode('utf8')) < 280:
            text += '\n' + status.pop()

        poster = douban['image'].replace(
            '.webp', '.jpg').replace(
            's_ratio_poster', 'l')
        urllib.request.urlretrieve(poster, 'poster.jpg')

        json.dump(
            self.filmlog,
            open(
                'film.json',
                'w'),
            ensure_ascii=False,
            indent=2)  # download links do exist
        return text

    def parse_film(self, url):
        '''Get magnet / e2dk / pan.baidu download links
        '''
        page = self.s.get(url, headers={'User-Agent': 'Chrome 82'}).text
        urls = re.search(r"urls = \"(.*)\"\, ads", page).group(1)
        disks = re.search(r"diskUrls = \"(.*)\"\, score", page).group(1)

        urls_decoded = base64.b64decode(urls[::-1]).decode('utf8').split('\n')
        disks_decoded = base64.b64decode(disks[::-1]).decode('utf8').split('\n')
        downloads = []
        
        for u in urls_decoded + disks_decoded:
            if u.startswith('magnet'):
                downloads.append(u.split('&')[0])
            elif 'yun' in u or 'pan.baidu' in u:
                tmp = u.strip().split('||')
                downloads.append(tmp[1] + " 密码 " + tmp[0])

        # print(urls_decoded, disks_decoded, sep="\n\n")
        print(downloads)

        

    def chooseOneFilm(self):
        sp = BeautifulSoup(requests.Session().get(self.mainpage).text, 'lxml')
        tops = sp.findAll('a', {'class': 'videopic'})[
            100:]  # top 100 of this months
        random.shuffle(tops)

        for a in tops:
            attrs = a.attrs
            pageid = attrs['href'].split('/')[-1].split('.')[0]
            if pageid in self.filmlog:
                continue
            if not any(e != '' and float(e) >= 6 for e in a.text.split('\n')):
                continue

            self.filmlog[pageid] = {
                'counter': 1,
                'name': attrs['title'],
                'link': attrs['href']}
            return attrs['href']

        rpageid = random.choice([pi for pi in self.filmlog.keys()])
        self.filmlog[rpageid]['counter'] += 1
        return self.filmlog[rpageid]['link']

    def twitterBot(self):
        try:
            url = self.chooseOneFilm()
            text = self.parseFilm(url)
            if text:
                print(text)
                Helper().postTweet(text)
                self.sl.alertGreco(text, __file__)
        except Exception as e:
            self.sl.alertGreco(str(e), __file__)
            print(e)


class Helper():
    def retrivePoster(self, poster):
        pass

    def parseDoubanInfo(self, dblink):
        s = requests.Session()
        soup = BeautifulSoup(s.get(dblink).text, 'lxml')
        dbinfos = json.loads(
            soup.find(
                'script', {
                    'type': "application/ld+json"}).text, strict=False)
        return dbinfos

    def parseBaiduLink(self, link):
        h = {'href': link.a.attrs['href']}
        pwd = re.search(r'密码:\s*([a-z\d]{4})', link.text)
        if pwd:
            h['pwd'] = pwd.groups()[0]
        return h

    def parseEd2kLink(self, oldlink, filmname):
        h = {'oldlink': oldlink}
        infos = oldlink.split('|')
        h['size'] = '{0:.2f}'.format(round(int(infos[3]) / (1024 ** 3), 2))

        name = re.search(r'\[.*\](.*)', infos[2]).groups()[0].split('.')
        h['name'] = '_'.join([filmname] + name[-3:-1]) + '.' + name[-1]

        infos[2] = h['name']
        h['newlink'] = '|'.join(infos)
        return h

    def postTweet(self, s):
        from twi import from_terminal
        from_terminal([s, 'poster.jpg'])


if __name__ == '__main__':
    bd = BDFilm()
    bd.parse_film('https://www.bd-film.cc/zx/30655.htm')
    # if len(sys.argv) > 1:
    #     Helper().postTweet(bd.parseFilm(sys.argv[1]))
    #     sys.exit(0)

    # while True:
    #     bd.twitterBot()
    #     time.sleep(300 * 6)
    #     # time.sleep(random.randint(3600, 3600 * 5))
