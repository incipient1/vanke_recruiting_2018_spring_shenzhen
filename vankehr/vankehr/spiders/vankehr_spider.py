# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import pyquery
from ..items import VankeItem


class VankehrSpiderSpider(scrapy.Spider):
    name = 'vankehr_spider'
    allowed_domains = ['vanke.com']
    url_format = r'http://rc.vanke.com/positions/search?occupation=-1&location_weak=\
    %E6%B7%B1%E5%9C%B3&published_id=5&keyword=&page={}'
    start_urls = [url_format.format(1)]

    def parse(self, response):
        pq = pyquery.PyQuery(response.text)
        padding = pq('#js-container > div > div:has("div") > div')

        for i in padding.items():
            meta = {}
            meta['position'] = i('ul > li:eq(0) > a').text()
            meta['detail_url'] = i('ul > li:eq(0) > a').attr('href')
            meta['company'] = i('ul > li:eq(1)').text()
            meta['occupation'] = i('ul > li:eq(2)').text()
            meta['city'] = i('ul > li.city > span.J_tipsy').text()
            meta['update'] = i('ul > li.update').text()
            meta['id_position'] = i('ul > li.action > span.js-detail').attr('data-id')

            url = 'http://rc.vanke.com/positions/detail?id={}'.format(meta['id_position'])
            yield Request(url,
                          callback = self.detail_parse,
                          meta = meta,
                          priority = 10,
                          )

        for page_num in range(2,12):
            yield Request(self.url_format.format(page_num),
                          callback = self.parse
                        )

    def detail_parse(self,response):
        pq2 = pyquery.PyQuery(response.text)
        extra_info = pq2('#body-inner > div > div > div > div > p').text().split('/')
        item = VankeItem()

        item['number'] = extra_info[0]
        item['degreee'] = extra_info[1]
        item['experience'] = extra_info[2]
        item['job_demand'] = pq2('#body-inner > div > div > div > div.module-bd:eq(0)').text()
        item['job_content'] = pq2('#body-inner > div > div > div > div.module-bd:eq(1)').text()

        item['position'] = response.meta['position']
        item['company'] = response.meta['company']
        item['occupation'] = response.meta['occupation']
        item['city'] = response.meta['city']
        item['update'] = response.meta['update']
        item['id_position'] = response.meta['id_position']

        yield item