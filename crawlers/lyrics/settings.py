# -*- coding: utf-8 -*-

# Scrapy settings for azlyrics project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lyrics-scraper'

SPIDER_MODULES = ['lyrics.spiders']
NEWSPIDER_MODULE = 'lyrics.spiders'

ITEM_PIPELINES = {
    'lyrics.pipelines.LyricsPipeline': 300
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 1

EXPORT_PATH = 'lyrics.csv' # Filepath of lyrics CSV
SONGS_PER_ARTIST = 3 # For metrolyrics: First X lyrics of each artist are going to be crawled (if available)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'azlyrics (+http://www.yourdomain.com)'
