# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['scrapy_spider.spiders']
NEWSPIDER_MODULE = 'scrapy_spider.spiders'

# USER_AGENT = 'scrapy_spider-redis (+https://github.com/rolando/scrapy-redis)'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

DOWNLOADER_MIDDLEWARES = {
    'scrapy_spider.middlewares.UserAgentMiddleware': 543,
    # 'zhihu.middlewares.CookiesMiddleware': 544,
    #'zhihu.middlewares.ProxyMiddleware':125,
    #"scrapy_spider.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 545,
}


ITEM_PIPELINES = {
    # 'example.pipelines.SpiderPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'industry'
MYSQL_USER = 'root'
MYSQL_PASSWD = '1234'

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

REDIS_HOST = '192.168.0.102'
REDIS_PORT = 6379

