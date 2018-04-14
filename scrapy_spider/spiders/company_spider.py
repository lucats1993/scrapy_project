# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ..items import SpiderTutorialItem
from ..module.tool import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class CompanySpider(RedisSpider):
    name = "co_spider"
    # start_urls = ["https://www.europages.co.uk/business-directory-europe.html"]

    def start_requests(self):
        url = 'https://www.europages.co.uk/business-directory-europe.html'
        yield Request(url)

    def parse(self, response):
        nodes = response.xpath('//div[@class="clickable"]/h2/a')
        source_url = extractDomainFromURL(response.url).split(':')[0]
        for node in nodes:
            item = SpiderTutorialItem()
            type_name = check_list(re.findall(r'^\w+', check_list(node.xpath('./text()').extract())))
            item['type_I'], item['type_II'] = get_realType(type_name)
            item['source'] = source_url
            yield Request(check_list(node.xpath('./@href').extract()), meta={'item_1': item}, callback=self.sec_parse)

    def sec_parse(self, response):
        item_1 = response.meta['item_1']
        co_items = response.xpath('.//div[@id="domain-columns"]//li')
        for co_item in co_items:
            yield Request(check_list(co_item.xpath('./a/@href').extract()), meta={'item_1': item_1}, callback=self.thr_parse)

    def thr_parse(self, response):
        item_1 = response.meta['item_1']
        co_items = response.xpath('.//ul[@class="full-list-article"]/li/div[contains(@class,"main-title")]/a[1]')
        for co_item in co_items:
            item = SpiderTutorialItem()
            item['type_I'], item['type_II'] = item_1['type_I'], item_1['type_II']
            item['source'] = item_1['source']
            item['company_name'] = get_coName(co_item.xpath('./text()').extract())
            url = check_list(co_item.xpath('./@href').extract())
            yield Request(url, meta={'item': item}, callback=self.detail_parse)
        next_url = response.xpath('//ul[@class="page-navi clearfix"]/li[last()]/a[@title="Next page"]/@href').extract()
        if next_url:
            # second_url = re.findall(r'.*\/',response.url)[0] + next_url[0]
            yield Request(next_url[0], meta={'item_1': item_1}, callback=self.thr_parse)
            # 有下级页面爬取 注释掉数据返回
            # return item

    def detail_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        # 二级内页数据提取
        item['website'] = extractDomainFromURL(check_list(
            response.xpath('.//div[@class="website"]//span[@class="id-pagepeeker-data"]/@rel').extract()))
        # 最终返回数据给爬虫引擎
        if item['website']:
            yield item
