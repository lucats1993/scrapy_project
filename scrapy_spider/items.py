# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SpiderTutorialItem(Item):
    # define the fields for your item here like:
    source = Field()
    type_I = Field()
    type_II = Field()
    company_name = Field()
    address = Field()
    website = Field()
    phone = Field()
    fax = Field()
    email = Field()
