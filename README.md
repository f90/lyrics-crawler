# LyricsCrawler (for Metrolyrics and Lyricswiki)

Automatically downloads lyrics for the top X songs of each artist on the metrolyrics database, and saves them into a CSV along with the artist, song name, and URL.

Currently filters out non-English lyrics using langid, but the specific language can be easily adapted. Also filters out broken lyrics.

Supports resuming the download after application crash or internet failure.
Built on the basic example at https://github.com/vmm/lyrics-generator

## Usage and requirements

### Required packages
The web crawler is based on python Scrapy project - find documentation from http://scrapy.org/. 

1) Install Scrapy:

```sh
pip install scrapy
 ```

2) For language filtering, langid is used (https://github.com/saffsd/langid.py). Install langid as follows:

```sh
pip install langid
```

### Settings (optional)

Open the settings.py file inside the metrolyrics folder to change the settings. In particular, the number of concurrent requests, the path for the lyrics output, and the number of songs crawled for each artist can be set.

### Usage

1) Starting the crawler:

```sh
# Go to the scrapy project top level folder
cd crawlers

# Run the spider - output the results as simple csv file with lyrics, lyrics URL, song name, and artist name as columns.
scrapy crawl metrolyrics -s JOBDIR=jobstate
```

The current crawler state is saved for later resuming. By default, results are saved in "lyrics.csv" in the same folder.

2) Resuming the crawler:

Make sure your previous lyrics file is still in the same location, then execute 
```sh
scrapy crawl metrolyrics -s JOBDIR=jobstate
```

The newly downloaded lyrics should now be appended to the already existing ones.

