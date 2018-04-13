# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from ..items import SpiderTutorialItem
from ..tool import *

class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['europages.co.uk']
    start_urls = ['https://www.europages.co.uk/business-directory-europe.html']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    links = LinkExtractor(allow='https://www.europages.co.uk:443.*',restrict_css=('.clickable'))
    rules = [Rule(link_extractor=links, callback="parseContent", follow=False)]
    def parseContent(self, response):
        divs = response.xpath('.//div[@id="domain-columns"]//li')
        for div in divs:
            url =div.xpath('./a/@href').extract()[0]
            yield Request(url, callback=self.second_parse)

    def second_parse(self, response):
        # 接收上级已爬取的数据
        # 一级内页数据提取
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
            yield Request(next_url[0], headers=self.headers,callback=self.second_parse)
            # 有下级页面爬取 注释掉数据返回
            # return item

    def detail_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        # 二级内页数据提取
        # item['address'] = tool.format_array(response.xpath('.//ul[@class="baseinfo"]/li[@class="linfo"]/a/text()').extract())
        item['website'] = extractDomainFromURL(format_array(
            response.xpath('.//div[@class="website"]//span[@class="id-pagepeeker-data"]/@rel').extract()))
        # 最终返回数据给爬虫引擎
        if item['website']:
            yield item


