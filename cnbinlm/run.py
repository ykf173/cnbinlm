# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

spiders = [
    'scrapy crawl cnbi',
]

if __name__ == '__main__':
    for i in spiders:
        execute(i.split())