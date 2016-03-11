from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from metrolyrics.items import LyricsItem
from scrapy.http import Request
import re
import string

extract_alphabets = list(string.ascii_lowercase)
base_url = 'http://www.metrolyrics.com/artists-%s-1.html'

def clean_html_but_br(string):
    return re.sub("<.*>", " ", string).split("\n \n")

class MetroLyricsSpider(CrawlSpider):
    name = 'metrolyrics'
    allowed_domains = ['www.metrolyrics.com']

    start_urls = []
    for a in extract_alphabets:
        start_urls.append(base_url % a)
    rules = (
        # Extract links matching to pagination and allow to follow them
        Rule (SgmlLinkExtractor(restrict_xpaths=('//a[@class="button next"]',)), follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # -> http://www.metrolyrics.com/patsy-cline-lyrics.html
        Rule(SgmlLinkExtractor(allow=('http://www.metrolyrics.com/.*', ),
                               restrict_xpaths="//table[@class='songs-table']"), 
             callback='parse_artist'),
    )

    def parse_artist(self, response):
        top_list_song = response.xpath("//table")
        for url in top_list_song.xpath(".//a/@href").extract()[2:4]:
            yield Request(url, callback=self.parse_lyrics)


    def parse_lyrics(self, response):
        item = LyricsItem()

        lyrics = response.xpath("//div[@id='lyrics-body-text']").extract()[0]

        item['lyrics'] = clean_html_but_br(lyrics)
        return item 

