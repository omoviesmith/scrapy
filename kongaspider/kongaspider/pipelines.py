# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PriceToUSDPipeline:

    ngnToUsdRate = 0.0022

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## check is price present
        if adapter.get('price'):

            #converting the price to a float
            floatPrice = float(adapter['price'].replace(',',''))

            #converting the price from gbp to usd using our hard coded exchange rate
            adapter['price'] = round(floatPrice * self.ngnToUsdRate, 0)

            return item

        else:
            # drop item if no price
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item


