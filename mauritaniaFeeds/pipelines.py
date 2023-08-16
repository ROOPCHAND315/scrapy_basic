# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os 
import sys
sys.path.insert(0,'/home/roopchand/projects/scrapyTest/mauritaniaFeeds/mauritaniaFeeds')
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from process_crawler import full_description
from items import Feeds,Article

class MauritaniafeedsPipeline:
    # Desclink=item.get('link')
    def __init__(self):
        self.conn=pymongo.MongoClient(
            'localhost',
            27017
        )
        db=self.conn['Testspider']
        self.collection = db['testTable']


    def process_item(self, item, spider):
        item =dict(item)
        if len(item)>2:
            link = item['link']
            source_id = item['source_id']
            pubDate = item['pubDate']
            description = item['description']
            title = item['title']

            data = {"title":title,"source_id":source_id,"description":description,"link":link,"pubDate":pubDate}
            
            self.collection.insert_one(data)
            full_description(spider='aajtak_fd',url=data['link'])
            
        if len(item)==2:
            try:
                # print("inside FullDescription")
                full_des=item['full_description']
                url = item['url']
            
                self.collection.update_one({'link':url},{'$set':{'full_description':full_des}})
                # self.full_descript.insert_one(data)
            except Exception as e:
                print("Error in fd",str(e))




        # if isinstance(item,Feeds):
        #     print("inside Items")
        #     link = item['link']
        #     source_id = item['source_id']
        #     pubDate = item['pubDate']
        #     description = item['description']
        #     title = item['title']

        #     data = {"title":title,"source_id":source_id,"description":description,"link":link,"pubDate":pubDate}
            
        #     self.collection.insert_one(data)
        #     full_description(spider='aajtak_fd',url=data['link'])
            
        # if isinstance(item,Article):
        #     print("inside FullDescription")
        #     full_des=item['full_description']
        #     data={'full_description':full_des}
        #     self.full_descript.insert_one(data)


            

        # if item['souce_id']:
        #     print("hello")
        #     print(item['source_id'])


        # print("Items>>>>>>>>>",item)
        # try:
        #     if isinstance(item,MauritaniafeedsItem):

        #         print("Link>>>>>>>>>>>>>>>.",item)
        #         self.collection.insert_one(dict(item))
        #         full_description(link=item['link'],spider='aajtak_fd')
                
        #     if isinstance(item,full_description_data):
        #         print(item)
        #         pass
        # except Exception as e:
        #     print("Error >>>>>>>",str(e))
      