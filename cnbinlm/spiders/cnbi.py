# -*- coding: utf-8 -*-
import scrapy
import re
from cnbinlm.items import CnbinlmItem

class CnbiSpider(scrapy.Spider):
    name = 'cnbi'
    allowed_domains = []
    start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4423170/']

    def parse(self, response):
        PMID = response.css('.fm-citation-pmid a::attr(href)').extract_first()
        taglist = response.xpath('//div[@class="tsec sec"]').extract()
        # for tag in taglist:
        #     print('tag1+'+tag)
        article = []

        for tag in taglist:
            if '"idm' not in tag and 'Abs' not in tag and 's' in tag:
                id = '//div[@id="' + tag[9:tag.find('" ')] + '"]/descendant::text()'
                segment = response.xpath(id).extract()
                if(len(self.deal_data(segment)) > 10):
                    article.append(self.deal_data(segment))

        pmc = response.url.split('/')
        pmc = pmc[len(pmc)-2]
        item = CnbinlmItem()

        item['pmid'] = str(PMID.split('/')[len(PMID.split('/'))-1])
        item['article'] = article
        item['pmc'] = pmc
        yield item

        with open('./url/url.txt', 'r') as f:
            new_urllist = f.read().split('\n')
            f.close()

        for new_url in new_urllist:
            new_url = response.urljoin(new_url)
            yield scrapy.Request(new_url, callback=self.parse)

    def deal_data(self, article):
        arti = ''
        sar = ''

        for ar in article:
            if len(ar) > 20 or len(ar) == 1:
                sar += ar
                if ar[len(ar)-3:] == ']. ' or ar[len(ar)-2:] == '. '\
                    or ar[len(ar)-2:] == '].' or ar[len(ar)-1:] == ' '\
                    or ar[len(ar)-1:] == '.':
                    arti += sar.replace('[', '').replace(']', '')
                    sar = ''
                if ar[len(ar)-3:] == '). ' or ar[len(ar)-2:] == '. '\
                    or ar[len(ar)-2:] == ').' or ar[len(ar)-1:] == ' '\
                    or ar[len(ar)-1:] == '.':
                    ar += sar.replace('(', '').replace(')', '')
                    sar = ''

        return arti