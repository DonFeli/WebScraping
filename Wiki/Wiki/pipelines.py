# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class WikiPipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'felita'
        password = 'pokl' # your password
        database = 'infoviz'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into wiki_content(name, url, description) values(%s,%s)",(item['name'],item['url'], item['description']))
        self.connection.commit()
        return item