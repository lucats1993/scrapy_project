# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import settings
import logging
from scrapy_spider.module import db

class SpiderPipeline(object):
    def __init__(self):
        # 连接数据库
        db.create_engine(settings.MYSQL_USER, settings.MYSQL_PASSWD, settings.MYSQL_DBNAME, settings.MYSQL_HOST)
    def process_item(self, item, spider):
        try:
            # 插入数据
            db.replace('copy2', **item)
            # 提交sql语句
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item

