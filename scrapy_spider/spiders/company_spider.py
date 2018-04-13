# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import SpiderTutorialItem
from ..module.tool import *
from scrapy_redis.spiders import RedisSpider


class CompanySpider(RedisSpider):
    """Follow categories and extract links."""
    name = 'co_spider'
    allowed_domains = ['europages.co.uk']
    # start_urls = ['https://www.europages.co.uk/business-directory-europe.html']
    # rules = (Rule(LinkExtractor(deny='companies',restrict_css=('.clickable'))),
    #          Rule(LinkExtractor(allow='companies',restrict_xpaths=('.//div[@id="domain-columns"]//li')),callback="parse_content"))

    def start_requests(self):
        url = 'https://www.europages.co.uk/business-directory-europe.html'
        yield Request(url)

    def parse(self,response):
        nodes = response.xpath('//div[not(@class="clickable")]/h2[@class="theme-title"]/a')
        source_url = extractDomainFromURL(response.url).split(':')[0]
        for node in nodes:
            item = SpiderTutorialItem()
            item['type_I'], item['type_II'] = get_realType(re.findall(r'^\w+',node.xpath('./text()').extract()[0])[0])
            item['source'] = source_url
            url = node.xpath('./@href').extract()[0]
            yield Request(url, meta={'item_1': item}, callback=self.sec_parse)

    def sec_parse(self,response):
        item_1 = response.meta['item_1']
        co_items = response.xpath('.//div[@id="domain-columns"]//li')
        for co_item in co_items:
            url = co_item.xpath('./a/@href').extract()[0]
            yield Request(url, meta={'item_1': item_1}, callback=self.parse_content)


    def parse_content(self, response):
        # 接收上级已爬取的数据
        co_items = response.xpath('.//ul[@class="full-list-article"]/li/div[contains(@class,"main-title")]/a[1]')
        for co_item in co_items:
            item = SpiderTutorialItem()
            item['company_name'] = get_coName(co_item.xpath('./text()').extract())
            url =co_item.xpath('./@href').extract()[0]
            # 二级内页地址爬取
            yield Request(url, meta={'item': item}, callback=self.detail_parse)
        next_url = response.xpath('//ul[@class="page-navi clearfix"]/li[last()]/a[@title="Next page"]/@href').extract()
        if next_url:
            # second_url = re.findall(r'.*\/',response.url)[0] + next_url[0]
            yield Request(next_url[0], callback=self.parse_content)
            # 有下级页面爬取 注释掉数据返回
            # return item

    def detail_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        # 二级内页数据提取
        item['website'] = extractDomainFromURL(format_array(
            response.xpath('.//div[@class="website"]//span[@class="id-pagepeeker-data"]/@rel').extract()))
        # 最终返回数据给爬虫引擎
        if item['website']:
            yield item


