from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from metrolyrics.items import LyricsItem

from scrapy.http import Request
import re
import string

extract_alphabets = list(string.ascii_lowercase)
base_url = 'http://www.metrolyrics.com/artists-%s-1.html'

def clean_html_but_br(string):
    # This HTML tag triggers a new paragraph, so we convert it into two line breaks
    cleaned = re.sub("<p.*?>", "\n\n", string)

    cleaned = re.sub("<.*?>", "", cleaned) # Remove all other html tags (br tags all have newlines already)

    # Clean up beginning and end
    cleaned = cleaned.strip()
    cleaned = cleaned.strip("\n")
    cleaned = cleaned.strip("\"")

    cleaned = cleaned.replace(",", "") # Remove comma as this is our delimiter (we will remove more special characters later anyway)
    return cleaned

class MetroLyricsSpider(CrawlSpider):
    name = 'metrolyrics'
    allowed_domains = ['www.metrolyrics.com']

    start_urls = []
    for a in extract_alphabets:
        start_urls.append(base_url % a)
    rules = (
        # Extract links matching to pagination and allow to follow them
        Rule (LinkExtractor(restrict_xpaths=('//a[@class="button next"]',)), follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # -> http://www.metrolyrics.com/patsy-cline-lyrics.html
        Rule(LinkExtractor(allow=('http://www.metrolyrics.com/.*', ),
                               restrict_xpaths="//table[@class='songs-table']"), 
             callback='parse_page'),
    )

    def parse_page(self, response):
        artist = response.xpath("//div[@class='artist-header content-header row']/div/h1/text()").extract()[0].strip()

        top_list_song = response.xpath("//table")

        songList = top_list_song.xpath(".//a/@href").extract()
        for url in songList[0:min(self.settings["SONGS_PER_ARTIST"], len(songList) - 1)]:
            print("URL " + url)

        for url in songList[0:min(self.settings["SONGS_PER_ARTIST"], len(songList) - 1)]:
            item = LyricsItem()
            item["lyricsURL"] = url
            item["artist"] = artist

            req = Request(url, callback=self.parse_lyrics)
            req.meta["item"] = item

            yield req


    def parse_lyrics(self, response):
        item = response.meta["item"]

        songName = response.xpath("//div[@class='lyrics']/header/h1/text()").extract()[0]
        songName = songName[1:-8] # Cut off "Lyrics" and line break

        lyrics = response.xpath("//div[@id='lyrics-body-text']").extract()[0]
        # Drop non-printable characters
        printable = set(string.printable)
        lyrics = filter(lambda x: x in printable, lyrics)

        item["lyrics"] = clean_html_but_br(lyrics)
        item["song"] = songName.strip()

        return item

