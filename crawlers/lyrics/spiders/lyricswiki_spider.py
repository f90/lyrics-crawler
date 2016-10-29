from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from metrolyrics.items import LyricsItem

from scrapy.http import Request
import re
import string

extract_alphabets = list(string.ascii_lowercase)
base_url = 'http://lyrics.wikia.com/wiki/Category:Song'

def clean_html_but_br(string):
    cleaned = re.sub("<.div.*?>", "", string) # Remove divs
    cleaned = re.sub("<br>", "\n", cleaned) # Turn <br> into newlines
    cleaned = re.sub("<.*?>", "", cleaned) # Remove all other html tags (br tags all have newlines already)

    # Clean up beginning and end
    cleaned = cleaned.strip()
    cleaned = cleaned.strip("\n")
    cleaned = cleaned.strip("\"")

    cleaned = cleaned.replace(",", "") # Remove comma as this is our delimiter (we will remove more special characters later anyway)
    return cleaned

class MetroLyricsSpider(CrawlSpider):
    name = 'lyricswiki'
    allowed_domains = ['http://lyrics.wikia.com', 'lyrics.wikia.com', 'www.lyrics.wikia.com']

    start_urls = ["http://lyrics.wikia.com/wiki/Category:Song"]
    #for a in extract_alphabets:
    #    start_urls.append(base_url % a)
    rules = (
        # Extract links matching to pagination and allow to follow them
        Rule (LinkExtractor(restrict_xpaths=("//a[@class='paginator-next button secondary']",)), follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # -> http://www.metrolyrics.com/patsy-cline-lyrics.html
        Rule(LinkExtractor(allow=('http://lyrics.wikia.com/wiki/.*', ),
                               restrict_xpaths="//div[@id = 'mw-pages']//div[@class = 'mw-content-ltr']"),
                                callback='parse_page')
    )

    def parse_page(self, response):
        item = LyricsItem()
        item["lyricsURL"] = response.url
        print("PARSING URL: " + response.url)
        item["artist"] = response.xpath("//meta[@property='og:title']/@content").extract()[0].split(":")[0]
        print(item["artist"])
        item["song"] = response.xpath("//div[@id='song-header-title']/b/text()").extract()[0]
        print(item["song"])

        # Extract lyrics
        lyrics = response.xpath("//div[@class='lyricbox']").extract()[0]

        # Drop non-printable characters
        printable = set(string.printable)
        lyrics = filter(lambda x: x in printable, lyrics)

        item["lyrics"] = clean_html_but_br(lyrics)

        return item