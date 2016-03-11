# Random Song Lyrics Generator

This is a simple web crawler excercise - Basically it extracts all of the lyrics (all artis from A to Z) from a well known lyric site and saves them to a local file and generates random 'song lyrics' using the extracted lyrics as the source.

## Usage and requirements

### Web crawler
The web crawler is based on python Scrapy project - find documentation from http://scrapy.org/. 

1) Install Scrapy:

```sh
pip install scrapy
 ```

2) Run the spider of your choise. Metrolyrics.com crawler is provided as an example

```sh
# Go to the scrapy project top level folder
cd crawlers

# Run the spider - output the results as simple csv file (json etc is also possible)
scrapy crawl metrolyrics -o ../lyricdb/lyrics.csv -t csv
```

Go and do something else. You'll probably end up with 2M rows of extracted lyrics.


## Make some song lyrics

Run the simple python script which picks out random rows from the file and mixes them up. The ouput is saved under newlyrics/ folder and the name of the file is the title of the new song

```sh
# lyrics with default values
python makeasong.py -i "lyricdb/lyrics.csv"

# you can also choose how many verses or choruses and how long (rows) they are
python makeasong.py -i "lyricdb/a_to_z.csv" -o newlyrics  --verses 3 --verse_lenght 10 --choruses 1
```

## Demo

Small demo app with limited lyrics is running at:

http://lucky-curve-775.appspot.com/


