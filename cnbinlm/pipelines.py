# -*- coding: utf-8 -*-
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CnbinlmPipeline(object):
    def process_item(self, item, spider):
        #pmc = item['pmc']
        pmid = item['pmid']
        path = "./spider_result/article.txt"
        dic = {'pmid':pmid}
        dic['article'] = item['article']
        with open(path, "a", encoding='utf-8') as f:
            f.writelines(json.dumps(dic, ensure_ascii=False) + '\n')

        f.close()
        return item
