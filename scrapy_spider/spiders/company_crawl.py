# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import SpiderTutorialItem
from ..module.tool import *
from scrapy_redis.spiders import RedisSpider


class CompanySpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'co_crawl'
    allowed_domains = ['exactseek.com']
    start_urls = ['http://local.exactseek.com/']
    rules = (
        Rule(LinkExtractor(allow='category', restrict_css=('.info h5'))),
        Rule(LinkExtractor(allow='category', restrict_css=('.pagination'))),
        Rule(LinkExtractor(allow='detail', restrict_css=('.view-h3')), callback="parse_content")
    )

    def parse_content(self, response):
        # 接收上级已爬取的数据
        item = SpiderTutorialItem()
        item['company_name'] = get_coName(response.xpath('.//span[@itemprop="name"]/span/text()').extract())
        item['phone'] = check_list(response.xpath('.//span[@itemprop="telephone"]/text()').extract())
        item['website'] = extractDomainFromURL(
            check_list(response.xpath('.//ul[@class="dropdown-menu"]//a[@itemprop="url"]/@href').extract()))
        item['email'] = check_list(
            response.xpath('.//ul[@class="dropdown-menu"]//a[@role="button"]/text()').extract())
        yield item

    def detail_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        # 二级内页数据提取
        item['website'] = extractDomainFromURL(check_list(
            response.xpath('.//div[@class="website"]//span[@class="id-pagepeeker-data"]/@rel').extract()))
        # 最终返回数据给爬虫引擎
        if item['website']:
            yield item
