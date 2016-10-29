# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import CsvItemExporter

import langid # To determine lyrics language
import os
import re

class LyricsPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings) # Feed settings into pipeline
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def __init__(self, settings):
        self.filename = settings["EXPORT_PATH"]

    def spider_opened(self, spider):
        filename = 'lyrics.csv'
        if os.path.exists(filename): # If file already exists and we resume work, open file in append mode and do not print header
            self.file = open(filename, 'ab')
            self.exporter = CsvItemExporter(self.file, False)
            self.exporter.start_exporting()
        else: # Create new csv file
            self.file = open(filename, 'w+b')
            self.exporter = CsvItemExporter(self.file)
            self.exporter.start_exporting()


    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        # Only export decently sized, English language lyrics that do not have an overwhelming number of special characters.
        text = item["lyrics"]
        if len(text) < 20:
            print("LYRICS TOO SHORT FOR SONG " + item["song"])
            return item
        if float(len(re.sub('\W+', '', text))) / float(len(text)) < 0.5:
            print("LYRICS CONTAIN TOO MANY SPECIAL CHARACTERS FOR SONG " + item["song"])
            return item
        if langid.classify(text)[0] != "en":
            print("LYRICS ARE NOT ENGLISH FOR SONG " + item["song"])
            return item
        self.exporter.export_item(item)
        return item
