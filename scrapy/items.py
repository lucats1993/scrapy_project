# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class SpiderTutorialItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = Field()
    type_I = Field()
    type_II = Field()
    company_name = Field()
    address = Field()
    website = Field()
    phone = Field()
    fax = Field()
    email = Field()
    pass

class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
