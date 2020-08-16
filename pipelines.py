# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
import csv
import json
# class LagouPipeline:
#
#     def __init__(self):
#         self.fp = open("lagou_python.json",'bw')
#         self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.fp.close()

class lagouCsvPipline:

    def __init__(self):
        self.fp = open("lagou_java1.csv",'w',encoding="utf-8",newline="")


        self.headers = ['job_salary', 'job_name', 'job_overlook', 'job_tempt', 'job_location', 'job_descript', 'company_name',
                   'company_field', 'company_stage', 'company_size', 'company_website']
        self.writer = csv.DictWriter(self.fp, self.headers)
        self.writer.writeheader()
        self.num = 1

    def process_item(self, item, spider):

        self.writer.writerow(item)
        print("写入{}条数据到csv文件了".format(self.num))
        print("--------------------"*2)
        self.num += 1
        return item

    def close_spider(self, spider):
        self.fp.close()